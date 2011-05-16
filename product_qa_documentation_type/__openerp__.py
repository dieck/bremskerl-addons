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
    "name": "Add QA documentation type",
    "version": "1.01",
    "depends": ["product_qa"],
    "author": "Marco Dieckhoff, BREMSKERL",
    "category": "Inventory Control",
    "description": """Add field for type of documentation (quality assurance)
    """,
    "init_xml": [],
    'update_xml': ["view/product_view.xml"],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': '${certificate}',
}