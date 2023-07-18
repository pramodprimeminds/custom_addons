from odoo import api, fields, models, tools, SUPERUSER_ID


class SalesCirculationDashboardData(models.Model):
    _name = 'sales.circulation.dashboard.data'

    @api.model
    def get_display_data(self):
        user = self.env.uid
        user_id = self.env['res.users'].browse(user)
        partner_id = self.env['res.partner'].search([('id', '=', user_id.partner_id.id)])

        # This Code For To Get The Total Returns Copies WithOut Credit
        returns = self.env['contact.report'].search([('agent', '=', user_id.partner_id.id), ('credit_note', '=', False),
                                                    ('stock_picking_return.name', 'ilike', 'RET')])
        total_return = 0.0
        if returns:
            for total_copies in returns:
                if total_copies.total_return:
                    total_return += total_copies.total_return
                else:
                    total_return = 0.0

        # This Code For User To Get For Invoice Total Amount And Total Due Amount
        invoice_obj = self.env['account.move'].search(
            [('partner_id', '=', user_id.partner_id.id), ('internal_order_bool', '=', True),
             ('state', '=', 'posted'), ('move_type', '=', 'out_invoice')])
        total_amount_inv = 0.0
        total_due_amount = 0.0
        for total_amount in invoice_obj:
            if invoice_obj:
                total_amount_inv += total_amount.amount_total
                total_due_amount += total_amount.amount_residual
            else:
                total_amount_inv = 0.0
                total_due_amount = 0.0

        # This Code For User To Get For Deposit amount & Outstanding Amount
        deposits_obj = self.env['account.deposit'].search(
            [('partner_id', '=', user_id.partner_id.id), ('circulation', '=', True), ('status', '=', 'running')])

        deposit_amt = 0.00
        outstanding_amt = 0.00
        for deposits in deposits_obj:
            deposit_amt += deposits.deposit_amt
            outstanding_amt += deposits.total_outstanding

        sale_order_lines = []
        order_lines = self.env['sale.order.line'].search([('agent_user_id', '=', user_id.id)])
        for lines in  order_lines:
            sale_order_lines.append({
                'product_template_id': lines.product_template_id,
                'newspaper_date': lines.newspaper_date
            })
        return {
            'total_indent_copies': partner_id.n_q_zone,
            'returns': total_return,
            'total_amount_inv': total_amount_inv,
            'total_due_amount': total_due_amount,
            'deposit_amt': deposit_amt,
            'outstanding_amt': outstanding_amt,
            'indent_lines': outstanding_amt
        }