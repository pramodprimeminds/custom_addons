from odoo import fields, models, api
from twilio.rest import Client
from odoo.exceptions import AccessError, UserError, ValidationError



class SendCustomSMS(models.Model):
    _inherit = 'res.company'

    account_sid = fields.Char(string="Account SID")
    auth_token = fields.Char(string="Authorization Token")
    from_number = fields.Char(string="From Phone Number")

    # def send_custom_sms(self):
    #     account_sid = 'ACe2998376e08ae47f9dca459d7e068b19'
    #     auth_token = '975bb5461383827c5a86cb1411bd4998'
    #     client = Client(account_sid, auth_token)
    #
    #     message = client.messages.create(
    #         from_="+16187871290",
    #         to='+918553837800',
    #         body='Hi How are you'
    #     )
    #
    #     print(message.sid)
    #


class SMSSaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def create(self, vals):
        if vals.get('reta_bool_field'):
            if vals.get('custom_seq', 'New') == 'New':
                vals['custom_seq'] = self.env['ir.sequence'].next_by_code('reta.quotation.sequence') or 'New'

        custom_seq = vals['custom_seq']
        company_name = self.env.user.company_id.name

        print(company_name)
        account_sid = self.env.user.company_id.account_sid
        auth_token = self.env.user.company_id.auth_token
        from_number = self.env.user.company_id.from_number
        amount_total = self.amount_total
        if vals.get('partner_id'):
            partner_obj = self.env['res.partner'].browse(int(vals.get('partner_id')))

        message = "Hi" + " " + partner_obj.name + " " + "here is your CIO " + custom_seq + " " + "from" + " " + company_name + ", amounting in ₹ " + "Please Pay as soon as possible "
        client = Client(account_sid, auth_token)
        # message = client.messages.create(
        #     from_=from_number,
        #     to=partner_obj.mobile,
        #     body='Hi'+ partner_obj.name
        # )
        result = super(SMSSaleOrder, self).create(vals)

        return result

    def action_confirm(self):
        result = super(SMSSaleOrder, self).action_confirm()
        if self.reta_bool_field or self.classified_bool_field:
            if not self.is_terms_and_conditions and not self.is_consent_form:
                raise ValidationError('Please Accept the Consent Form and Terms&conditions')

            account_sid = self.env.user.company_id.account_sid
            auth_token = self.env.user.company_id.auth_token
            from_number = self.env.user.company_id.from_number
            # if vals.get('partner_id'):
            partner_obj = self.env['res.partner'].browse(int(self.partner_id))
            print(partner_obj)

            client = Client(account_sid, auth_token)
            message = client.messages.create(
                from_=from_number,
                to=partner_obj.mobile,
                body='Hi How are you'
            )
            print(message)

        return result
