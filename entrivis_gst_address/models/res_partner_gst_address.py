from odoo import fields, api, models
from odoo.exceptions import UserError
import json
import requests
import datetime


class ResPartner(models.Model):
    _inherit = 'res.partner'

    gst_verified = fields.Boolean(string="GST Verified", default=False, readonly=True)
    gst_status = fields.Char(string="GST Status", readonly=True)
    current_date = fields.Char(reaonly=True, string="", readonly=True)

    def fetch_address(self):
        asp_id = self.env.user.company_id.aspid
        pwd = self.env.user.company_id.password
        for rec in self:
            if rec.vat:
                url = 'https://gstapi.charteredinfo.com/commonapi/v1.1/search?aspid='+str(asp_id)+'&password='+str(pwd)+'$&Action=TP&Gstin=' + str(
                    rec.vat)
                current_date_time = datetime.datetime.now()
                formatted_date_time = current_date_time.strftime("%Y-%m-%d %H:%M:%S")
                result = json.loads(requests.get(url).content)
                tax = result.get('pradr', False)
                address = tax.get('addr')
                pincode = address.get('pncd', False)
                temp_street = address.get('flno', False) + "," + address.get('bno')
                state = self.env['res.country.state'].search([('name', '=', address.get('stcd'))])
                district = self.env['res.state.district'].search([('name', '=', address.get('dst'))])
                trade_name = result.get('tradeNam')
                city = address.get('st', False) + "," + address.get('loc')
                status = result.get('sts')

                if status == "Active":
                    rec.write({
                        'company_name': trade_name,
                        'street': temp_street,
                        'street2': address.get('st', False),
                        'city': city,
                        "district_id": district.id,
                        'state_id': state,
                        'zip': pincode,
                        'country_id': self.env.ref('base.in').id,
                        'gst_verified': True,
                        'gst_status': result.get('sts'),
                        'current_date': formatted_date_time

                    })
                else:
                    rec.write({
                        'company_name': trade_name,
                        'street': temp_street,
                        'street2': address.get('st', False),
                        'city': city,
                        "district_id": district.id,
                        'state_id': state,
                        'zip': pincode,
                        'country_id': self.env.ref('base.in').id,
                        'gst_status': result.get('sts'),
                        'current_date': formatted_date_time

                    })


@api.onchange('vat')
def onchange_gst_verified(self):
    for rec in self:
        if rec.vat:
            rec.gst_verified = False


class ResCompany(models.Model):
    _inherit = 'res.company'

    aspid = fields.Char(string="ASP ID")
    password = fields.Char(string="Password")


