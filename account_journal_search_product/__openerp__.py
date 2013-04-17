# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP Module
#    
#    Copyright (C) 2013+ BREMSKERL-REIBBELAGWERKE EMMERLING GmbH & Co. KG
#    Author Marco Dieckhoff
#
##############################################################################
{
    "name": "Add product search field to journal items view",
    "version": "1.0",
    "depends": ["account"],
    "author": "Marco Dieckhoff, BREMSKERL",
    "category": "Generic Modules/Accounting",
    "description": """Add product search field to journal items view
    """,
    "init_xml": [],
    'update_xml': ["view/account_view.xml",
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': '${certificate}',
}