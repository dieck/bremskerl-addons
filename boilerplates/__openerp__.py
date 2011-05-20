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
    "name": "Boilerplates",
    "version": "1.0",
    "depends": ["base", "base_tools", "product" ],
    "author": "Marco Dieckhoff, BREMSKERL",
    "category": "Custom",
    "description": """
This module
    """,
    "init_xml": [],
    'update_xml': ["security/boilerplates_security.xml",
                   "security/ir.model.access.csv",
                   "data/boilerplates_data.xml", 
                   "view/boilerplates_view.xml",
                   "wizard/boilerplates_wiz_view.xml"],
    'demo_xml': ["data/boilerplates_demo.xml"],
    'installable': True,
    'active': False,
#    'certificate': '${certificate}',
}