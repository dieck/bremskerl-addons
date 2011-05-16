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
    "name": "Make field to choose Raw Material Location to BoM mandatory",
    "version": "1.0",
    "depends": ["mrp_raw_material_location"],
    "author": "Marco Dieckhoff, BREMSKERL",
    "category": "Production",
    "description": """Make field to choose Raw Material Location to BoM mandatory
    """,
    "init_xml": [],
    'update_xml': ["view/mrp_view.xml",
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': '${certificate}',
}