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
    "name": "Add a menu item to Project to start with Group by Parent set",
    "version": "1.0",
    "depends": ["project"],
    "author": "Marco Dieckhoff, BREMSKERL",
    "category": "Project Management",
    "description": """Adds a menu item to Project to start with Group by Parent set""",
    "init_xml": [],
    'update_xml': ["view/project_view.xml",
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': '${certificate}',
}