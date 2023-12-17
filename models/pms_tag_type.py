from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class PmsTagType(models.Model):
    _name = 'pms.property.tag.type'
    _description = 'property tag type realted table'

    name = fields.Char(string='Property tag type name')