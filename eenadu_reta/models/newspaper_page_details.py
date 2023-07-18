from odoo import fields, models, api, _


class NewspaperPageDetails(models.Model):
    _name = 'newspaper.page.details'

    name = fields.Integer('Page No')
    length = fields.Integer('Paper Length')
    width = fields.Integer('Paper Width')
    size = fields.Integer('Total Size(Sq.cm)', compute='_compute_paper_size')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
    base_price = fields.Monetary('Amount', currency_field='currency_id')


    @api.depends('length','width')
    def _compute_paper_size(self):
        for rec in self:
            rec.size = rec.length * rec.width