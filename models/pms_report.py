from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class PmsReport(models.TransientModel):
    _name = 'pms.report'
    _description = 'pms report generation'

    model_name = fields.Selection([('pms.property.contract','Booking'),('pms.payment','Invoice'),('pms.transaction.line','Transaction')],string='Select Topic', required=True)

    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)

    def button_search(self):

        table = self.model_name


        booking_obj = self.env[table]
        booking_obj = booking_obj.search([('create_date','>=',self.start_date),('create_date','<=',self.end_date)])
        print('-------wizrd calling------')
        # print(booking_obj)


        if table == 'pms.property.contract':

            data_line =  list()

            total = 0
            for item in booking_obj:

                if item.state == 'confirmed':
                    data_line.append((item.name, item.customer.name, item.order_date, item.expiration_date, item.state, item.total_amount))
                    total = total + item.total_amount
            datas = {

                'start_date':self.start_date,
                'end_date':self.end_date,
                'data_line':data_line,
                'total' : total
            }

            return self.env.ref('property_management_system.action_all_report_booking').report_action([], data= datas)

        if table == 'pms.payment':

            data_line =  list()

            amount_total = 0
            amount_paid = 0
            amount_due = 0


            for item in booking_obj:

                data_line.append((item.name, item.booking_id.name, item.customer_id.name, item.invoice_date, item.payment_state, item.amount_total, item.amount_paid, item.amount_due))
                
                
                
                amount_total = amount_total + item.amount_total
                amount_paid = amount_paid + item.amount_paid
                amount_due = amount_due + item.amount_due

            datas = {

                'start_date':self.start_date,
                'end_date':self.end_date,
                'data_line':data_line,
                'amount_total' : amount_total,
                'amount_paid' : amount_paid,
                'amount_due' : amount_due,

            }

            return self.env.ref('property_management_system.action_all_report_invoice').report_action([], data= datas)

                                        




        if table == 'pms.transaction.line':

            data_line =  list()

            amount_total = 0


            for item in booking_obj:

                data_line.append((item.name, item.booking_id.name, item.customer_id.name, item.invoice_id.name, item.payment_method, item.amount_paid))
                
                amount_total = amount_total + item.amount_paid


            datas = {

                'start_date':self.start_date,
                'end_date':self.end_date,
                'data_line':data_line,
                'amount_total' : amount_total,

            }

            return self.env.ref('property_management_system.action_all_report_transaction').report_action([], data= datas)

                                   


        return {'type': 'ir.actions.act_window_close'}