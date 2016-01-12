# -*- coding: utf-8 -*-

from osv import osv, fields
from tools.translate import _

class tags(osv.osv):
    _name = "tagging.tags"
    _columns = {
        "name": fields.char("Tag", size=64, required=True, translate=True),
        "description": fields.char("Short Description", size=256, translate=True),
        "notes": fields.text("Notes"),
        "active": fields.boolean("Active"),
    }
    _defaults = {
        "active": lambda *a: True,
    }
    _sql_constraints = [
        ('tagging_tags_name_unique', 'unique (name)', _('The tag names must be unique!')),
    ]
tags()

class tagging_related_tags(osv.osv):
    _inherit = "tagging.tags"
    _name = _inherit

    _columns = {
        "related_tags_ids": fields.many2many("tagging.tags", "tagging_related_tags", "tag_id", "related_tag_id", string="Related Tags"),
        
    }
tagging_related_tags()
