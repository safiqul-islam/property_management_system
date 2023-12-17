from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class PmsPropertyTag(models.Model):
    _name = 'pms.property.tag'
    _description = 'this table is for property tag store'

    type_of_tag = fields.Many2one( 'pms.property.tag.type' ,string='Property tag type')
    name = fields.Char(string='Name of tag')