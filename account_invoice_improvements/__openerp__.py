{
    'name': "AbAKUS invoice improvements",
    'version': '9.0.1.0.3',
    'depends': ['account'],
    'author': "Valentin THIRION & Bernard DELHEZ, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Accounting',
    'description': 
    """
    Invoicing improvements

    This modules adds some functionalities to the invoicing process for AbAKUS. 
        - it adds a field in the invoice form with the next invoice number.
        - it auto copies the supplier ref number to the bank transfer communication field.
        - it checks if the supplier invoice number already exists.
        - it adds a group by in account.move.line that groups by journal entry.
        - it changes the fields order in the treeview of account.move.line.
        - it adds a filter that filters on customer accont related move lines on lines
        - it adds a filter that filters on supplier accont related move lines on lines
        - it checks if all the lines of the invoices contains exactly one tax
        - it checks if the 'analytic account' field is set

    This module has been developed by Valentin THIRION @ AbAKUS it-solution.
    """,
    'data': [
        'views/account_invoice_view.xml',
        'views/account_move_line_view.xml',
        'data/invoice_workflow.xml'
    ],
}
