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
    'name' : 'Survey: Change Response User',
    'version' : '6.0',
    'author' : 'Marco Dieckhoff, BREMSKERL',
    'website' : 'www.bremskerl.com',
    'depends' : ['survey'],
    'category' : 'Tools',
    'description': "Allows changing the user for the last entered survey answer, thus allowing to input legacy answers (like fax) of your partners more convenient.",
    'init_xml' : [],
    'demo_xml' : [],
    'update_xml' : ["security/survey_security.xml",
                    "security/ir.model.access.csv",
                    "wizard/survey_answer.xml",
                    ],
    'active': False,
    'installable': True
}
