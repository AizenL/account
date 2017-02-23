{
    'name': "Belgium VAT Checks",
    'version': '9.0.1.0.1',
    'depends': [
        'l10n_be',
    ],
    'author': "Valentin THIRION, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Sales',
    'description': """
Ths module adds a wizard that do a serie of checks on the VAT report that are used by the financial people to evaluate the coherence of the Belgium VAT declaration.

This module has been developed by Valentin THIRION @ AbAKUS it-solutions.""",
    'data': [
        'wizard/vat_check_wizard.xml',
    ],
}