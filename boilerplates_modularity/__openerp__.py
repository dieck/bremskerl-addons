# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP Module
#    
#    Copyright (C) 2010-2011 BREMSKERL-REIBBELAGWERKE EMMERLING GmbH & Co. KG
#    Author Marco Dieckhoff
#
##############################################################################
#
#    Merge Picking up to v5 of OpenERP was written by Axelor, www.axelor.com
#    This is a complete rewrite.
#
##############################################################################
{
    'name' : 'Boilerplates Modularity',
    'version' : '6.0',
    'author' : 'Marco Dieckhoff (Bremskerl)',
    'website' : 'www.bremskerl.com',
    'depends' : ['boilerplates'],
    'category' : 'Boilerplates',
    'description': "Prepares Boilerplates to use module specific addons",
    'init_xml' : [],
    'demo_xml' : [],
    'update_xml' : ['view/boilerplates_view.xml'],
    'active': False,
    'installable': True
}
