# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
#from odoo import models
from odoo import api, fields, models, tools, SUPERUSER_ID


class RetaDashboard(models.Model):
    _name = 'reta.dashboard.data'

    def get_display_data(self, user_id):
        user_id = self.env['res.users'].search([('id', '=', int(user_id))])

        reta_order_cio_obj = self.env['sale.order'].search([('reta_agent_user_id', '=', user_id.id),('reta_bool_field', '=', True),('reta_state', '=', 'draft')])
        reta_order_scheduling_obj = self.env['sale.order'].search([('reta_agent_user_id', '=', user_id.id),('reta_bool_field', '=', True),('reta_state', '=', 'sent')])
        reta_order_waiting_for_approval_obj = self.env['sale.order'].search([('reta_agent_user_id', '=', user_id.id),('reta_bool_field', '=', True),('reta_state', '=', 'waiting_for_approval')])
        reta_order_ro_obj = self.env['sale.order'].search([('reta_agent_user_id', '=', user_id.id),('reta_bool_field', '=', True),('reta_state', '=', 'sale')])
        invoice_obj = self.env['account.move'].search([('agent_name', '=', user_id.partner_id.id),('reta_bool_field', '=', True)])
        deposits_obj = self.env['account.deposit'].search([('partner_id', '=', user_id.partner_id.id),('reta', '=', True),('status', '=', 'running')])

        target_obj = self.env['sales.person.target'].search([('partner_id', '=', user_id.partner_id.id),('is_reta_target', '=', True)])

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
                    product_name = str(target_line.product_id.name)+' ('+str(target_line.product_id.product_template_attribute_value_ids.name)+')'
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
            'user':user_id.name,
            'cio':len(reta_order_cio_obj),
            'scheduling':len(reta_order_scheduling_obj),
            'waiting_for_approval':len(reta_order_waiting_for_approval_obj),
            'release_orders':len(reta_order_ro_obj),
            'invoices':len(invoice_obj),
            'deposit_amt':deposit_amt,
            'outstanding_amt':outstanding_amt,
            'total_payment_received':total_payment_received,
            'total_commission_received':total_commission_received,
            'target_lines': target_lines
        }

        return dashboard_display_vals