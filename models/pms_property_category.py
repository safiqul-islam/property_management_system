from odoo import models, fields, api, _
from odoo.exceptions import  UserError, ValidationError


class PmsPropertyCategory(models.Model):
    _name = 'pms.property.category'
    _description = 'proerty category list'


    name = fields.Char(string='Category Name')