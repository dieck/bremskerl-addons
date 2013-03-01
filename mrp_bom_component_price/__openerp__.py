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
    "name": "Add cost price to bom line components",
    "version": "1.0",
    "depends": ["mrp"],
    "author": "Marco Dieckhoff, BREMSKERL",
    "category": "Production",
    "description": """Add cost price to bom line components
    """,
    "init_xml": [],
    'update_xml': ["view/mrp_view.xml",
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': '${certificate}',
}