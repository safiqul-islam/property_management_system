from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError


class PmsTransactionLine(models.Model):

    _name = 'pms.transaction.line'
    _description = 'transaction record table'

    name = fields.Char(string='Name', required=True, copy=False, readonly=True, index=True, default='New')
    invoice_id = fields.Many2one('pms.payment', string='Invoice')
    booking_id = fields.Many2one('pms.property.contract', string='Booing Reference')
    customer_id = fields.Many2one('pms.customer',string='Cutomer')
    currency_id = fields.Many2one('res.currency', string="Currency",related='invoice_id.currency_id')

    bank_name = fields.Char(string='Bank Name')
    branch = fields.Char(string='Branch')
    account_number = fields.Char(string='Account Number')
    payment_method = fields.Selection([('bank','Bank'),('cash','Cash')], string='Payment Method')

    amount_paid = fields.Monetary(string='Paid Amount')



    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            sequence = self.env['ir.sequence'].next_by_code('pms_transaction_sequence') or '/'
            vals['name'] = sequence
        return super(PmsTransactionLine, self).create(vals)
