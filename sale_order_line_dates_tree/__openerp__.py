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
    "name": "Add commitment date for sale order lines to tree view",
    "version": "6.0.3",
    "depends": ["sale_order_lines", "sale_order_line_dates"],
    "author": "Marco Dieckhoff, BREMSKERL",
    "category": "Sales",
    "description": """Adds commitment date for sale order lines
    
    Please note: inline view in Sales orders does not change, only the Sale Order Line tree view.
    """,
    "init_xml": [],
    'update_xml': ["view/sale_view.xml",
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': '${certificate}',
}