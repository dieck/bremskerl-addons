# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP Module
#    
#    Copyright (C) 2013+ BREMSKERL-REIBBELAGWERKE EMMERLING GmbH & Co. KG
#    Author Marco Dieckhoff
#
##############################################################################
{
    "name": "Add future stock moves link to manufactoring orders",
    "version": "1.0",
    "depends": ["mrp","product","stock"],
    "author": "Marco Dieckhoff, BREMSKERL",
    "category": "Production",
    "description": """Add future stock moves link to manufactoring orders
    """,
    "init_xml": [],
    'update_xml': ["view/mrp_view.xml",
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': '${certificate}',
}