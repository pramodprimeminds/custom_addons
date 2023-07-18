import datetime

from odoo import fields
from odoo.http import request, root
from odoo.service import security

from odoo.addons.base_rest import restapi
from odoo.addons.component.core import Component
import logging

_logger = logging.getLogger(__name__)


def _rotate_session(httprequest):
    if httprequest.session.rotate:
        root.session_store.delete(httprequest.session)
        httprequest.session.sid = root.session_store.generate_key()
        if httprequest.session.uid:
            httprequest.session.session_token = security.compute_session_token(
                httprequest.session, request.env
            )
        httprequest.session.modified = True


# class PartnerNewApiService(Component):
#     _inherit = "base.rest.service"
#     _name = "partner.new_api.service"
#     _usage = "partner"
#     _collection = "base_rest_auth_user_service.services"
#     _description = """
#         Partner New API Services
#         Services developed with the new api provided by base_rest
#     """
    #
    # @restapi.method([(["/customer_details"], "GET")], auth="public", )
    # def customer_details(self):
    #     customer_det = []
    #     customer_names = self.env['res.partner'].search([])
    #     for i in customer_names:
    #         address = str(i.street if i.street else ' ') + ' ' + str(
    #             i.street2 if i.street2 else ' ') + ' ' + str(
    #             i.city if i.city else ' ') + ' ' + str(
    #             i.country_id.name if i.country_id.name else ' ')
    #         customer_det.append({
    #             'id': i.id,
    #             'name': i.name,
    #             'address': address,
    #             'gst': i.vat,
    #             'pan': i.l10n_in_pan,
    #             'phone': i.phone,
    #             'mobile': i.mobile,
    #             'email': i.email,
    #             'website': i.website,
    #             'title': i.title.name,
    #         })
    #     return customer_det
    #
    # @restapi.method([(["/agent_names"], "GET")], auth="public", )
    # def agent_names(self):
    #     agent_dict = list()
    #     agent_name = self.env['res.partner'].search([('is_newsprint_agent', '=', True)])
    #     for i in agent_name:
    #         agent_dict.append({'id': i.id, 'name': i.name})
    #     return agent_dict
    #
    # @restapi.method([(["/pricelist"], "GET")], auth="public", )
    # def pricelist(self):
    #     price_dict = list()
    #     pricelist = self.env['product.pricelist'].search([])
    #     order_lines = self.env['product.pricelist.item'].search([])
    #     price_order = []
    #     for rec in order_lines:
    #         price_order.append({
    #             'product': rec.product_tmpl_id.name,
    #             'variants': rec.product_id.name,
    #             'minimum quantity': rec.min_quantity,
    #             'length': rec.length,
    #             'width': rec.width,
    #             'price': rec.fixed_price,
    #             'start date': rec.date_start,
    #             'end date': rec.date_end
    #         })
    #
    #     for i in pricelist:
    #         price_dict.append({
    #             'id': i.id,
    #             'pricelist name': i.name,
    #             'order_lines': price_order
    #         })
    #     return price_dict
    #
    # @restapi.method([(["/quotation_template"], "GET")], auth="public", )
    # def quotation_template(self):
    #     pay_dict = list()
    #     quotation_template = self.env['sale.order.template'].search([])
    #     order_lines = self.env['sale.order.template.line'].search([])
    #     order = []
    #     for rec in order_lines:
    #         order.append({
    #             'product name': rec.product_id.name,
    #             'description': rec.name,
    #             'quantity': rec.product_uom_qty,
    #             'unit of measure': rec.product_uom_id.name
    #         })
    #     for i in quotation_template:
    #         pay_dict.append({
    #             'id': i.id,
    #             'name': i.name,
    #             'Quotation expires after': i.number_of_days,
    #             'confirmation mail': i.mail_template_id.name,
    #             'product': order
    #         })
    #     return pay_dict
    #
    # @restapi.method([(["/products"], "GET")], auth="public", )
    # def products(self):
    #     prod_dict = list()
    #     products = self.env['product.template'].search([])
    #     for i in products:
    #         prod_dict.append({
    #             'id': i.id,
    #             "name": i.name,
    #             "unit of measure": i.uom_id.name,
    #             "purchase uom": i.uom_po_id.name,
    #             "sales price": i.list_price,
    #             "customer taxes": i.taxes_id.name,
    #             "cost": i.standard_price,
    #             "product category": i.categ_id.name,
    #             "internal reference": i.default_code,
    #             'hsn/sac code': i.l10n_in_hsn_code,
    #             'hsn/sac description': i.l10n_in_hsn_description,
    #             'barcode': i.barcode,
    #             'product tags': i.product_tag_ids.name
    #         })
    #     return prod_dict
    #
    # @restapi.method([(["/payment_terms"], "GET")], auth="public", )
    # def payment_terms(self):
    #     payment = list()
    #     payment_terms = self.env['account.payment.term'].search([])
    #     for i in payment_terms:
    #         payment.append({
    #             'id': i.id,
    #             'name': i.name})
    #     return payment
    #
    # @restapi.method([(["/unit_of_measure"], "GET")], auth="public", )
    # def unit_of_measure(self):
    #     uom_dict = list()
    #     unit_of_measure = self.env['uom.uom'].search([])
    #     for i in unit_of_measure:
    #         uom_dict.append({
    #             'id': i.id,
    #             'name': i.name,
    #             'category': i.category_id.name,
    #             'Indian GST UQC': i.l10n_in_code,
    #             'type': i.uom_type,
    #             'ration': i.factor,
    #             'rounding': i.rounding
    #         })
    #     return uom_dict
    #
    # @restapi.method([(["/account_deposit"], "GET")], auth="public", )
    # def account_deposit(self):
    #     account_dep = []
    #     account = self.env['account.deposit'].search([])
    #     order_lines = self.env['deposit.outstanding'].search([])
    #     order = []
    #     for rec in order_lines:
    #         order.append({
    #             'period': rec.periodd,
    #             'actual amount': rec.actual_amt,
    #             'interest amount': rec.interest_amt,
    #             'outstanding amount': rec.outstanding_amt
    #         })
    #
    #     for i in account:
    #         account_dep.append({
    #             'id': i.id,
    #             'partner': i.partner_id.name,
    #             'deposit amount': i.deposit_amt,
    #             'interest percentage': i.interest_percent,
    #             'total outstanding': i.total_outstanding,
    #             'partial payment pending': i.remaining_amount_payment,
    #             'order lines': order
    #         })
    #     return account_dep
    #
    # @restapi.method([(["/advertisement_position"], "GET")], auth="public", )
    # def advertisement_position(self):
    #     advt = []
    #     advertisement = self.env['advertisement.position'].search([])
    #     for i in advertisement:
    #         advt.append({
    #             'id': i.id,
    #             'name': i.name})
    #     return advt
    #
    # @restapi.method([(["/sale_document"], "GET")], auth="public", )
    # def sale_document(self):
    #     sale = []
    #     sale_document = self.env['sale.document.type'].search([])
    #     for i in sale_document:
    #         sale.append({
    #             'id': i.id,
    #             'name': i.name})
    #     return sale
    #
    # @restapi.method([(["/reta_target_scheme"], "GET")], auth="public", )
    # def reta_target_scheme(self):
    #     scheme = []
    #     line_order = []
    #     target_scheme = self.env['target.scheme'].search([])
    #     target_scheme_line = self.env['target.scheme.line'].search([])
    #     for rec in target_scheme_line:
    #         line_order.append({
    #             'product': rec.product_id.name,
    #             'unit of measure': rec.product_uom_id.name
    #         })
    #
    #     for i in target_scheme:
    #         scheme.append({
    #             'id': i.id,
    #             'Scheme Name': i.name,
    #             'order line': line_order})
    #     return scheme

    # @restapi.method([(["/reta_agents_target"], "GET")], auth="public", )
    # def reta_agents_target(self):
    #     target = []
    #     line_order = []
    #     target_scheme = self.env['sales.person.target'].search([])
    #     target_scheme_line = self.env['product.target.line'].search([])
    #     for rec in target_scheme_line:
    #         line_order.append({
    #             'product': rec.product_id.name,
    #             'target amount': rec.target_amount,
    #             'achieved amount': rec.achieved_amount,
    #             'to be achieved': rec.to_be_achieved
    #         })
    #
    #     for i in target_scheme:
    #         target.append({
    #             'id': i.id,
    #             'agent': i.partner_id.name,
    #             'scheme': i.target_scheme_id.name,
    #             'order_lines': line_order})
    #     return target
    #
    # @restapi.method([(["/taxes"], "GET")], auth="public", )
    # def taxes(self):
    #     tax_dict = list()
    #     tax_id = self.env['account.tax'].search([])
    #     order_lines = self.env['account.tax'].search([])
    #     order = []
    #     for rec in order_lines:
    #         order.append({
    #             'tax name': rec.name,
    #             'tax computation': rec.amount_type,
    #             'amount': rec.amount
    #         })
    #     for i in tax_id:
    #         tax_dict.append({
    #             'id': i.id,
    #             'tax name': i.name,
    #             'tax computation': i.amount_type,
    #             'tax type': i.type_tax_use,
    #             'tax scope': i.tax_scope,
    #             'order lines': order})
    #     return tax_dict

    # @restapi.method([(["/create_quotations"], "POST")], auth="user", )
    # def create_quotations(self):
    #     params = request.params
    #     cust_id = self.env['res.partner'].search([('name', '=', params.get('partner_id'))])
    #     pricelist = self.env['product.pricelist'].sudo().search([('name', "=", params.get('pricelist_id'))])
    #     payment_terms = self.env['account.payment.term'].search([('name', '=', params.get('payment_term_id'))])
    #     agent_name = self.env['res.partner'].search([('name', '=', params.get('agent_name'))])
    #
    #     order_line_vals = params.get('reta_order_line')
    #     cust_order_line = list()
    #     scheduling_date = ""
    #     l10n_in_gst_treatment = ""
    #     if params.get('scheduling_date') == 'Specific Date':
    #         scheduling_date += 'specific_date'
    #     else:
    #         scheduling_date += 'multiple_date'
    #
    #     # print(params.get('l10n_in_gst_treatment'),"================================================================")
    #     # # if params.get('l10n_in_gst_treatment') == 'Registered Business - Regular':
    #     # #     l10n_in_gst_treatment += 'regular'
    #     # if params.get('l10n_in_gst_treatment') == 'Registered Business - Composition':
    #     #     l10n_in_gst_treatment += 'composition'
    #     # elif params.get('l10n_in_gst_treatment') == 'Unregistered Business':
    #     #     l10n_in_gst_treatment += 'unregistered'
    #     # elif params.get('l10n_in_gst_treatment') == 'Consumer':
    #     #     l10n_in_gst_treatment += 'consumer'
    #     # elif params.get('l10n_in_gst_treatment') == 'Overseas':
    #     #     l10n_in_gst_treatment += 'overseas'
    #     # elif params.get('l10n_in_gst_treatment') == 'Special Economic Zone':
    #     #     l10n_in_gst_treatment += 'special_economic_zone'
    #     # elif params.get('l10n_in_gst_treatment') == 'Deemed Export':
    #     #     l10n_in_gst_treatment += 'deemed_export'
    #     # else:
    #     #     l10n_in_gst_treatment += 'uin_holders'
    #     #
    #     # print(l10n_in_gst_treatment,"--------------------------------------------------------")
    #
    #     quotation_template = self.env['sale.order.template'].search(
    #         [('name', '=', params.get('sale_order_template_id'))])
    #     for rec in order_line_vals:
    #         product = self.env['product.product'].sudo().search([('name', '=', rec['product_id'])])
    #         tax_id = self.env['account.tax'].search([('name', '=', rec['tax_id']), ('type_tax_use', '=', 'sale')])
    #         length = rec['length']
    #         width = rec['width']
    #         discount = rec['discount']
    #         product_uom_qty = rec['product_uom_qty']
    #         cust_order_line.append((0, 0, {
    #             'product_id': product.id,
    #             'length': length,
    #             'width': width,
    #             'product_uom_qty': product_uom_qty,
    #             "price_unit": product.uom_id.id,
    #             'tax_id': tax_id,
    #             'discount': discount,
    #         }))
    #     customer_val = {
    #         'reta_bool_field': True,
    #         'partner_id': cust_id.id,
    #         'agent_name': agent_name.id,
    #         'validity_date': params.get('validity_date'),
    #         # 'l10n_in_gst_treatment': l10n_in_gst_treatment,
    #         'payment_term_id': payment_terms.id,
    #         'sale_order_template_id': quotation_template.id,
    #         'reta_order_line': cust_order_line,
    #         'scheduling_date': scheduling_date,
    #         'from_date': params.get('from_date'),
    #         'to_date': params.get('to_date'),
    #         'publish_start_date': params.get('publish_start_date'),
    #         'no_of_occurence': params.get('no_of_occurence'),
    #         'time_interval': params.get('time_interval'),
    #         'pricelist_id': int(pricelist),
    #         'mob_seq_number': params.get('mob_seq_number'),
    #         'mob_seq_id': params.get('mob_seq_id')
    #     }
    #     print(customer_val,"000000000000000000000000000000000000000")
    #     quotation_obj = self.env['sale.order'].search(
    #         [('mob_seq_number', '=', params.get('mob_seq_number')), ('mob_seq_id', '=', params.get('mob_seq_id'))])
    #     if quotation_obj:
    #         return {
    #             'Status': "Record already Created!",
    #             'CIO Reference': quotation_obj.custom_seq,
    #             'id': quotation_obj.id
    #         }
    #     else:
    #         quotation = self.env['sale.order'].create(customer_val)
    #
    #         return {"id": quotation.id, "Status": "Success", "CIO Reference": quotation.custom_seq,
    #                 "Number": quotation.name}
    #
    # @restapi.method([(["/create_customer"], "POST")], auth="user", )
    # def create_customer(self):
    #     params = request.params
    #     user_id = self.env.user
    #     state = self.env['res.country.state'].search([('name', '=', params.get('state_id'))])
    #     district = self.env['res.state.district'].search([('name', '=', params.get('district_id'))])
    #     country = self.env['res.country'].search([('name', '=', params.get('country_id'))])
    #     team = self.env['crm.team'].search([('name', '=', params.get('team_id'))])
    #     payment_terms = self.env['account.payment.term'].search([('name', '=', params.get('property_payment_term_id'))])
    #
    #     company_type = ""
    #     if params.get('company_type') == 'Individual':
    #         company_type += 'person'
    #     elif params.get('company_type') == 'Company':
    #         company_type += 'company'
    #     l10n_in_gst_treatment = ""
    #     if params.get('l10n_in_gst_treatment') == 'Registered Business - Regular':
    #         l10n_in_gst_treatment += 'regular'
    #     if params.get('l10n_in_gst_treatment') == 'Registered Business - Composition':
    #         l10n_in_gst_treatment += 'composition'
    #     elif params.get('l10n_in_gst_treatment') == 'Unregistered Business':
    #         l10n_in_gst_treatment += 'unregistered'
    #     elif params.get('l10n_in_gst_treatment') == 'Consumer':
    #         l10n_in_gst_treatment += 'consumer'
    #     elif params.get('l10n_in_gst_treatment') == 'Overseas':
    #         l10n_in_gst_treatment += 'overseas'
    #     elif params.get('l10n_in_gst_treatment') == 'Special Economic Zone':
    #         l10n_in_gst_treatment += 'special_economic_zone'
    #     elif params.get('l10n_in_gst_treatment') == 'Deemed Export':
    #         l10n_in_gst_treatment += 'deemed_export'
    #     else:
    #         l10n_in_gst_treatment += 'uin_holders'
    #
    #     customer_list = {
    #         'company_type': company_type,
    #         'name': params.get('name'),
    #         'l10n_in_gst_treatment': l10n_in_gst_treatment,
    #         'street': params.get('street'),
    #         'street2': params.get('street2'),
    #         'city': params.get('city'),
    #         'district_id': district.id,
    #         'state_id': state.id,
    #         'country_id': country.id,
    #         'zip': params.get('zip'),
    #         'l10n_in_pan': params.get('l10n_in_pan'),
    #         'phone': params.get('phone'),
    #         'mobile': params.get('mobile'),
    #         'email': params.get('email'),
    #         'website': params.get('website'),
    #         'vat': params.get('vat'),
    #         'pan_number': params.get('pan_number'),
    #         'user_id': user_id.id,
    #         'team_id': team.id,
    #         'property_payment_term_id':payment_terms.id
    #     }
    #     customer = self.env['res.partner'].create(customer_list)
    #     return {"id": customer.id,
    #             "Status": "Success"}
    #
    # @restapi.method([(["/sale_order_history"], "GET")], auth="user", )
    # def sale_order_history(self):
    #     current_user = request.session.uid
    #     sale_orders = self.env['sale.order'].search([])
    #     customer_det = []
    #     if current_user:
    #         for i in sale_orders:
    #             customer_det.append({
    #                 'id': i.id,
    #                 'name': i.partner_id.name,
    #                 'sale_order': i.custom_sale_seq,
    #                 'quotation': i.custom_seq
    #             })
    #     return customer_det
    #
    # @restapi.method([(["/update_customer"], "PATCH")], auth="public", )
    # def update_customer(self):
    #     params = request.params
    #     record_id = self.env['res.partner'].search([('id', "=",  params.get('id'))])
    #     state = self.env['res.country.state'].search([('name', '=', params.get('state_id'))])
    #     district = self.env['res.state.district'].search([('name', '=', params.get('district_id'))])
    #     country = self.env['res.country'].search([('name', '=', params.get('country_id'))])
    #     team = self.env['crm.team'].search([('name', '=', params.get('team_id'))])
    #     payment_terms = self.env['account.payment.term'].search([('name', '=', params.get('property_payment_term_id'))])
    #     company_type = ""
    #     if params.get('company_type') == 'Individual':
    #         company_type += 'person'
    #     elif params.get('company_type') == 'Company':
    #         company_type += 'company'
    #     l10n_in_gst_treatment = ""
    #     if params.get('l10n_in_gst_treatment') == 'Registered Business - Regular':
    #         l10n_in_gst_treatment += 'regular'
    #     if params.get('l10n_in_gst_treatment') == 'Registered Business - Composition':
    #         l10n_in_gst_treatment += 'composition'
    #     elif params.get('l10n_in_gst_treatment') == 'Unregistered Business':
    #         l10n_in_gst_treatment += 'unregistered'
    #     elif params.get('l10n_in_gst_treatment') == 'Consumer':
    #         l10n_in_gst_treatment += 'consumer'
    #     elif params.get('l10n_in_gst_treatment') == 'Overseas':
    #         l10n_in_gst_treatment += 'overseas'
    #     elif params.get('l10n_in_gst_treatment') == 'Special Economic Zone':
    #         l10n_in_gst_treatment += 'special_economic_zone'
    #     elif params.get('l10n_in_gst_treatment') == 'Deemed Export':
    #         l10n_in_gst_treatment += 'deemed_export'
    #     else:
    #         l10n_in_gst_treatment += 'uin_holders'
    #
    #     record_id.company_type = company_type
    #     record_id.name = params.get('name')
    #     record_id.l10n_in_gst_treatment = l10n_in_gst_treatment
    #     record_id.street = params.get('street')
    #     record_id.street2 = params.get('street2')
    #     record_id.city = params.get('city')
    #     record_id.district_id = district.id
    #     record_id.state_id = state.id
    #     record_id.country_id = country.id
    #     record_id.zip = params.get('zip')
    #     record_id.l10n_in_pan = params.get('l10n_in_pan')
    #     record_id.phone = params.get('phone')
    #     record_id.mobile = params.get('mobile')
    #     record_id.email = params.get('email')
    #     record_id.website = params.get('website')
    #     record_id.vat = params.get('vat')
    #     record_id.pan_number = params.get('pan_number')
    #     record_id.team_id = team.id,
    #     record_id.property_payment_term_id = payment_terms.id,
    #
    #     return {"Status": "Details Updated successfully"}
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    # @restapi.method([(["/job_applications"], "POST")], auth="public", )
    # def job_applications(self):
    #     params = request.params
    #     degree = self.env['hr.recruitment.degree'].search([('name', '=', params.get('type_id'))])
    #     job_id = self.env['hr.job'].search([('name', '=', params.get('job_id'))])
    #     title = ""
    #     if params.get('title') == 'Dr':
    #         title += 'dr'
    #     elif params.get('title') == 'Ms':
    #         title += 'ms'
    #     elif params.get('title') == 'Mrs':
    #         title += 'mrs'
    #     else:
    #         title += 'mrs'
    #     Attachments = request.env['ir.attachment']
    #     att_bin = params['attachement_id1']
    #     attachment_id = Attachments.sudo().create({
    #         'name': params.get('name') + ' ' + 'resume',
    #         # 'res_name': 'name',
    #         'type': 'binary',
    #         'res_model': 'hr.applicant',
    #         'public': True,
    #         'datas': att_bin,
    #     })
    #     candidate_list = {
    #         'name': params.get('name'),
    #         'title': title,
    #         'partner_name': params.get('partner_name'),
    #         'email_from': params.get('email_from'),
    #         'location': params.get('location'),
    #         'partner_mobile': params.get('partner_mobile'),
    #         'job_id': job_id.id,
    #         'type_id': degree.id,
    #         'attachement_id1': attachment_id,
    #     }
    #     job = self.env['hr.applicant'].sudo().create(candidate_list)
    #     return {"Status": "Success", "id": job.id}
    #
    # @restapi.method([(["/job_positions"], "GET")], auth="public", )
    # def job_positions(self):
    #     position_list = []
    #     positions = self.env['hr.job'].search([])
    #     for i in positions:
    #         address = str(i.address_id.street if i.address_id.street else ' ') + ' ' + str(
    #             i.address_id.street2 if i.address_id.street2 else ' ') + ' ' + str(
    #             i.address_id.city if i.address_id.city else ' ') + ' ' + str(
    #             i.address_id.country_id.name if i.address_id.country_id.name else ' ')
    #     for pos in positions:
    #         position_list.append({
    #             'id': pos.id,
    #             'job position': pos.name,
    #             'department': pos.department_id.name,
    #             'company name': pos.address_id.name,
    #             'job location': address,
    #             'number of openings': pos.no_of_recruitment,
    #             'website published': pos.website_published,
    #             'recruiter': pos.user_id.name,
    #             # 'interviewers': pos.interviewer_ids.id
    #         })
    #     return {"Job Position": position_list}
    #
    #
    #
    #
    #



class SessionAuthenticationService(Component):
    _inherit = "base.rest.service"
    _name = "session.authenticate.service"
    _usage = "auth"
    _collection = "session.rest.services"

    @restapi.method([(["/login"], "POST")], auth="public")
    def authenticate(self):
        params = request.params
        # db_name = params.get("db", db_monodb())
        values ={}
        user_id = self.env.user
        request.session.authenticate(params["db"], params["login"], params["password"])
        result = request.env["ir.http"].session_info()
        # avoid to rotate the session outside of the scope of this method
        # to ensure that the session ID does not change after this method
        _rotate_session(request)
        request.session.rotate = False
        expiration = datetime.datetime.utcnow() + datetime.timedelta(days=90)
        result["session"] = {
            "sid": request.session.sid,
            "expires_at": fields.Datetime.to_string(expiration),
        }
        user_id = self.env['res.users'].search([('id', '=', int(user_id))])

        reta_order_cio_obj = self.env['sale.order'].search(
            [('reta_agent_user_id', '=', user_id.id), ('reta_bool_field', '=', True), ('reta_state', '=', 'draft')])
        reta_order_scheduling_obj = self.env['sale.order'].search(
            [('reta_agent_user_id', '=', user_id.id), ('reta_bool_field', '=', True), ('reta_state', '=', 'sent')])
        reta_order_waiting_for_approval_obj = self.env['sale.order'].search(
            [('reta_agent_user_id', '=', user_id.id), ('reta_bool_field', '=', True),
             ('reta_state', '=', 'waiting_for_approval')])
        reta_order_ro_obj = self.env['sale.order'].search(
            [('reta_agent_user_id', '=', user_id.id), ('reta_bool_field', '=', True), ('reta_state', '=', 'sale')])
        invoice_obj = self.env['account.move'].search(
            [('agent_name', '=', user_id.partner_id.id), ('reta_bool_field', '=', True)])
        deposits_obj = self.env['account.deposit'].search(
            [('partner_id', '=', user_id.partner_id.id), ('reta', '=', True), ('status', '=', 'running')])

        target_obj = self.env['sales.person.target'].search(
            [('partner_id', '=', user_id.partner_id.id), ('is_reta_target', '=', True)])

        commission_obj = self.env['commission.settlement'].search([('agent_id', '=', user_id.partner_id.id)])

        deposit_amt = 0.00
        outstanding_amt = 0.00
        for deposits in deposits_obj:
            deposit_amt += deposits.deposit_amt
            outstanding_amt += deposits.total_outstanding

        target_lines = []

        for target in target_obj:
            for target_line in target.product_target_line_ids:
                if target_line.product_id.product_template_attribute_value_ids:
                    product_name = str(target_line.product_id.name) + ' (' + str(
                        target_line.product_id.product_template_attribute_value_ids.name) + ')'
                else:
                    product_name = str(target_line.product_id.name)
                target_lines.append({
                    'product_id': product_name,
                    'target_amount': target_line.target_amount,
                    'achieved_amount': target_line.achieved_amount,
                    'to_be_achieved': target_line.to_be_achieved
                })

        total_payment_received = 0.00
        total_commission_received = 0.00
        for commission in commission_obj:
            for line in commission.reta_order:
                total_payment_received += line.amount_paid
                total_commission_received += line.commission

        dashboard_display_vals = {
            'user': user_id.name,
            'cio': len(reta_order_cio_obj),
            'scheduling': len(reta_order_scheduling_obj),
            'waiting_for_approval': len(reta_order_waiting_for_approval_obj),
            'release_orders': len(reta_order_ro_obj),
            'invoices': len(invoice_obj),
            'deposit_amt': deposit_amt,
            'outstanding_amt': outstanding_amt,
            'total_payment_received': total_payment_received,
            'total_commission_received': total_commission_received,
            'target_lines': target_lines
        }
        values.update({
            'result': result,
            'dashboard': dashboard_display_vals
        })
        return values

    @restapi.method([(["/logout"], "POST")], auth="user")
    def logout(self):
        request.session.logout(keep_db=True)
        return {"message": "Successful logout"}

