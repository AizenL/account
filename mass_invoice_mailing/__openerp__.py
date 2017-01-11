{
   'name': "Mass invoice mailing",
    'version': '9.0.1.0',
    'depends': ['account'],
    'author': "Bernard DELHEZ, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Accounting',
    'description': 
    """
    Mass invoice mailing

    It adds a new menuitem "Send by email" in the more section when your are on Customer Invoices.
    It sends all selected invoices that are not already sent and have the state open.
    
    This module has been developed by Bernard Delhez, intern @ AbAKUS it-solutions, under the control of Valentin Thirion.
    """,
    'data': ['wizard/send_invoices_by_email.xml',
            ],
}
