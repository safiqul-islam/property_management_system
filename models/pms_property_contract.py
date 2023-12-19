from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date


class PmsPropertyContract(models.Model):
    _name = 'pms.property.contract'
    _description = 'this table stores customer and property contract'

    name = fields.Char(string='Name', required=True, copy=False, readonly=True, index=True, default='New')


    # property_id = fields.Many2one('pms.property', string='Property')

    booking_line_ids = fields.One2many('pms.boooking.line','booking_id', string='Properties')

    # property_address = fields.Char(related='property_id.address')
    
    customer = fields.Many2one('pms.customer', string='Customer', required=True)
    customer_address = fields.Char(related="customer.address")
    customer_email = fields.Char(related="customer.email")
    customer_phone = fields.Char(related="customer.phone")
    purpose = fields.Selection([('rent', 'Rent'), ('booking', 'Booking')], string='Purpose', default='booking')
    order_date = fields.Date(string='Order Date', default=fields.date.today())
    expiration_date = fields.Date(string='Expiration', default=fields.date.today())
    payment_term = fields.Many2one( 'pms.payment.terms',string='Payment Terms')
    # currency_id = fields.Many2one(string="Currency", related='booking_line_ids.property_id.currency_id.id')
    
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env['res.currency'].search([('name', '=', 'USD')]))
    
    total_amount = fields.Monetary(string='Total', compute='_get_total_amount', store=True)
    # due_amount = fields.Monetary(string='Due Amount')
    
    note = fields.Char(string='Note')
    # start_date = fields.Date(string='Start Date', default=fields.date.today(), retuired=True)
    # end_date = fields.Date(string='End Date', default=fields.date.today(), retuired=True)
    # total_days = fields.Integer(string='Total days')
    
    # price_per_day = fields.Monetary(string='Price Per day', related='property_id.booking_price')
    # amount = fields.Monetary(string='Amount', compute='_get_amount', store=True)
    
    # availability = fields.Selection([('not available','Not Available'),('available','Available')], string='Availability', default='available', compute='_get_availability', store=True)

    state = fields.Selection([  ('cancelled', 'Cancelled'),('draft', 'Draft'),('confirmed', 'Confirmed')], string='Contract Status', default='draft')
    # payment_status = fields.Selection([('fully paid','Fully Paid'),('partially paid','Patially Paid'),('not paid','Not Paid')], string='Payment status', default='not paid')
    delivery_ids = fields.One2many('pms.delivery','booking_id', string='Delivery')
    invoice_ids = fields.One2many('pms.payment','booking_id', string='Invoice')

    delivery_count = fields.Integer(string='Delivery Count', compute='_delivery_count')
    invoice_count = fields.Integer(string='Invoice Count', compute='_invoice_count')

    shipping_policy = fields.Selection([('as soon as possible','As Soon As Possible'),('when all procdedure done','When All Procedure Done')], string='Shipping Policy', default='as soon as possible')

    delivery_date = fields.Date(string='Delivery Date', default=fields.date.today(), required=True)

    delivery_status = fields.Selection([('delivered','Delivered'),('not delivered','Not Delivered')], string='Delivery Status', default='not delivered')

    signed_by = fields.Char(string='Signed By')
    signed_on = fields.Char(string='Signed On')
    Signature = fields.Image(string='Signature')

    confirm_button_show = fields.Boolean(string='Confirm button show', default=False)


    broker_id = fields.Many2one('pms.customer', string='Broker', )
    # sale_person = fields.Many2one( 'pms.customer' ,string='Sale person', default=lambda self:self.env.user )

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            sequence = self.env['ir.sequence'].next_by_code('pms_booking_sequence') or '/'
            vals['name'] = sequence


        return super(PmsPropertyContract, self).create(vals)
    

    @api.depends('booking_line_ids')
    def _get_total_amount(self):
        total = 0

        for record in self.booking_line_ids:
            total = total + record.amount
            
        self.total_amount = total



    @api.depends('delivery_ids')
    def _delivery_count(self):
        for rec in self:
            rec.delivery_count = len(rec.delivery_ids)

    @api.depends('invoice_ids')
    def _invoice_count(self):
        for rec in self:
            rec.invoice_count = len(rec.invoice_ids)

    # @api.onchange('start_date')
    # def get_end_date(self):
    #     self.end_date = self.start_date


    # @api.onchange('start_date', 'end_date')
    # def onchange_start_date_end_date(self):

    #     start_date = self.start_date
    #     end_date = self.end_date

    #     days_difference = (end_date - start_date).days

    #     self.total_days = days_difference

    #     Property_obj = self.env['pms.property.contract']
    #     property = Property_obj.search([('property_id.id','=',self.property_id.id),('end_date','>',date.today())])

    #     for item in property:
    #         if item.start_date <= self.start_date <= item.end_date or item.start_date <= self.end_date <= item.end_date:

    #             self.availability = 'not available'
    #             break
    #         else:
    #             self.availability = 'available'
        

    # @api.depends('end_date')
    # def _get_availability(self):

    #     self.availability = self.availability

    @api.onchange('booking_line_ids')
    def get_confirm_button(self):
        
        for record in self.booking_line_ids:
            if record.availability != 'available':
                self.confirm_button_show = False
            else:
                self.confirm_button_show = True


    def confirm_action(self):

        for record in self.booking_line_ids:

            property_id = record.property_id
            start_date = record.start_date
            end_date = record.end_date

            Property_obj = self.env['pms.boooking.line']
            property_start_time = Property_obj.search([('property_id.id','=',property_id.id),('end_date','>',date.today()),('start_date','<=',start_date),('end_date','>=',start_date)])

            
            if len(property_start_time) >1:
                for item in property_start_time:
                    if item.id != record.id:
                        item.availability = 'not available'
            else:
                property_end_time = Property_obj.search([('property_id.id','=',property_id.id),('end_date','>',date.today()),('start_date','<=',end_date),('end_date','>=',end_date)])

                if len(property_end_time) >1:
                                for item in property_end_time:
                                    if item.id != record.id:
                                        item.availability = 'not available'


            if record.availability != 'available':
                raise ValidationError('Insert a available property')
            else:
                record.state = 'confirm'
        

        self.state = 'confirmed'
        self.confirm_button_show = False

        new_invoice = self.env['pms.payment'].create({
            'booking_id': self.id,
            'customer_id': self.customer.id,
            'state':'draft',
            
            # Add other fields for the delivery record
        })

        # You can perform additional actions if needed

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'pms.payment',
            'res_id': new_invoice.id,
            'view_mode': 'form',
            'view_id': False,
            'target': 'current',
        }

    # @api.model
    def make_payment(self):

        action = self.env.ref('property_management_system.action_pms_delivery').read()[0]
        action['domain'] = [('booking_id', '=', self.id)]

        if len(self.delivery_ids) == 1:
            # If there is a single delivery, open the form view
            action['views'] = [(self.env.ref('property_management_system.pms_delivery_view_form').id, 'form')]
            action['res_id'] = self.delivery_ids.id
        else:
            # If there are multiple deliveries, open the tree view
            action['views'] = [(self.env.ref('property_management_system.pms_delivery_view_tree').id, 'tree')]
            action['res_id'] = False  # No specific record ID for the tree view

        return action



 
    def make_invoice(self):

        if len(self.invoice_ids) == 1:
           return {
                'type': 'ir.actions.act_window',
                'res_model': 'pms.payment',
                'res_id': self.invoice_ids.id,
                'view_mode': 'form',
                'view_id': False,
                'target': 'current',
            }
        else:

            return {
                'type': 'ir.actions.act_window',
                'name': 'pms_invoice',
                'res_model': 'pms.payment',
                'domain':[('id','in',self.invoice_ids.ids)],
                'view_mode': 'tree,form',
                'target': 'current',
            }


    
    def cancel_booking(self):
        self.state = 'cancelled'
        self.confirm_button_show = False

    def make_draft(self):
        self.state = 'draft'


# for report genration task
    # def action_open_wizard(self):
    #     return {
    #         'name': 'Report Wizard',
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'pms.report',
    #         'view_mode': 'form',
    #         'view_id': self.env.ref('property_management_system.view_pms_report_wizard_form').id,
    #         'target': 'new',
    #         'binding_model_id': self.env.ref('property_management_system.model_my_model').id,
    #     }