from openerp import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class invoice_line_with_custom_create(models.Model):
    _inherit = ['account.invoice.line']

    @api.model
    def create(self, values):
        if 'invoice_line_tax_ids' not in values or values['invoice_line_tax_ids'] == None or len(values['invoice_line_tax_ids']) == 0:
            # NEW TAX COMPUTATION FROM HERE
            values['invoice_line_tax_ids'] = None

            invoice = self.env['account.invoice'].search([('id', '=', values.get('invoice_id'))])
            product = self.env['product.product'].search([('id', '=', values.get('product_id'))])
            category = product.categ_id
            applicable_taxes = []
            if (invoice.type == 'out_invoice') or (invoice.type == 'out_refund'):
                for tax in category.taxes_id:
                    if tax.company_id == invoice.company_id:
                        applicable_taxes.append(tax.id)
            elif (invoice.type == 'in_invoice') or (invoice.type == 'in_refund'):
                for tax in category.supplier_taxes_id:
                    if tax.company_id == invoice.company_id:
                        applicable_taxes.append(tax.id)

            # Convert to other taxes if invoice (and so partner) has a specific fiscal position
            applied_taxes =[]
            for tax in applicable_taxes:
                for rule in invoice.fiscal_position_id.tax_ids:
                    if tax == rule.tax_src_id.id:
                        applicable_taxes.remove(tax)
                        applied_taxes.append(rule.tax_dest_id.id)
                        break

            values['invoice_line_tax_ids'] = [[6, None, applied_taxes]]
        return super(invoice_line_with_custom_create, self).create(values)
