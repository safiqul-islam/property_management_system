from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class PmsPropertySold(models.Model):
    _name = 'pms.property.sold'
    _description = 'this table is for storing the sold out property records'

    property_id = fields.Many2one('pms.property', string='Property')
    customer = fields.Many2one('pms.customer', string='Customer')
    purpose = fields.Selection([('sold', 'Sold')])



    # def confirm_action(self):

    #     for record in self.booking_line_ids:
    #         if record.availability != 'available':
    #             raise ValidationError('Insert a available property')
        

    #     self.state = 'confirmed'

    #     new_delivery = self.env['pms.delivery'].create({
    #         'booking_id': self.id,
            
    #         # Add other fields for the delivery record
    #     })

    #     # You can perform additional actions if needed

    #     return {
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'pms.delivery',
    #         'res_id': new_delivery.id,
    #         'view_mode': 'form',
    #         'view_id': False,
    #         'target': 'current',
    #     }