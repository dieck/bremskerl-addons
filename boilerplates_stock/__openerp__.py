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
    'name' : 'Boilerplates for Stock',
    'version' : '6.0',
    'author' : 'Marco Dieckhoff, BREMSKERL',
    'website' : 'www.bremskerl.com',
    'depends' : ['boilerplates','stock'],
    'category' : 'Boilerplates',
    'description': "Adds Boilerplate actions to Stock forms: Delivery Notes",
    'init_xml' : [],
    'demo_xml' : [],
    'update_xml' : ['view/boilerplates_view.xml', 'wizard/boilerplates_view.xml'],
    'active': False,
    'installable': True
}