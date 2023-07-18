from odoo import api, models, fields, _

class SaleOrderReta(models.Model):
    _inherit = 'sale.order'

    reta_order_line = fields.One2many('sale.order.line','order_id')
    reta_bool_field = fields.Boolean(default=False)
    custom_seq = fields.Char(string='CIO Reference',readonly=True,copy=False,default='New')
    reta_state = fields.Selection(
    selection=[
        ('draft', "CIO"),
        ('sent', "Scheduling"),
        ('waiting_for_approval', "Waiting For Approval"),
        ('sale', "Confirmed"),
        ('print', "Published"),
        ('done', "Locked"),
        ('cancel', "Rejected"),
    ],
    string="Status",
    readonly=True, copy=False, index=True,
    tracking=3,
    default='draft')
    length = fields.Integer(string='Length')
    width = fields.Integer(string='Width')
    custom_sale_seq = fields.Char(string='RO Sequence',readonly=True,copy=False,default='New Sale')
    agent_name = fields.Many2one('res.partner',string='Agent Name')
    reta_agent_user_id = fields.Many2one('res.users',compute='_compute_agent_user_id')

    @api.depends('agent_name')
    def _compute_agent_user_id(self):
        for rec in self:
            if rec.agent_name:
                user_obj = self.env['res.users'].search([('partner_id', '=', rec.agent_name.id)])
                rec.reta_agent_user_id = user_obj.id
            else:
                rec.reta_agent_user_id = None

    @api.model
    def default_get(self, values):
        result = super(SaleOrderReta, self).default_get(values)
        result['agent_name'] = self.env.user.partner_id.id
        result['user_id'] = self.env.user.id

        return result

    def print_button(self):
        self.state = 'print'
        self.reta_state = 'print'

    # def onchange_pricelist(self):

    #     for rec in self:
    #         pricelist = self.env['product.pricelist.item'].search(['product_tmpl_id','=',self.reta_order_line.product_id])
    #         if pricelist:
    #             rec.reta_order_line.length = pricelist.length

    @api.model
    def create(self,vals):
        if vals.get('reta_bool_field'):
            if vals.get('custom_seq', 'New') == 'New':
                vals['custom_seq'] = self.env['ir.sequence'].next_by_code('reta.quotation.sequence') or 'New'

        result = super(SaleOrderReta,self).create(vals)

        return result

    @api.depends('reta_state')
    def _compute_custom_sequence(self):
        for order in self:
            if order.state == 'sale':
                if order.reta_bool_field:
                    sequence = self.env['ir.sequence'].next_by_code('reta.sale.sequence')
                    order.custom_sale_seq = sequence
                else:
                    order.custom_sale_seq = 'New Sale'
            else:
                order.custom_sale_seq = 'New Sale'


    def action_confirm(self):
        result = super(SaleOrderReta, self).action_confirm()
        self._compute_custom_sequence()
        return result

    @api.constrains('state')
    def states_change_reta(self):
        if self.state == 'draft':
            self.reta_state = 'draft'
        elif self.state == 'sent':
            self.reta_state = 'sent'
        elif self.state == 'sale':
            self.reta_state = 'sale'
        elif self.state == 'done':
            self.reta_state = 'done'
        elif self.state == 'cancel':
            self.reta_state = 'cancel'


class RetaOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    pricelist_id = fields.Many2one('product.pricelist.item')
    length = fields.Integer(string='Length',readonly=False)
    width = fields.Integer(string='Width',readonly=False)
    page = fields.Many2one('newspaper.page.details', string='Page No')
    ad_position = fields.Many2one('advertisement.position', string="Position")


    @api.onchange('length', 'width')
    def onchange_length_width(self):
        for qty in self:
            multiply = qty.length * qty.width
            type_multiply = float(multiply)
            qty.product_uom_qty = type_multiply


class ProductPriceListInherit(models.Model):
    _inherit = 'product.pricelist.item'

    length = fields.Integer(string='Length')
    width = fields.Integer(string='Width')


class AccountMoveInheritSale(models.Model):
    _inherit = 'account.move'

    agent_name = fields.Many2one('res.partner', string='Agent Name', readonly=True, compute='compute_agent_name' )
    agent_user_id = fields.Many2one('res.users', string="Agent User Id", compute='compute_agent_user_id')
    reta_bool_field = fields.Boolean(string='Reta Orders')

    def compute_agent_name(self):
        for res in self:
            agent = self.env['sale.order'].search([('name', '=', res.invoice_origin)])
            if agent:
                res.agent_name = agent.agent_name.id
                res.reta_bool_field = agent.reta_bool_field
            if not res.agent_name and res.reta_bool_field:
                continue

    @api.depends('agent_name')
    def compute_agent_user_id(self):
        for rec in self:
            if rec.agent_name:
                agent_user_id = self.env['res.users'].search([('partner_id','=',rec.agent_name.id)],limit=1)
                if agent_user_id:
                    rec.agent_user_id = agent_user_id.id
                else:
                    rec.agent_user_id = None
            else:
                rec.agent_user_id = None
