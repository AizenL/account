{
    'name': "Structured Communication on Payment Orders",
    'version': '9.0.1.0.1',
    'depends': [
        'account_payment_order',
    ],
    'author': "Valentin THIRION, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Accounting',
    'description': 
    """
    This module will adapt the invoice form to be able to insert a structured BBA communication.

    It will also manage this field value for the payment lines and SEPA exported file.
    
    This module has been developed by Valentin THIRION, @ AbAKUS it-solutions.
    """,
    'data': [
        'views/payment_order_view.xml',
        'views/account_invoice_view.xml',
    ],
}