# -*- coding: utf-8 -*-
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
    "name": "Tagging",
    "version": "1.0",
    "depends": ["base", "base_tools" ],
    "author": "Marco Dieckhoff, BREMSKERL",
    "category": "Tools",
    "description": """
This addon, together with it's modular extensions, provides tagging for multiple modules.

Tags can be used to link different objects, from Sales Offers to Delivery Orders to a specific keyword, thus creating a one-point-overview.
Every object may belong to multiple tags, allowing a kind of project-based fast access over all related elements.
 
Tags can be looked up in Tools / Tagging.

Modular extensions provide relations to the different objects. 
    """,
    "init_xml": [],
    'update_xml': ["security/ir.model.access.csv",
                   "view/tagging_view.xml",
                   ],
    'demo_xml': [],
    'installable': True,
    'active': False,
#    'certificate': '${certificate}',
}