from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import re


class PmsCustomer(models.Model):
    _name = 'pms.customer'
    _description = 'This table stores customer information'

    # first_name = fields.Char(string='First Name' , required=True)
    # last_name = fields.Char(string='Last Name', required=True)
    name = fields.Char(string='Name')
    gender = fields.Selection([('male','Male'),('female','Female'),('other','Other')])
    date_of_birth = fields.Date(string='Date of Birth')
    nid_number = fields.Char(string='NID Number', required=True)
    phone = fields.Char(string='Phone Number')
    email = fields.Char(string='Email')
    photo = fields.Image(string='Photo')
    occupation = fields.Char(string='Occupation')
    job_position = fields.Char(string='Job Position')
    address = fields.Char(string='Address')
    post_code = fields.Char(string='Postcode')
    is_broker = fields.Boolean(string='Is a Broker ?')
    invoice_ids = fields.One2many('pms.payment','customer_id', string='Invoice')
    booking_ids = fields.One2many('pms.property.contract','customer', string='Booking')

    # @api.onchange('first_name','last_name')
    # def onchange_firs_name_last_name(self):
    #     self.update({'name': str(self.first_name) + ' ' + str(self.last_name)})


    @api.onchange('email')
    def _get_email(self):

        if self.email:

            a = re.match(r'[a-zA-Z0-9_-]+@[a-zA-Z0-9]+\.[a-zA-Z]{1,3}$',str(self.email))
            if a:
                pass
            else:
                raise ValidationError('Give a valid email address')
        else:
            pass
            

    # @api.onchange('phone')
    # def _get_phone(self):
    #     if len(self.phone) <= 11:

    #         a = re.match(r'[0-9]{1,11}$',str(self.phone))
    #         if a:
    #             pass
    #         else:
    #             raise ValidationError('Give a valid email address')

    #     elif len(self.phone) > 11:

    #         a = re.match(r'[a-zA-Z0-9_-]+@[a-zA-Z0-9]+\.[a-zA-Z]{1,3}$',str(self.phone))
    #         if a:
    #             pass
    #         else:
    #             raise ValidationError('Give a valid email address')