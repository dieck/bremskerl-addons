# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP Module
#    
#    Copyright (C) 2010-2011 BREMSKERL-REIBBELAGWERKE EMMERLING GmbH & Co. KG
#    Author Marco Dieckhoff
#
##############################################################################
{
    "name": "Add a menu item to Sales Orders without setting salesman in search",
    "version": "1.0",
    "depends": ["sale"],
    "author": "Marco Dieckhoff, BREMSKERL",
    "category": "Sales",
    "description": """Add a menu item to Sales Orders without setting salesman in search""",
    "init_xml": [],
    'update_xml': ["view/sale_view.xml",
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': '${certificate}',
}