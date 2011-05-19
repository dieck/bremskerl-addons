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
    'name' : 'Survey: Show Responses',
    'version' : '6.0',
    'author' : 'Marco Dieckhoff (Bremskerl)',
    'website' : 'www.bremskerl.com',
    'depends' : ['survey'],
    'category' : 'Tools',
    'description': "Shows responses of surveys to survey (and tool) managers",
    'init_xml' : [],
    'demo_xml' : [],
    'update_xml' : ["security/survey_security.xml",
                    "security/ir.model.access.csv",
                    "view/survey_view.xml",
                    ],
    'active': False,
    'installable': True
}
