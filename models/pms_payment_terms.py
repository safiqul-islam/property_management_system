from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class PmsPaymentTerms(models.Model):
    _name = 'pms.payment.terms'
    _description = 'payment terms table'

    name = fields.Char(string='Name')



class PaymentWizTranziantModel(models.TransientModel):

    _name = 'pms.payment.bill'
    _description = 'bill creation wizard'

    booking_id = fields.Many2one('pms.property.contract', string='Booking')
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env['res.currency'].search([('name', '=', 'USD')]))
    
    name = fields.Char(string='Name')
    payment_method = fields.Selection([('bank','Bank'),('cash','Cash')], string='Payment Method', default='cash')

    is_bank = fields.Boolean(string='Is Bank', default=False)
    bank_name = fields.Char(string='Bank Name')
    branch = fields.Char(string='Branch')
    account_number = fields.Char(string='Account Number')

    # invoice_type = fields.Selection([('regular invoice','Regular Invoice'),('down payment invoice','Down Payment Invoice')], string='Create Invoice', default='regular invoice')


    invoicing_type = fields.Selection([('regular invoice','Regular Invoice'),('down payment invoice','Down Payment Invoice')], string='Create Invoice', default='regular invoice')


    is_down_payment = fields.Boolean(string='Is downpayment', default=False)
    down_payment_amount = fields.Monetary(string='Amount')

    @api.onchange('invoicing_type')
    def get_invoice_type(self):
        if self.invoicing_type == 'down payment invoice':
            self.is_down_payment = True
        else:
            self.is_down_payment = False

    @api.onchange('payment_method')
    def get_payment_method_type(self):
        if self.payment_method == 'bank':
            self.is_bank = True
        else:
            self.is_bank = False


    def create_bill(self):

        invoice_id = self.env.context.get('invoice_id')
        booking_id = self.env.context.get('booking_id')
        customer_id = self.env.context.get('customer_id')
        amount_total = self.env.context.get('need_to_pay_amount')
        currency_id = self.env.context.get('currency_id')

        invoice_obj = self.env['pms.payment']
        obj = invoice_obj.search([('id','=',invoice_id)])

        if self.is_bank:
           bank_name = self.bank_name
           branch = self.branch
           account_number = self.account_number

        else:
           bank_name = ''
           branch = ''
           account_number = ''

        if self.is_down_payment:

            if self.down_payment_amount <= amount_total:
                paid_amount = self.down_payment_amount
                obj.payment_state = 'partially_paid'
            else:
                raise UserError('Insert the valid amount')

        else:
            paid_amount = amount_total
            obj.payment_state = 'paid'


        new_transaction = self.env['pms.transaction.line'].create({
            'invoice_id': invoice_id,
            'booking_id': booking_id,
            'customer_id': customer_id,
            'currency_id': currency_id,
            'bank_name': bank_name,
            'branch':branch,
            'account_number':account_number,
            'amount_paid': paid_amount,
            'payment_method':self.payment_method
            
            # Add other fields for the delivery record
        })

        aleady_paid = obj.amount_paid
        obj.amount_paid = paid_amount + aleady_paid
        obj.state = 'posted'

    


    