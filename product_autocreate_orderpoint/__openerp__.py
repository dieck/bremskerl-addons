# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP Module
#    
#    Copyright (C) 2012+ BREMSKERL-REIBBELAGWERKE EMMERLING GmbH & Co. KG
#    Author Marco Dieckhoff
#
##############################################################################
{
    "name": "Create Minimum Stock Rule (Orderpoint) for new/changed products",
    "version": "1.01",
    "depends": ["product", "procurement", "stock"],
    "author": "Marco Dieckhoff, BREMSKERL",
    "category": "Inventory Control",
    "description": """Creates a Minimum Stock Rule (Orderpoint) for min. 0, max. 0 on new or changed stockable products, if no orderpoint exists.
    """,
    "init_xml": [],
    'update_xml': [],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': '${certificate}',
}