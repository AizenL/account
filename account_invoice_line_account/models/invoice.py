from openerp import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class AccountInvoiceLine(models.Model):
    _inherit = ['account.invoice.line']

    @api.model
    def create(self, values):
        record = super(AccountInvoiceLine, self).create(values)

        if record.product_id and record.product_id.type != 'service':
            if record.product_id.income_analytic_account_id:
                record.income_analytic_account_id = record.product_id.income_analytic_account_id
            elif record.product_id.categ_id and record.product_id.categ_id and record.product_id.categ_id.income_analytic_account_id:
                record.income_analytic_account_id = record.product_id.categ_id.income_analytic_account_id
            else:
                record.income_analytic_account_id = False

        return record