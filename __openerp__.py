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
    "name": "Add field to choose Raw Material Location to BoM",
    "version": "1.0",
    "depends": ["mrp","sale"],
    "author": "Marco Dieckhoff, BREMSKERL",
    "category": "Production",
    "description": """Add field to choose Raw Material Location to BoM.
    This is then used in new Manufactoring Orders, and in the generated Stock Moves.
    """,
    "init_xml": [],
    'update_xml': ["view/mrp_view.xml",
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': '${certificate}',
}