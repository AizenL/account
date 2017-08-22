# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions, _

import logging
_logger = logging.getLogger(__name__)

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    partner_vat = fields.Char(string="Vendor's TIN")

    @api.multi
    @api.onchange('partner_id')
    def compute_partner_vat(self):
        for invoice in self:
            invoice.partner_vat = invoice.partner_id.vat