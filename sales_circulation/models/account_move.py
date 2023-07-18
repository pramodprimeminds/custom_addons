from odoo import fields, api, models
from datetime import datetime, timedelta

import datetime


class SaleOrderInvoice(models.Model):
    _inherit = 'sale.order'

    def action_view_invoice(self):
        res = super(SaleOrderInvoice, self).action_view_invoice()
        invoices = self.mapped('invoice_ids')
        for invoice in invoices:
            if invoice.invoice_origin.startswith('IO') and invoice.invoice_origin == self.name:
                print(invoice.invoice_origin, 'invoicesssss',self.name)
                invoice.write({'internal_order_bool': True})
        return res


class AccountMoveBool(models.Model):
    _inherit = 'account.move'

    internal_order_bool = fields.Boolean('Is Internal order')
    total = fields.Float('Total Copies')
    newsprint_agent = fields.Many2one('res.partner', 'Newsprint Agent')
    ret_ids = fields.Many2many('stock.picking', string='New')

    def action_post(self):
        # res = super(AccountMoveBool, self).action_post()
        agent_report = self.env['contact.report'].search(
            [('agent', '=', self.newsprint_agent.id), ('stock_picking', 'in', self.ret_ids.ids)])
        for rec in agent_report:
            rec.update({
                'credit_note': True,
                'account_move': self.id,

            })
        return super(AccountMoveBool, self).action_post()

    # This Is For Invoice Of Particular Agents(Schedule Action also)
    def creating_agent_invoices(self):
        current_date = fields.Date.today()
        one_month_ago = current_date - timedelta(days=30)
        sale_orders = self.env['sale.order'].search([('internal_order', '=', True),
                                                     ('create_date', '>=', one_month_ago),
                                                     ('create_date', '<=', current_date)])
        agent_list = []
        product_list = []
        for order in sale_orders:
            for line in order.order_line:
                if line.region_s:
                    if line.region_s.id not in agent_list:
                        agent_list.append(line.region_s.id)
                    if line.product_id.id not in product_list:
                        product_list.append(line.product_id.id)

        for agent_id in agent_list:
            total_copies = 0
            invoice_line_list = []
            for product in product_list:
                agent_obj = self.env['res.partner'].browse(agent_id)
                product_obj = self.env['product.product'].browse(product)
                so_line_obj = self.env['sale.order.line'].search([('product_id', '=', product), ('region_s', '=', agent_id)])
                for so_line in so_line_obj:
                    total_copies += so_line.product_uom_qty - agent_obj.f_q_zone + agent_obj.p_q_zone + agent_obj.v_q_zone + agent_obj.pr_q_zone + agent_obj.c_c_zone + agent_obj.o_q_zone
                    so_ids = self.env['sale.order'].search([('order_line', '=', so_line.id)])
                invoice_line = {
                    'product_id': product_obj.id,
                    'quantity': total_copies,
                    'price_unit': product_obj.lst_price,
                    'name': product_obj.name,
                }
                invoice_line_list.append((0, 0, invoice_line))

            invoice_vals = {
                'partner_id': agent_id,
                # 'invoice_date': datetime.today(),
                'internal_order_bool': True,
                'move_type': 'out_invoice',  # Specify the invoice type (out_invoice for customer invoice)
                'invoice_origin': so_ids.name,
                'currency_id': so_ids.currency_id.id,
                'company_id': so_ids.company_id.id,
                'user_id': so_ids.user_id.id,
                'fiscal_position_id': so_ids.fiscal_position_id.id,
                'invoice_payment_term_id': so_ids.payment_term_id.id,
                'line_ids': invoice_line_list,
                # Add other required fields based on your needs
            }

            self.env['account.move'].create(invoice_vals)

        return True
