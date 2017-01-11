import calendar
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from openerp import api, fields, models, _
from openerp.exceptions import UserError, ValidationError
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT as DF
from openerp.tools import float_compare, float_is_zero


import logging
_logger = logging.getLogger(__name__)

class account_asset_depreciation_line_improved(models.Model):
    _inherit = ['account.asset.depreciation.line']

    depreciated_value = fields.Float(string='Amount Already Depreciated', required=True)
    cumulative_depreciated_value = fields.Float(string='Cumulative Depreciation', required=True)