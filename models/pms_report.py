from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class PmsReport(models.TransientModel):
    _name = 'pms.report'
    _description = 'pms report generation'

    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')

    def button_search(self):


        booking_obj = self.env['pms.property.contract']
        booking_obj = booking_obj.search([('start_date','>=',self.start_date),('start_date','<=',self.end_date)])
        print('-------wizrd calling------')
        print(booking_obj)
        return {'type': 'ir.actions.act_window_close'}