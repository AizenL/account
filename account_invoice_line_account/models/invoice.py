from openerp import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class AccountInvoiceLine(models.Model):
    _inherit = ['account.invoice.line']

    @api.model
    def create(self, values):
        record = super(AccountInvoiceLine, self).create(values)

        if record.product and record.product.type != 'service':
            if record.product.income_analytic_account_id:
                record.income_analytic_account_id = record.product.income_analytic_account_id
            elif record.product.categ_id and record.product.categ_id and record.product.categ_id.income_analytic_account_id:
                record.income_analytic_account_id = record.product.categ_id.income_analytic_account_id
            else:
                record.income_analytic_account_id = False

        return record