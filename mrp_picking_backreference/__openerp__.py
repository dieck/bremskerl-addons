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
    "name": "Add backtracking reference for stock moves to manufactoring orders for raw material provision",
    "version": "1.0",
    "depends": ["mrp","stock"],
    "author": "Marco Dieckhoff, BREMSKERL",
    "category": "Production",
    "description": "Add backtracking reference for stock moves to manufactoring orders for raw material provision",
    "init_xml": [],
    'update_xml': ["view/stock_view.xml",
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': '${certificate}',
}