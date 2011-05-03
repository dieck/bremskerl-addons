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
    "name": "Add Sale Reference to MRP Production tree view",
    "version": "1.0",
    "depends": ["sale_mrp"],
    "author": "Marco Dieckhoff, BREMSKERL",
    "category": "Production",
    "description": """Add Sale Reference to MRP Production tree view""",
    "init_xml": [],
    'update_xml': ["view/mrp_view.xml",
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': '${certificate}',
}