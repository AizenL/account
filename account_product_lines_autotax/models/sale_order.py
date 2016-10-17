from openerp import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class sale_order_line_with_custom_create(models.Model):
    _inherit = ['sale.order.line']

    @api.model
    def create(self, values):
        if 'tax_id' not in values or values['tax_id'] == None or len(values['tax_id']) == 0:
            # NEW TAX COMPUTATION FROM HERE
            values['tax_id'] = None

            sale = self.env['sale.order'].search([('id', '=', values.get('order_id'))])
            product = self.env['product.product'].search([('id', '=', values.get('product_id'))])
            category = product.categ_id
            applicable_taxes = []
            for tax in category.taxes_id:
                if tax.company_id == sale.company_id:
                    applicable_taxes.append(tax.id)
            values['tax_id'] = [[6, None, applicable_taxes]]

            # Convert to other taxes if invoice (and so partner) has a specific fiscal position
            for tax in applicable_taxes:
                for rule in sale.fiscal_position_id.tax_ids:
                    if tax == rule.tax_src_id.id:
                        applicable_taxes.remove(tax)
                        applicable_taxes.append(rule.tax_dest_id.id)
                        break

        return super(sale_order_line_with_custom_create, self).create(values)
