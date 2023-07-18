from odoo import fields, models, api, _
from odoo.fields import Command
from odoo.exceptions import UserError, ValidationError

class CreateQuotationPayment(models.TransientModel):
	_name = 'create.quotation.payment'

	@api.model
	def default_get(self, values):
		result = super(CreateQuotationPayment, self).default_get(values)
		quotation_obj = self.env['sale.order'].browse(self._context.get('active_id'))
		result['order_id'] = quotation_obj.id
		result['quotation_total_amount'] = quotation_obj.cio_amount_due
		# result['payment_amount'] = quotation_obj.amount_total

		return result

	order_id = fields.Many2one('sale.order', string='CIO Reference')
	payment_type = fields.Selection([
		('full', 'Full Payment'),
		('partial', 'Partial Payment')
		], string="Payment Type")
	currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
	quotation_total_amount = fields.Monetary('CIO Total Amount', currency_field="currency_id")
	payment_amount = fields.Monetary('Payment Amount', currency_field="currency_id")
	remaining_amount = fields.Monetary('Remaining Amount', currency_field="currency_id")

	@api.onchange('payment_type')
	def onchange_payment_type(self):
		if self.payment_type == 'partial':
			self.payment_amount = 0.00
		elif self.payment_type == 'full':
			self.payment_amount = self.order_id.cio_amount_due
		else:
			self.payment_amount = 0.00

	@api.onchange('payment_amount')
	def onchange_payment_amount(self):
		self.remaining_amount = self.quotation_total_amount - self.payment_amount

	def action_create_quotation_payment(self):
		if self.payment_amount == 0.00:
			raise UserError('Please enter the Payment Amount')
		else:
			if self.order_id.cio_paid_amount == 0.00:
				inv_line = []
				for line in self.order_id.reta_order_line:
					inv_line.append((0,0,{
							'display_type': line.display_type or 'product',
				            'sequence': line.sequence,
				            'name': line.name,
				            'product_id': line.product_id.id,
				            'product_uom_id': line.product_uom.id,
				            'quantity': line.product_uom_qty,
				            'discount': line.discount,
				            'price_unit': line.price_unit,
				            'tax_ids': [Command.set(line.tax_id.ids)],
				            'sale_line_ids': [Command.link(line.id)],
				            'is_downpayment': line.is_downpayment,		            
						}))

				create_values = {
					'ref': self.order_id.client_order_ref or '',
		            'move_type': 'out_invoice',
		            'narration': self.order_id.note,
		            'currency_id': self.order_id.currency_id.id,
		            'campaign_id': self.order_id.campaign_id.id,
		            'medium_id': self.order_id.medium_id.id,
		            'source_id': self.order_id.source_id.id,
		            'team_id': self.order_id.team_id.id,
		            'partner_id': self.order_id.partner_invoice_id.id,
		            'partner_shipping_id': self.order_id.partner_shipping_id.id,
		            'fiscal_position_id': (self.order_id.fiscal_position_id or self.order_id.fiscal_position_id._get_fiscal_position(self.order_id.partner_invoice_id)).id,
		            'invoice_origin': self.order_id.name,
		            'invoice_payment_term_id': self.order_id.payment_term_id.id,
		            'invoice_user_id': self.order_id.user_id.id,
		            'payment_reference': self.order_id.reference,
		            'transaction_ids': [Command.set(self.order_id.transaction_ids.ids)],
		            'company_id': self.order_id.company_id.id,
		            'reta_bool_field': True,
					'invoice_line_ids': inv_line
				}

				new_inv_obj = self.env['account.move'].create(create_values)

				new_inv_obj.action_post()

				payment_values = {
					'payment_type': 'inbound',
					'partner_id': self.order_id.partner_id.id,
					'amount': self.payment_amount,
					'company_id': self.order_id.company_id.id,
					'sale_order_id': self.order_id.id,
				}

				new_payment_obj = self.env['account.payment'].create(payment_values)

				new_payment_obj.action_post()
			else:
				payment_values = {
					'payment_type': 'inbound',
					'partner_id': self.order_id.partner_id.id,
					'amount': self.payment_amount,
					'company_id': self.order_id.company_id.id,
					'sale_order_id': self.order_id.id,
				}

				new_payment_obj = self.env['account.payment'].create(payment_values)

				new_payment_obj.action_post()

			self.order_id.cio_paid_amount += self.payment_amount


		return {'type': 'ir.actions.act_window_close'}