from openerp.osv import osv

class account_invoice_mass_mailing(osv.osv_memory):
    _name = "account.invoice.mass.mailing"
    _description = "Invoice Mass Mailing"

    def send_invoices_by_email(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        active_ids = context.get('active_ids', []) or []

        account_invoice_obj = self.pool['account.invoice']
        email_template_obj = self.pool['mail.template']
        mail_mail_obj = self.pool['mail.mail']
        template_ids = email_template_obj.search(cr, uid, [('name', '=','Invoice - Send by Email')], context=context)
        
        if template_ids:
            for invoice in account_invoice_obj.browse(cr, uid, active_ids, context=context):
                if invoice.state == 'open' and invoice.sent==False:
                    email_template_obj.send_mail(cr, uid, template_ids[0], invoice.id, force_send=True)
                    invoice.sent = True
                
        return {'type': 'ir.actions.act_window_close'}
