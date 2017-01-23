{
    'name': "Remittance Advice on Payment Orders",
    'version': '9.0.1.0.1',
    'depends': [
        'account_payment_order',
        'account_payment_partner',
    ],
    'author': "Valentin THIRION, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Accounting',
    'description': 
    """
    
    
    This module has been developed by Valentin THIRION, @ AbAKUS it-solutions.
    """,
    'data': [
        'views/res_partner_view.xml',
        'views/account_payment_line.xml',
        'views/account_payment.xml',
        'data/remittance_advice_mail_template.xml',
    ],
}