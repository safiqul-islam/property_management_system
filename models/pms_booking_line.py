from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import date


class PmsBookingLine(models.Model):

    _name = 'pms.boooking.line'
    _description = 'property list for booking'

    property_id = fields.Many2one('pms.property',string='Property', required=True)
    name = fields.Char(string='Name', related='property_id.name')
    booking_id = fields.Many2one('pms.property.contract',string='Booking')
    start_date = fields.Date(string='Start Date', default=fields.date.today())
    end_date = fields.Date(string='End Date', default=fields.date.today())

    property_address = fields.Char(related='property_id.address')

    currency_id = fields.Many2one(string="Currency", related='property_id.currency_id')
    price_per_day = fields.Monetary(string='Price Per day', related='property_id.booking_price')
    total_days = fields.Integer(string='Total days')
    amount = fields.Monetary(string='Amount', compute='_get_amount', store=True)
    booked_confirm = fields.Boolean(string='Booked', default=False)
    availability = fields.Selection([('not available','Not Available'),('available','Available')], string='Availability')

    state = fields.Selection([('cancel','Cancelled'),('draft','Draft'),('confirm','Confimred')],string='Status', default='draft')


    @api.onchange('start_date')
    def get_end_date(self):
        self.end_date = self.start_date


    @api.onchange('start_date', 'end_date')
    def onchange_start_date_end_date(self):

        start_date = self.start_date
        end_date = self.end_date

        if start_date < date.today() or end_date < date.today():
            raise ValidationError('Please Insert a valide date')

        days_difference = (end_date - start_date).days

        self.total_days = days_difference

        if days_difference == 0 or self.state == 'confirm':
            self.availability = 'not available'

        else:

            self.availability = 'available'

            Property_obj = self.env['pms.boooking.line']

            # property = Property_obj.search([('property_id.id','=',self.property_id.id),('end_date','>',date.today())])

            property_start_time = Property_obj.search([('property_id.id','=',self.property_id.id),('end_date','>',date.today()),('start_date','<=',self.start_date),('end_date','>=',self.start_date)])

            if property_start_time and property_start_time.state == 'confirm':
                self.availability = 'not available'
            else:
                property_end_time = Property_obj.search([('property_id.id','=',self.property_id.id),('end_date','>',date.today()),('start_date','<=',self.end_date),('end_date','>=',self.end_date)])

                if property_end_time and property_end_time.state == 'confirm':
                    self.availability = 'not available'
                else:
                    self.availability = 'available'
        

    # @api.depends('start_date','end_date')
    # def _get_availability(self):

    #     Property_obj = self.env['pms.boooking.line']

    #     for record in self:

    #         if record.total_days == 0:
    #             record.availability = 'not available'

    #         property = Property_obj.search([('property_id.id','=',record.property_id.id),('end_date','>',date.today())])

    #         property = property.search([('start_date','<=',record.start_date),('end_date','>=',record.start_date)])

    #         if len(property)>1:
    #             record.availability = 'not available'
    #         else:
    #             property = property.search([('start_date','<=',record.end_date),('end_date','>=',record.end_date)])

    #             if len(property)>1:
    #                 record.availability = 'not available'
    #             else:
    #                 record.availability = 'available'
            

        # for record in self:
        #     avail_state = ''
        #     for item in record:
        #         avail_state = item.availability
        #     record.availability = avail_state


    @api.depends('total_days')
    def _get_amount(self):

        for record in self:
            total_amount = 0
            for item in record:
                total_amount = total_amount + item.total_days * item.price_per_day
            record.amount = total_amount
