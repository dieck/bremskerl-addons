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
    "name": "Add production lot in manufactoring order views",
    "version": "1.0",
    "depends": ["mrp"],
    "author": "Marco Dieckhoff, BREMSKERL",
    "category": "Production",
    "description": """Add production lot in manufactoring order views
        Tab 'Consumed products' / 'Products to consume',
        Tab 'Finished products' / 'Products to finish'
    """,
    "init_xml": [],
    'update_xml': ["view/mrp_view.xml",
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': '${certificate}',
}