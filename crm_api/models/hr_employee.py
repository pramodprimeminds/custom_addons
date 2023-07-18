from odoo import models, fields, api
import requests


class HrEmployees(models.Model):
    _name = 'employee.mobile'
    _rec_name = "employee_number"

    employee_number = fields.Char(string="Employee Number")


class EmployeesNumber(models.Model):
    _inherit = 'hr.employee'

    mobile_number_new_ids = fields.Many2many('employee.mobile', string="Employee Mobile Number")

    user_name = fields.Char(string="Tata Telecommunication User Name")
    password = fields.Char(string="Tata Telecommunication Password")
    tata_telecom_access_token = fields.Char(string="Access Token")


    # @api.model
    # def search(self, args, offset=0, limit=None, order=None, count=False):
    #
    #     res_user = self.env['res.users'].search([])
    #     if self._uid and self._uid != 1:
    #         user = self.env['res.users'].browse(self._uid)
    #         restricted_numbers = user.mobile_number_new_ids.ids
    #
    #         if restricted_numbers:
    #             args.append(('employee_number', 'in', restricted_numbers))
    #
    #     return super(EmployeesNumber, self).search(args, offset, limit, order, count)
    #

    def generate_tata_telecommunication_access_token(self):

        employee_obj = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)])
        employee = self.env['hr.employee'].search([])
        for rec in employee:
            if rec.user_name and rec.password:
                token_url = 'https://api-smartflo.tatateleservices.com/v1/auth/login'
                # Request payload
                data = {
                    "email": rec.user_name,
                    "password": rec.password
                }

                # Send POST request to generate access token
                response = requests.post(token_url, data=data)

                if response.status_code == 200:
                    access_token = response.json().get('access_token')
                    rec.tata_telecom_access_token = access_token
                    return access_token
                else:
                    return None
