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
    "name": "Add a menu item to Purchase Orders without setting Responsible in search",
    "version": "1.0",
    "depends": ["purchase"],
    "author": "Marco Dieckhoff, BREMSKERL",
    "category": "Purchases",
    "description": """Add a menu item to Purchase Orders without setting Responsible in search""",
    "init_xml": [],
    'update_xml': ["view/purchase_view.xml",
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': '${certificate}',
}