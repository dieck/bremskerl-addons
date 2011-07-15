# -*- coding: utf-8 -*-

from osv import osv, fields
from tools.translate import _

class tags(osv.osv):
    _name = "tagging.tags"
    _columns = {
        "name": fields.char("Tag", size=64, required=True, translate=True),
        "description": fields.char("Short Description", size=256, translate=True),
        "notes": fields.text("Notes"),
        "active": fields.boolean("Archived"),
    }
    _defaults = {
        "active": lambda *a: False,
    }
    _sql_constraints = [
        ('tagging_tags_name_unique', 'unique (name)', _('The tag names must be unique!')),
    ]
tags()
     