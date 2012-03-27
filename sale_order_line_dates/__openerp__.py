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
    "name": "Add commitment date for sale order lines",
    "version": "6.0.3",
    "depends": ["sale_order_dates"],
    "author": "Marco Dieckhoff, BREMSKERL",
    "category": "Sales",
    "description": """Adds commitment date for sale order lines
    
    !ATTENTION! Will not show fields with sale_layout installed. Use sale_layout_order_line_dates.

    """,
    "init_xml": [],
    'update_xml': ["view/sale_view.xml",
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': '${certificate}',
}