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
    "name": "QA section in product information",
    "version": "1.01",
    "depends": ["product"],
    "author": "Marco Dieckhoff, BREMSKERL",
    "category": "Inventory Control",
    "description": """Provides QA section in product information for multiple addons
    """,
    "init_xml": [],
    'update_xml': ["view/product_view.xml"],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': '${certificate}',
}