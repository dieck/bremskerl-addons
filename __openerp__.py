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
    "name": "Adds decimal precision configuration to Bill of Material units",
    "version": "1.0",
    "depends": ["mrp", "decimal_precision"],
    "author": "Marco Dieckhoff, BREMSKERL",
    "category": "Production",
    "description": "Adds decimal precision configuration to Bill of Material units",
    "init_xml": [],
    'update_xml': ["data/bom_data.xml",
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': '${certificate}',
}