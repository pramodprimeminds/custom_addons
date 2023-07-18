from odoo import fields, models, api, _

class SchedulingPositionDetails(models.Model):
	_name = 'scheduling.position.details'

	scheduling_line_id = fields.Many2one('scheduling.lines', string='Scheduling Line Ref')
	product_id = fields.Many2one('product.product', string="Product")
	name = fields.Char('Description')
	length = fields.Integer('Length')
	width = fields.Integer('Width')
	page = fields.Many2one('newspaper.page.details', string='Page No')
	ad_position = fields.Many2one('advertisement.position', string="Position")
	publish_date = fields.Date('Publish Date', readonly=True)