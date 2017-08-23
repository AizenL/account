from openerp import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class AccountInvoiceLine(models.Model):
    _inherit = ['account.invoice.line']

    @api.model
    def create(self, values):
        product = self.env['product.product'].search([('id', '=', values['product_id'])]) if values.get('product_id') else self.product_id

        if product and product.type != 'service':
            if product.income_analytic_account_id:
                values['account_analytic_id'] = product.income_analytic_account_id.id
            elif product.categ_id and product.categ_id and product.categ_id.income_analytic_account_id:
                values['account_analytic_id'] = product.categ_id.income_analytic_account_id.id
            else:
                values['account_analytic_id'] = False

        if values.get('account_analytic_id'):
            _logger.info('\n\n' + str(values['account_analytic_id']) + '\n\n')

        return super(AccountInvoiceLine, self).create(values)