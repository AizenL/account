
from openerp import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)

class Partner(models.Model):
    _inherit = 'res.partner'

    send_remittance_advice = fields.Boolean(string="Send remittance advice", default=False)