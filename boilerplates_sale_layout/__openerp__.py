# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP Module
#    
#    Copyright (C) 2012-tbd BREMSKERL-REIBBELAGWERKE EMMERLING GmbH & Co. KG
#    Author Marco Dieckhoff
#
##############################################################################
{
    'name' : 'Boilerplates for Sales with sale_layout',
    'version' : '6.0',
    'author' : 'Marco Dieckhoff (Bremskerl)',
    'website' : 'www.bremskerl.com',
    'depends' : ['boilerplates_sale','sale_layout'],
    'category' : 'Boilerplates',
    'description': """Adds Boilerplate actions to Sales forms: Order Lines""",
    'init_xml' : [],
    'demo_xml' : [],
    'update_xml' : ['wizard/boilerplates_view.xml'],
    'active': False,
    'installable': True
}
