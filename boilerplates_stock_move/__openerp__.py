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
    'name' : 'Boilerplates for Stock Moves',
    'version' : '6.0',
    'author' : 'Marco Dieckhoff, BREMSKERL',
    'website' : 'www.bremskerl.com',
    'depends' : ['boilerplates','boilerplates_stock','stock_move_notes'],
    # Hint: stock_move_notes is a custom addon from me, too :)
    'category' : 'Boilerplates',
    'description': "Adds Boilerplate actions to Stock Moves forms",
    'init_xml' : [],
    'demo_xml' : [],
    'update_xml' : ['wizard/boilerplates_view.xml'],
    'active': False,
    'installable': True
}
