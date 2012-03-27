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
    "name": "Add commitment date for sale order lines using sale_layout",
    "version": "6.0.3",
    "depends": ["sale_order_line_dates", "sale_layout"],
    "recommended": ["sale_order_dates"],
    "author": "Marco Dieckhoff, BREMSKERL",
    "category": "Sales",
    "description": "Adds commitment date for sale order lines using sale_layout",
    "init_xml": [],
    'update_xml': ["view/sale_view.xml",
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': '${certificate}',
}