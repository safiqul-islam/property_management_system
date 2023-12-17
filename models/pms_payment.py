from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError


class PmsPayment(models.Model):
    _name = 'pms.payment'
    _description = 'payment table'

    name = fields.Char(string='Name', required=True, copy=False, readonly=True, index=True, default='New')

    booking_id = fields.Many2one('pms.property.contract',string='Booking')
    booking_records_ids = fields.One2many(string='Properties', related='booking_id.booking_line_ids')
    
    customer_id = fields.Many2one('pms.customer', string='Customer')
    customer_address = fields.Char(related='customer_id.address')

    invoice_date = fields.Date(string='Invoice Date', default=fields.date.today())
    payment_reference = fields.Char(string='Payment Reference', related='booking_id.name')
    payment_terms = fields.Many2one( 'pms.payment.terms',string='Payment Terms', related='booking_id.payment_term')
    due_date = fields.Date(string='Due Date')

    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env['res.currency'].search([('name', '=', 'USD')]))
    amount_total = fields.Monetary(string='Total', related='booking_id.total_amount')
    amount_paid = fields.Monetary(string='Paid Amount', compute='_get_due')
    amount_due = fields.Monetary(string='Due Amount', compute='_get_due')
    need_to_pay = fields.Monetary(string='Need to pay', compute='_get_due')

    payment_state = fields.Selection([('not_paid','Not Paid'),('paid','Paid'),('partially_paid','Partially Paid')], string='Payment Status', default='not_paid')
    state = fields.Selection([('draft','Draft'),('posted','Posted')], string='Status')

    transaction_ids = fields.One2many('pms.transaction.line','invoice_id',string='Transaction Line')


    note = fields.Char(string='Note')

    transaction_count = fields.Integer(string='Transaction Count', compute='_transaction_count')





    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            sequence = self.env['ir.sequence'].next_by_code('pms_invoice_sequence') or '/'
            vals['name'] = sequence
        return super(PmsPayment, self).create(vals)
    
    @api.depends('amount_paid')
    def _get_due(self):

        tran_obj = self.env['pms.transaction.line']

        for self in self:

            find_obj = tran_obj.search([('invoice_id','=',self.id),('booking_id','=',self.booking_id.id),('customer_id','=',self.customer_id.id)])

            total_paid = 0
            for item in find_obj:
                total_paid = total_paid + item.amount_paid

            self.amount_paid = total_paid
            self.amount_due = self.amount_total - total_paid

            if self.amount_due == 0:
                self.need_to_pay = 0
            else:
                self.need_to_pay = self.amount_due
        


    # for payment wizard
    def open_payment_wizard(self):

        return {
            'name': 'Create Bill',
            'type': 'ir.actions.act_window',
            'res_model': 'pms.payment.bill',
            'view_mode': 'form',
            'view_id': self.env.ref('property_management_system.view_pms_payment_wizard_form').id,
            'target': 'new',
            'context': {'invoice_id':self.id,'booking_id':self.booking_id.id,'customer_id':self.customer_id.id, 'need_to_pay_amount':self.need_to_pay,'currency_id':self.currency_id},
            # 'binding_model_id': self.env.ref('property_management_system.model_my_model').id,
        }
    
    @api.depends('transaction_ids')
    def _transaction_count(self):
        for rec in self:
            rec.transaction_count = len(rec.transaction_ids)
    
    def view_transaction(self):
        # return {
        #             'type': 'ir.actions.act_window',
        #             'name': 'pms_transaction',
        #             'res_model': 'pms.transaction.line',
        #             'domain':[('id','=',self.transaction_ids.id)],
        #             'view_mode': 'tree,form',
        #             'target': 'current',
        #         }
    
        if len(self.transaction_ids) == 1:
           return {
                'type': 'ir.actions.act_window',
                'res_model': 'pms.transaction.line',
                'res_id': self.transaction_ids.id,
                'view_mode': 'form',
                'view_id': False,
                'target': 'current',
            }
        else:

            return {
                'type': 'ir.actions.act_window',
                'name': 'pms_transaction',
                'res_model': 'pms.transaction.line',
                'domain':[('id','in',self.transaction_ids.ids)],
                'view_mode': 'tree,form',
                'target': 'current',
            }
