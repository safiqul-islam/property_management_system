from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError


class PmsSaleOrderLine(models.Model):


    _name =  'pms.sale.order.line'
    _description = 'for storing sale order line'

    name = fields.Char(string='Name')
    