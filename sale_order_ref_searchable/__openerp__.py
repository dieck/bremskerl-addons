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
    "name": "View Sales Orders: Customer Reference always directly searchable",
    "version": "6.0.3",
    "depends": ["sale"],
    "author": "Marco Dieckhoff, BREMSKERL",
    "category": "Sales",
    "description": "View Sales Orders: Customer Reference always directly searchable",
    "init_xml": [],
    'update_xml': ["view/sale_view.xml",
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': '${certificate}',
}