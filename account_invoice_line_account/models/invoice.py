from openerp import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class AccountInvoiceLine(models.Model):
    _inherit = ['account.invoice.line']

    def _compute_values(self, values):

        product = self.env['product.product'].search([('id', '=', values['product_id'])]) if values.get('product_id') else self.product_id

        # if product:
        #     if product.type != 'service':
        #         if 

        _logger.info('\n\n' + str(product) + '\n\n')

        _logger.info('\n\n' + str(product.type) + '\n\n')

        if(values.get('income_analytic_account_id'))
            _logger.info('\n\n' + str(self.env['account.analytic.account'].search([('id', '=', values['income_analytic_account_id'])]).name) + '\n\n')

        return values

    @api.model
    def create(self, values):
        _logger.info('\n\nCREATE\n\n')
        values = self._compute_values(values)
        return super(AccountInvoiceLine, self).create(values)

    @api.one
    def write(self, values):
        _logger.info('\n\nWRITE\n\n')
        values = self._compute_values(values)
        return super(AccountInvoiceLine, self).write(values)