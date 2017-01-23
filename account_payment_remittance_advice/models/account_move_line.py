from openerp import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)

class MoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.multi
    def _prepare_payment_line_vals(self, payment_order):
        vals = super(MoveLine, self)._prepare_payment_line_vals(payment_order)
        vals.update({'send_remittance_advice': self.partner_id.send_remittance_advice})

        return vals
        
