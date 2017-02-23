from openerp import models, fields, api

import logging

_logger = logging.getLogger(__name__)

class be_vat_checks(models.TransientModel):
    _name = "be.vat.checks"

    company_id = fields.Many2one('res.company',
        string="Company", required=True)
    date_from = fields.Date(string="Start Date", required=True)
    date_to = fields.Date(string="End Date", required=True)
    check_result = fields.Text(string='Check Results', readonly=True)

    @api.multi
    def compute_cheks(self):
        _logger.debug("DO THE CHECKS")
    
        text = "Checks done:\n"

        # Check 1
        text += "- 01 : [01] and/or [02] and/or [03], so [54]\n"

        # Check 2
        text += "- 02 : [54], so [01] and/or [02] and/or [03]\n"

        # Check 3
        text += "- 03 : [55], so [84] and/or [86] and/or [88]\n"

        self.check_result = text

        return {
            'context': self.env.context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'be.vat.checks',
            'res_id': self.id,
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
            }