# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP Module
#    
#    Copyright (C) 2010-2011 BREMSKERL-REIBBELAGWERKE EMMERLING GmbH & Co. KG
#    Author Marco Dieckhoff
#
##############################################################################
{
    "name": "Test Equiment Management",
    "version": "1.0",
    "depends": ["base", "decimal_precision", "account", "audittrail", "base_tools"],
    "author": "Marco Dieckhoff, BREMSKERL",
    "category": "Custom",
    "description": """Test Equipment Management Suite""",
    "init_xml": [],
    'update_xml': ["data/tem_data.xml",
                   "security/tem_security.xml",
                   "security/ir.model.access.csv", 
                   "view/tem_view.xml",
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': '${certificate}',
}