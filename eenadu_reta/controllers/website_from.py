from odoo import fields, http, _
from odoo.http import request

class WebsiteFormReta(http.Controller):

    @http.route('/reta/cio', type='http', auth="public", website=True)
    def cio_form(self):
        pricelist = request.env['product.pricelist'].search([])
        print(pricelist)
        payment_terms = request.env['account.payment.term'].search([])
        print(payment_terms)
        customer_names = request.env['res.partner'].search([])
        print(customer_names)
        quotation_template = request.env['sale.order.template'].search([])
        print(quotation_template)
        products = request.env['product.template'].search([])
        print(products)
        return http.request.render('eenadu_reta.website_cio_form', {'pricelist': pricelist,"payment_terms": payment_terms,
                                                                    "customer_names": customer_names,"quotation_template": quotation_template,
                                                                    "products": products})

    @http.route('/reta/cio_submitted', type='http', auth="public", website=True)
    def cio_submitted(self, **post):
        values = []
        values.append({
            'agent_name': post.get('agent_name')
        })
        print(values)

        return http.request.render('eenadu_reta.website_cio_form')

