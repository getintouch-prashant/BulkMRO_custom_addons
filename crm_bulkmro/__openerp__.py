# -*- coding: utf-8 -*-
{
    'name': "crm_bulkmro",

    'summary': """
        Custom CRM lead module for BulkMRO.
        """,

    'description': """
        Main Features : 
        * Assigns a Unique Sequence number to every new lead created.
        """,

    'author': "Prashant Kumar",
#     'website': "http://www.yourcompany.com",

    'category': 'Customer Relationship Management',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'crm'],

    # always loaded
    'data': [
             'lead_view.xml'
        # 'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}