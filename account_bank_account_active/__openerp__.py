{
    'name': "Bank account active",
    'version': '9.0.1.0.1',
    'depends': ['account'],
    'author': "Valentin THIRION & Bernard DELHEZ, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Accounting',
    'description': 
    """
    Bank account active

    This module adds a field 'active' on the bank accounts in order to hide the ones that don't exist anymore.

    This module has been developed by Jason PINDAT, intern @ AbAKUS it-solution.
    """,
    'data': [
        'views/account_bank_account.xml',
    ],
}
