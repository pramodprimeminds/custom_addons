from odoo import fields, api, models
import requests
import json
import time
from odoo.http import request


class CrmLeadExtension(models.Model):
    _inherit = 'crm.lead'

    agent_number = fields.Many2one('employee.mobile',string="Agent Number")
    mobile_num = fields.Char(string='Customer Number')
    crm_call_logs = fields.Text(string="CRM Call Logs", tracking=True)

    def make_click_to_call(self):
        employee_obj = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)])
        # mob_no = self.env['employee.mobile'].search(['agent_number', '=', self.env.employee_number])
        # print(mob_no,"----------------------------------")
        url = "https://api-smartflo.tatateleservices.com/v1/click_to_call"
        agent_number = self.agent_number.employee_number
        customer_number = self.mobile_num
        payload = {
            "agent_number": agent_number,
            "destination_number": customer_number,
            "caller_id": customer_number,
            "async": 0,
            "custom_identifier": "",
            "get_call_id": 1
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Authorization": employee_obj.tata_telecom_access_token
        }

        response = requests.post(url, json=payload, headers=headers)
        res = response.text

        caller_id = json.loads(res)

        #
        # url = "https://api-smartflo.tatateleservices.com/v1/call/records"
        #
        # result_new = json.loads(requests.get(url, headers=headers).content)
        # new = result_new.get('results')
        # aaa = []
        # for rec in new:
        #     aaa.append({
        #         'call_id': rec.get('call_id'),
        #         # "description": rec.get('description'),
        #         'call_duration': rec.get('call_duration'),
        #         # 'time': rec.get('time'),
        #         'end_stamp': rec.get('end_stamp'),
        #     })
        #
        # message_value = ''
        #
        # for i in aaa:
        #     if str(caller_id['call_id']) == str(i['call_id']) and str(i['end_stamp']):
        #         message_value = 'Call Duration:' + str(i['call_duration'])
        #
        # self.crm_call_logs = message_value
        #



