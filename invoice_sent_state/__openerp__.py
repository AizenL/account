{
    'name': "Invoice sent state",
    'version': '9.0.1.0',
    'depends': ['account_accountant'],
    'author': "Valentin THIRION, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Invoicing',
    'description': """
    #Sent state on invoice

    This module adds a new state info "sent" for the invoice, it is set auto to 'True' when sent by email or printed.
    It shows it in the tree view and in the form view.

    This module has been developed by Valentin THIRION @ AbAKUS it-solutions
    """,
    'data': ['account_invoice_view.xml',],
    'demo': [],
}
