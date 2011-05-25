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
    "name": "Add note fields to MRP Orders and BoMs",
    "version": "1.0",
    "depends": ["mrp"],
    "author": "Marco Dieckhoff, BREMSKERL",
    "category": "Production",
    "description": "Adds note fields to MRP Orders and BoMs",
    "init_xml": [],
    'update_xml': ["view/mrp_view.xml",
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': '${certificate}',
}