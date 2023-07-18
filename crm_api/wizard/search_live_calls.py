from odoo import fields, models, api
import requests
import json


class SearchLiveCalls(models.TransientModel):
    _name = 'live.calls.wizard'
    _description = 'Live Calls Wizard'

    live_calls = fields.Char(string="Live Calls")
    customer_number = fields.Char(string="Customer Number")
    customer_name = fields.Char(string="Customer Name")

    def search_live_calls_new(self):
        employee_obj = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)])
        url = "https://api-smartflo.tatateleservices.com/v1/live_calls"
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": employee_obj.tata_telecom_access_token
        }
        result = json.loads(requests.get(url, headers=headers).content)
        live_calls_dict = ''
        for calls in result:
            live_calls_dict = calls.get('customer_number')

        print(live_calls_dict,'-----live_calls_dict------')

        cust_name = self.env['crm.lead'].search([('mobile_num', "=", str(live_calls_dict))])
        print(cust_name)

        ctx = ({
            # 'default_customer_number': cust_name.mobile_num,
            'default_customer_number': "123456789",
            # 'default_customer_name': cust_name.name
            'default_customer_name': "aaaaaaa"
        })
        print(ctx)

        return {
            'view_mode': 'form',
            'view_id': False,
            'res_model': self._name,
            'domain': [],
            'context': ctx,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
