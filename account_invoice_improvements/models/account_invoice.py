from openerp import models, fields, api, _
from openerp.exceptions import ValidationError

import logging

_logger = logging.getLogger(__name__)

class account_invoice_improved(models.Model):
    _inherit = ['account.invoice']

    next_invoice_number = fields.Char(compute='_compute_next_invoice_number', string="Next document number", store=False)
    comment = fields.Html('Additional Information', readonly=True, states={'draft': [('readonly', False)]})


    @api.one
    @api.depends('journal_id')
    def _compute_next_invoice_number(self):
        if not self.journal_id:
            self.next_invoice_number =  "NO JOURNAL SELECTED"
            return

        if self.state in ("", "draft"):
            nn_int = self.journal_id.sequence_id.number_next
            nn_string = str(nn_int)
            
            nn_ex_string = self.env['account.invoice'].search([['journal_id','=',self.journal_id.id],['number', '!=', '']], limit=1).number

            l = len(nn_ex_string) - 1
            if l > 0:
                cpt = 0;
                for i in range(l, 0, -1):
                    if nn_ex_string[i].isnumeric():
                        cpt += 1
                    else:
                        break
                seq = int(nn_ex_string[-cpt:]) + 1
                nn = nn_ex_string[:-cpt]
                self.next_invoice_number =  nn + str(seq)
            else:
                self.next_invoice_number =  '1'
        else:
            self.next_invoice_number =  "ERROR"
    
    @api.onchange('supplier_invoice_number')
    def update_reference(self):
        if self.partner_id and self.supplier_invoice_number and len(self.supplier_invoice_number) > 0:
            account_invoices = self.env['account.invoice'].search([[('supplier_invoice_number', '=', self.supplier_invoice_number),('partner_id','=',self.partner_id.id)]])
            if account_invoices:
                self.reference = ""
                raise ValidationError('Supplier Invoice Number Failure - The supplier invoice number already exists')
            else:
                self.reference = self.supplier_invoice_number
        else:
            self.reference = self.supplier_invoice_number

    @api.multi
    def check_validate_and_send_invoice_if_out(self):
        for line in self.invoice_line_ids:
            # Check if there is a tax on each line
            if len(line.invoice_line_tax_ids) == 0:
                raise ValidationError('No tax! - A line in this invoice does not contain any tax. This is not allowed by the system. Please, correct this.')
                self.write({'state': 'draft'})
            # Check if there is an analytic account on each line
            if len(line.account_analytic_id) == 0:
                raise ValidationError('No Analytic Account! - A line in this invoice does not contain an analytic account. This is not allowed by the system. Please, correct this.')
                self.write({'state': 'draft'})

        #Methods for the validation of the invoice.
        self.action_date_assign()
        self.action_move_create()

        if self.type == 'out_invoice':
            self.invoice_validate()
            #Method that return the mail form.
            return self.action_invoice_sent()
        return self.invoice_validate()
