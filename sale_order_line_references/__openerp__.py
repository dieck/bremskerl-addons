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
    "name": "Adds customer reference to Sale Order Lines tree view",
    "version": "6.0.3",
    "depends": ["sale_order_lines"],
    "author": "Marco Dieckhoff, BREMSKERL",
    "category": "Sales",
    "description": "Adds customer reference to Sale Order Lines tree view",
    "init_xml": [],
    'update_xml': ["view/sale_view.xml",
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': '${certificate}',
}