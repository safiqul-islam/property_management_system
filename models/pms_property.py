from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class PmsProperty(models.Model):
    _name = 'pms.property'
    _description = 'this table is for storing property details'

    name = fields.Char(string='Property Name', required= True)
    address = fields.Char(string='Address')
    postalcode = fields.Char(string='Postal Code')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    photo = fields.Image(string='Image')
    description = fields.Text(string='Description')
    property_file = fields.Binary(string='Property File')
    bedrooms = fields.Integer(string='Bed Rooms')
    living_area = fields.Integer(string='Living Area')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area')
    garden_orientation = fields.Selection( [('north','North'), ('south','South'), ('east','East') ,('west','West')] , string='Garden Orientation' )
    swimming_pool = fields.Boolean(string='Swimming Pool')
    swimming_pool_orientation = fields.Selection( [('north','North'), ('south','South'), ('east','East') ,('west','West')] , string='Swimming Pool' )
    garage = fields.Boolean(string='Garage')
    property_status = fields.Selection([('available','Available'),('booked','booked'),('sold','Sold')], string='Property Status', default='available')
    
    currency_id = fields.Many2one('res.currency', string="Currency", default=lambda self: self.env.company.currency_id.id)
    
    for_sell = fields.Boolean(string='For sell')
    selling_price = fields.Monetary(string='Selling Price')
    
    for_booking = fields.Boolean(string='For Booking', default=True)
    booking_price = fields.Monetary(string='Booking Price per day')

    tag_ids = fields.Many2many('pms.property.tag' ,string='Tags')
    category_id = fields.Many2one('pms.property.category', string='Property Category')


    def availableProperty(self):
        self.property_status = 'available'

    def bookProperty(self):

        return {
            'name': 'book_property',
            'type': 'ir.actions.act_window',
            'res_model': 'pms.property.contract',
            'view_mode': 'form,tree',
            'views': [(False, 'form')],
            'target': 'current',
            'context': { 'default_property_id': self.id,'default_purpose':'booking', 'default_currency_id':self.currency_id.id,'default_price_per_daye':self.booking_price},
            
        }

    def sellProperty(self):
        self.property_status = 'sold'
    
    def rentProperty(self):
        self.property_status = 'rent'
    