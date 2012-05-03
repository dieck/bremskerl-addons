# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP Module
#    
#    Copyright (C) 2010-tbd BREMSKERL-REIBBELAGWERKE EMMERLING GmbH & Co. KG
#    Author Marco Dieckhoff
#
##############################################################################
{
    'name' : 'Boilerplates for Sales',
    'version' : '6.0',
    'author' : 'Marco Dieckhoff, BREMSKERL',
    'website' : 'www.bremskerl.com',
    'depends' : ['boilerplates','sale'],
    'category' : 'Boilerplates',
    'description': """Adds Boilerplate actions to Sales forms: Order Lines
    
    !ATTENTION! Will not work with sale_layout. Use boilerplates_sale_layout.
    
    """,
    'init_xml' : [],
    'demo_xml' : [],
    'update_xml' : ['view/boilerplates_view.xml', 'wizard/boilerplates_view.xml'],
    'active': False,
    'installable': True
}
