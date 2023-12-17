from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError



class PmsDelivery(models.Model):
    _name = 'pms.delivery'
    _rec_names_search = ['name', 'booking_id.name']
    _description = 'delivery main table'

    name = fields.Char(string='Name',  required=True, copy=False, readonly=True)
    state = fields.Selection([('deaft','Draft'),('waiting','Waiting'),('ready','Ready'),('done','Done')], string='Delivery State', default='waiting')

    booking_id = fields.Many2one('pms.property.contract',string='Booking')
    customer = fields.Many2one(string='Delivery to', related="booking_id.customer")

    priority = fields.Selection([
        ('0','Low'),
        ('1','Normal'),
        ('2','High'),
        ('3','Very high')
        ], string='Priority')
    

    scheduled_date = fields.Date(string='Scheduled Date', default=fields.date.today())

    deadline = fields.Date(string='Deadline', related='booking_id.delivery_date')
    shipping_policy = fields.Selection([('as soon as possible','As Soon As Possible'),('when all procdedure done','When All Procedure Done')], string='Shipping Policy', default='as soon as possible')

    source = fields.Char(string='Source', compute='_get_source')

    property_records = fields.One2many(string='Properties', related='booking_id.booking_line_ids')
    
    note = fields.Char(string='Note', related="booking_id.note")
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env['res.currency'].search([('name', '=', 'USD')]))
    
    total_amount = fields.Monetary(string='total', related="booking_id.total_amount")


    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            sequence = self.env['ir.sequence'].next_by_code('pms_delivery_sequence') or '/'
            vals['name'] = sequence
        return super(PmsDelivery, self).create(vals)


    @api.depends('booking_id')
    def _get_source(self):
        for rec in self:
            self.source = rec.booking_id.name


    
    def validate_delivery(self):


        new_payment = self.env['pms.payment'].create({
            'booking_id': self.booking_id.id,
            
            # Add other fields for the delivery record
        })

        self.state = 'done'

        # You can perform additional actions if needed

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'pms.payment',
            'res_id': new_payment.id,
            'view_mode': 'form',
            'view_id': False,
            'target': 'current',
        }
    
    # for payment wizard
    def action_open_payment_wizard(self):

        return {
            'name': 'Create Bill',
            'type': 'ir.actions.act_window',
            'res_model': 'pms.payment.bill',
            'view_mode': 'form',
            'view_id': self.env.ref('property_management_system.view_pms_payment_wizard_form').id,
            'target': 'new',
            # 'binding_model_id': self.env.ref('property_management_system.model_my_model').id,
        }

