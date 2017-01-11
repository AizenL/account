import calendar
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from openerp import api, fields, models, _
from openerp.exceptions import UserError, ValidationError
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from openerp.tools import float_compare, float_is_zero


import logging
_logger = logging.getLogger(__name__)

class account_asset_improved(models.Model):
    _inherit = ['account.asset.asset']

    asset_already_partially_depreciated = fields.Boolean('Asset already partially depreciated')
    already_passed_depreciations = fields.Integer('Passed depreciations')
    

    @api.one
    @api.depends('value', 'salvage_value', 'depreciation_line_ids.move_check', 'depreciation_line_ids.amount')
    def _amount_residual(self):
        total_amount = 0.0
        for line in self.depreciation_line_ids:
            if line.move_check:
                total_amount += line.amount

        if self.asset_already_partially_depreciated:
            posted_depreciation_line_ids = self.depreciation_line_ids.filtered(lambda x: x.move_check).sorted(key=lambda l: l.depreciation_date)
            self.value_residual = posted_depreciation_line_ids[-1].remaining_value
        else:
            self.value_residual = self.value - total_amount - self.salvage_value

    def _compute_board_amount(self, sequence, residual_amount, amount_to_depr, undone_dotation_number, posted_depreciation_line_ids, total_days, depreciation_date):
        amount = 0
        if sequence == undone_dotation_number:
            amount = residual_amount
        else:
            if self.asset_already_partially_depreciated:
                # Depreciate the same amount as older dep
                # old_depreciations_amount =  #posted_depreciation_line_ids[len(posted_depreciation_line_ids) - 1].amount
                return self.value / (self.method_number * self.method_period)
                    
            if self.method == 'linear':
                
                amount = amount_to_depr / (undone_dotation_number - len(posted_depreciation_line_ids))
                _logger.debug("Amount to depr= %s | Undone dot numb = %s | len = %s | Amount = %s", amount_to_depr, undone_dotation_number, len(posted_depreciation_line_ids), amount)
                if self.prorata:
                    amount = amount_to_depr / self.method_number
                    if sequence == 1:
                        if self.method_period % 12 != 0:
                            date = datetime.strptime(self.date, '%Y-%m-%d')
                            month_days = calendar.monthrange(date.year, date.month)[1]
                            days = month_days - date.day + 1
                            amount = (amount_to_depr / self.method_number) / month_days * days
                        else:
                            days = (self.company_id.compute_fiscalyear_dates(depreciation_date)['date_to'] - depreciation_date).days + 1
                            amount = (amount_to_depr / self.method_number) / total_days * days
            elif self.method == 'degressive':
                amount = residual_amount * self.method_progress_factor
                if self.prorata:
                    if sequence == 1:
                        if self.method_period % 12 != 0:
                            date = datetime.strptime(self.date, '%Y-%m-%d')
                            month_days = calendar.monthrange(date.year, date.month)[1]
                            days = month_days - date.day + 1
                            amount = (residual_amount * self.method_progress_factor) / month_days * days
                        else:
                            days = (self.company_id.compute_fiscalyear_dates(depreciation_date)['date_to'] - depreciation_date).days + 1
                            amount = (residual_amount * self.method_progress_factor) / total_days * days
        return amount

    def _compute_board_undone_dotation_nb(self, depreciation_date, total_days):
        undone_dotation_number = self.method_number
        if self.asset_already_partially_depreciated:
            undone_dotation_number = undone_dotation_number - self.already_passed_depreciations

        if self.method_time == 'end':
            end_date = datetime.strptime(self.method_end, DF).date()
            undone_dotation_number = 0
            while depreciation_date <= end_date:
                depreciation_date = date(depreciation_date.year, depreciation_date.month, depreciation_date.day) + relativedelta(months=+self.method_period)
                undone_dotation_number += 1
        if self.prorata:
            undone_dotation_number += 1
        return undone_dotation_number

    @api.multi
    def compute_depreciation_board(self):
        self.ensure_one()

        posted_depreciation_line_ids = self.depreciation_line_ids.filtered(lambda x: x.move_check).sorted(key=lambda l: l.depreciation_date)
        unposted_depreciation_line_ids = self.depreciation_line_ids.filtered(lambda x: not x.move_check)

        # Remove old unposted depreciation lines. We cannot use unlink() with One2many field
        commands = [(2, line_id.id, False) for line_id in unposted_depreciation_line_ids]

        if self.value_residual != 0.0:
            
            amount_to_depr = residual_amount = self.value_residual
            if self.prorata:
                # if we already have some previous validated entries, starting date is last entry + method period
                if posted_depreciation_line_ids and posted_depreciation_line_ids[-1].depreciation_date:
                    last_depreciation_date = datetime.strptime(posted_depreciation_line_ids[-1].depreciation_date, DF).date()
                    depreciation_date = last_depreciation_date + relativedelta(months=+self.method_period)
                else:
                    depreciation_date = datetime.strptime(self._get_last_depreciation_date()[self.id], DF).date()
            else:
                # depreciation_date = 1st of January of purchase year if annual valuation, 1st of
                # purchase month in other cases
                if self.method_period >= 12:
                    asset_date = datetime.strptime(self.date[:4] + '-01-01', DF).date()
                else:
                    asset_date = datetime.strptime(self.date[:7] + '-01', DF).date()
                # if we already have some previous validated entries, starting date isn't 1st January but last entry + method period
                if posted_depreciation_line_ids and posted_depreciation_line_ids[-1].depreciation_date:
                    last_depreciation_date = datetime.strptime(posted_depreciation_line_ids[-1].depreciation_date, DF).date()
                    depreciation_date = last_depreciation_date + relativedelta(months=+self.method_period)
                else:
                    depreciation_date = asset_date
            day = depreciation_date.day
            month = depreciation_date.month
            year = depreciation_date.year
            total_days = (year % 4) and 365 or 366

            undone_dotation_number = self._compute_board_undone_dotation_nb(depreciation_date, total_days)

            #last_already_depreciated_value = 0
            #if self.asset_already_partially_depreciated:
            last_already_depreciated_value = self.value - posted_depreciation_line_ids[-1].remaining_value
            
            for x in range(len(posted_depreciation_line_ids), undone_dotation_number):
                
                sequence = x + 1
                amount = self._compute_board_amount(sequence, residual_amount, amount_to_depr, undone_dotation_number, posted_depreciation_line_ids, total_days, depreciation_date)
                amount = self.currency_id.round(amount)
                if float_is_zero(amount, precision_rounding=self.currency_id.rounding):
                    continue
                residual_amount -= amount

                # The depreciation ends before the supposed date (meaning we probably depreciated too much before)
                last_depreciation = False
                if residual_amount < amount:
                    #amount = amount + residual_amount
                    #residual_amount = 0
                    last_depreciation = True
                    
                vals = {
                    'amount': amount,
                    'asset_id': self.id,
                    'sequence': sequence,
                    'name': (self.code or '') + '/' + str(sequence),
                    'remaining_value': residual_amount,
                    'cumulative_depreciated_value': self.value - (self.salvage_value + residual_amount),
                    'depreciated_value': last_already_depreciated_value,#self.value - (self.salvage_value + residual_amount) - amount, # Added amount here because we want to have the 'previously' depreciated amount before this line
                    'depreciation_date': depreciation_date.strftime(DF),
                }
                commands.append((0, False, vals))
                
                last_already_depreciated_value = last_already_depreciated_value + amount

                if last_depreciation:
                    amount = residual_amount
                    residual_amount -= amount
                    # Considering Depr. Period as months
                    depreciation_date = date(year, month, day) + relativedelta(months=+self.method_period)
                    day = depreciation_date.day
                    month = depreciation_date.month
                    year = depreciation_date.year
                    vals = {
                        'amount': amount,
                        'asset_id': self.id,
                        'sequence': sequence + 1,
                        'name': (self.code or '') + '/' + str(sequence),
                        'remaining_value': residual_amount,
                        'cumulative_depreciated_value': self.value - (self.salvage_value + residual_amount),
                        'depreciated_value': last_already_depreciated_value,#self.value - (self.salvage_value + residual_amount) - amount, # Added amount here because we want to have the 'previously' depreciated amount before this line
                        'depreciation_date': depreciation_date.strftime(DF),
                    }
                    commands.append((0, False, vals))
                    break;


                # Considering Depr. Period as months
                depreciation_date = date(year, month, day) + relativedelta(months=+self.method_period)
                day = depreciation_date.day
                month = depreciation_date.month
                year = depreciation_date.year

        self.write({'depreciation_line_ids': commands})

        return True

    