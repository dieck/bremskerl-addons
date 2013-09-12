# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP Module
#    
#    Copyright (C) 2010-2011 BREMSKERL-REIBBELAGWERKE EMMERLING GmbH & Co. KG
#    Author Marco Dieckhoff
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name' : 'Move RePick (DEPRECATED)',
    'version' : '6.0',
    'author' : 'Marco Dieckhoff, BREMSKERL',
    'website' : 'www.bremskerl.com',
    'depends' : ['stock','sale','stock_sale_order_references'],
    'category' : 'Warehouse',
    'description': """
    This module allows you to pick stock moves from Warehouse - Product Moves - Receive/Deliver Products and combine them into a new picking (Incoming Shipment / Delivery Order).
    
    Deprecated due to side effects. We now use stock_picking_group.

    
    """,
    'init_xml' : [],
    'demo_xml' : [],
    'update_xml' : [ 'view/stock_view.xml',
                     'wizard/move_repick_view.xml',
                    ],
    'active': False,
    'installable': True
}
