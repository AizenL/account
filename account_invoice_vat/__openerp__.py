# -*- coding: utf-8 -*-
{
    'name': "Account Invoice VAT",

    'summary': """
    """,

    'description': """
        Account Invoice VAT
        
        Adds the TIN field of the Vendor in the Vendor Bill form, list & search filter.
        
        This module has been developed by Jason PINDAT, intern @ AbAKUS it-solutions.
    """,

    'author': "Jason PINDAT, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",

    'category': 'Accounting',
    'version': '9.0.1.0',

    'depends': ['base', 'sale', 'account'],

    'data': [
        'views/account_invoice.xml'
    ],
}