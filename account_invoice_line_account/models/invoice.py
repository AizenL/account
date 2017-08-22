from openerp import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class AccountInvoiceLine(models.Model):
    _inherit = ['account.invoice.line']

    @api.model
    def create(self, values):
        return super(AccountInvoiceLine, self).create(values)
