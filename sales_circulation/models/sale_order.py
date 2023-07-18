from odoo import api, models, fields, _
from datetime import datetime, timedelta

from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    duplicate_order_id = fields.Many2one('sale.order')
    agent_code = fields.Char('Agent Code', related='region_s.agent_code')
    agent_user_id = fields.Many2one('res.users', string="Agent User")

    category_id = fields.Many2one('product.category', string='Category')
    contact_name = fields.Many2one('res.partner', string="Regions")
    printing_unit = fields.Many2one('res.partner', string="Printing Unit")
    newspaper_date = fields.Date('Newspaper Date')  # newsly add
    magazine = fields.Float('Magazine QTY')
    special_Edition = fields.Float('Special Edition QTY')
    ware_locat = fields.Char('Warehouse Location')
    add_new_product_ids = fields.Many2one('add.new.product', ondelete='restrict')
    wc = fields.Many2one('mrp.workcenter', string='Manufacturing Unit')
    invisible_field = fields.Integer()
    region = fields.Char('Region')
    region_s = fields.Many2one('res.partner', 'Agents')
    location_id = fields.Many2one(
        'stock.location', 'Source Location')
    free_copies = fields.Float(string="Free copies")
    agent_copies = fields.Float(string="Agent copies")
    postal_copies = fields.Float(string="Postal copies")
    voucher_copies = fields.Float(string="Voucher copies")
    promotional_copies = fields.Float(string="Promotional copies")
    correspondents_copies = fields.Float(string="Correspondent's copies")
    office_copies = fields.Float(string="Office copies")

    @api.onchange('free_copies','agent_copies','postal_copies','voucher_copies','promotional_copies', 'correspondents_copies', 'office_copies')
    def agents_copies(self):
        self.product_uom_qty = self.free_copies + self.agent_copies + self.postal_copies + self.voucher_copies + self.promotional_copies + self.correspondents_copies + self.office_copies



    @api.constrains('product_id')
    def location_ids(self):
        for rec in self:
            location = rec.product_id.bom_ids.picking_type_id.default_location_src_id.id
            rec.location_id = location

    # to change the delivary qantity of magazin
    @api.onchange('magazine')
    def add_qty_m(self):
        for add in self:
            add.product_uom_qty = add.magazine

    # to change the delivary qantity of the special edition quantity
    @api.onchange('special_Edition')
    def add_qty_s(self):
        for add in self:
            add.product_uom_qty = add.special_Edition

    # depends on warehouse adding product
    @api.onchange('wc')
    def product_wc(self):
        wc = self.env['mrp.workcenter'].search([('name', '=', self.wc.name)])
        for i in wc:
            # print(i.capacity_ids.product_id.name)
            for j in i.capacity_ids:
                print(j.product_id.name)
                self.product_id = j.product_id

        if not self.contact_name:
            self.contact_name = self.order_id.partner_shipping_id

    def _prepare_procurement_values(self, group_id=False):
        res = super(SaleOrderLine, self)._prepare_procurement_values(group_id)
        if self.region_s:
            res.update({'partner_id': self.region_s.id or self.order_id.partner_shipping_id.id or False,
                        'newspaper_date': self.newspaper_date, 'regions': self.region, 'internal_order_delivary': True})
        return res


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _key_assign_picking(self):
        keys = super(StockMove, self)._key_assign_picking()
        return keys + (self.partner_id,)

    def _search_picking_for_assignation(self):
        self.ensure_one()
        picking = super(StockMove, self)._search_picking_for_assignation()
        if self.sale_line_id and self.partner_id:
            picking = picking.filtered(lambda l: l.partner_id.id == self.partner_id.id)
            if picking:
                picking = picking[0]
        return picking


class ProductTemplate(models.Model):
    _inherit = "product.template"

    variant_bom_ids = fields.One2many('mrp.bom', 'product_id', 'BOM Product Variants')
    scrap_location = fields.Many2one('stock.location', 'Scrap Location')


class ProductProductNew(models.Model):
    _inherit = "product.product"

    is_magazine = fields.Boolean('Is Magazine?')
    is_special_edition = fields.Boolean('Is Special Edition?')


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sale_order_duplicating = fields.Boolean('sale order duplicating', default=False)
    order_line_duplicate = fields.One2many('sale.order.line', 'order_id')
    new_seq = fields.Char(string='Internal Order Number', readonly=True, required=True, default='NEW')

    add_new_product = fields.One2many('add.new.product', 'order_id')
    internal_order = fields.Boolean('boolen internal', default=False)

    @api.model
    def create(self, vals_list):
        if vals_list.get('internal_order') == True:
            vals_list['name'] = self.env['ir.sequence'].next_by_code(
                'internal.order') or _("New")
            vals_list['new_seq'] = vals_list['name']

        return super(SaleOrder, self).create(vals_list)

    # def action_sale_order_line_filter_category(self):
    #     domain = [('order_id', '=', self.id)]
    #     view_id = self.env.ref('circulation_new.sale_order_line_view_tree').id
    #     return {
    #         'name': 'Filtered Sale Order Lines',
    #         # 'view_type': 'tree',
    #         'view_id': view_id,
    #         'view_mode': 'tree',
    #         'res_model': 'sale.order.line',
    #         'type': 'ir.actions.act_window',
    #         'domain': domain,
    #         'target': 'new',
    #     }

    # def action_sale_order_line_search_category(self):
    #     domain = [('category_id', '=', self.order_line.category_id.id)]
    #     return {
    #         'name': 'Search Sale Order Lines',
    #         'view_type': 'form',
    #         'view_mode': 'tree,form',
    #         'res_model': 'sale.order.line',
    #         'type': 'ir.actions.act_window',
    #         'domain': domain,
    #     }

    mrp_order_count = fields.Integer(
        compute='_compute_mrp_order_count',
        string='MRP Order Count',
        readonly=True
    )

    def view_mrp_orders(self):
        for res in self.env.user.partner_id.segment_agents.ids:
            rem = self.env['res.users'].browse(res)
            for user in  self.env.user.partner_id.segment_agents.partner_id.segment_agents.ids:
                r = self.env['res.users'].browse(user)
                for user_id in self.env.user.partner_id.segment_agents.partner_id.segment_agents.partner_id.segment_agents.ids:
                    m = self.env['res.users'].browse(user_id)
        action = self.env.ref('mrp.mrp_production_action').read()[0]
        action['domain'] = [('origin', '=', self.name)]
        return action

    @api.depends('name')
    def _compute_mrp_order_count(self):
        self.mrp_order_count = 0
        for order in self:
            order.mrp_order_count = self.env['mrp.production'].search_count([
                ('origin', '=', order.name)
            ])

    state_duplicate = fields.Selection(
        selection=[
            ('draft', "Demand"),
            ('sent', "Demand Sent"),
            ('sale', "Confirmed"),
            ('done', "Locked"),
            ('cancel', "Cancelled"),
        ],
        string="Status",
        readonly=True, copy=False, index=True,
        tracking=3,
        default='draft')

    @api.constrains('state')
    def states_change(self):
        if self.state == 'draft':
            self.state_duplicate = 'draft'
        elif self.state == 'sent':
            self.state_duplicate = 'sent'
        elif self.state == 'sale':
            self.state_duplicate = 'sale'
        elif self.state == 'done':
            self.state_duplicate = 'done'
        elif self.state == 'cancel':
            self.state_duplicate = 'cancel'

    @api.constrains('add_new_product')
    def lines_added(self):
        # By this method values are passing from add_new_product to sale.order.line based and child_ids
        line_ids = []
        for lines in self.add_new_product:
            if lines.check_box == False:
                line_ids.append(lines)
                lines.check_box = True
        for partner in line_ids:
            # partner gives records of add_new_product
            for regions in partner.regions_contact:
                for agent in regions.region_zone:
                    for zones in regions.add_zones_to_line:
                        if agent.cc_zone.name == zones.cc_zone.name:
                            if agent.cc_zone.active_agent == True:
                                if partner.product_id.is_magazine == True:

                                    self.env['sale.order.line'].create({
                                        'printing_unit': partner.partner_id.id,
                                        # 'region': regions.Zone_Name,
                                        'region_s': agent.cc_zone.id,
                                        'prod,uct_id': partner.product_id.id,
                                        'agent_user_id': zones.cc_zone.user_id.id,
                                        # passing values from total no copies to product_qty
                                        'free_copies': zones.Freebee_Quantity_zone,
                                        'agent_copies': zones.newspaper_quantity_zone,
                                        'postal_copies': zones.Postal_copies_zone,
                                        'voucher_copies': zones.voucher_copies_zone,
                                        'promotional_copies': zones.promotional_copies_zone,
                                        'correspondents_copies': zones.corresspondents_copies_zone,
                                        'office_copies': zones.office_copies_zone,
                                        'product_uom_qty': zones.total_copies_zone,
                                        'magazine': zones.total_copies_zone,
                                        'contact_name': regions.id,
                                        # 'contact_name_Duplicate': child.name,
                                        'order_id': self.id,
                                        'add_new_product_ids': partner.id,
                                        'newspaper_date': partner.newspaper_date,  # new 28 apr
                                        # based on this the product_uom_qty field getting hide
                                        'invisible_field': 1,
                                    })
                                elif partner.product_id.is_special_edition == True:
                                    self.env['sale.order.line'].create({
                                        'printing_unit': partner.partner_id.id,
                                        # 'region': regions.Zone_Name,
                                        'region_s': agent.cc_zone.id,
                                        'product_id': partner.product_id.id,
                                        'agent_user_id': zones.cc_zone.user_id.id,
                                        # passing values from total no copies to product_qty
                                        'free_copies': zones.Freebee_Quantity_zone,
                                        'agent_copies': zones.newspaper_quantity_zone,
                                        'postal_copies': zones.Postal_copies_zone,
                                        'voucher_copies': zones.voucher_copies_zone,
                                        'promotional_copies': zones.promotional_copies_zone,
                                        'correspondents_copies': zones.corresspondents_copies_zone,
                                        'office_copies': zones.office_copies_zone,
                                        'product_uom_qty': zones.total_copies_zone,
                                        'special_Edition': zones.total_copies_zone,
                                        'contact_name': regions.id,
                                        # 'contact_name_Duplicate': child.name,
                                        'order_id': self.id,
                                        'add_new_product_ids': partner.id,
                                        'newspaper_date': partner.newspaper_date,  # new 28 apr
                                        # based on this the product_uom_qty field getting hide
                                        'invisible_field': 1,
                                    })
                                else:
                                    self.env['sale.order.line'].create({
                                        'printing_unit': partner.partner_id.id,
                                        # 'region': regions.Zone_Name,
                                        'region_s': agent.cc_zone.id,
                                        'product_id': partner.product_id.id,
                                        'agent_user_id': zones.cc_zone.user_id.id,
                                        # passing values from total no copies to product_qty
                                        'free_copies': zones.Freebee_Quantity_zone,
                                        'agent_copies': zones.newspaper_quantity_zone,
                                        'postal_copies': zones.Postal_copies_zone,
                                        'voucher_copies': zones.voucher_copies_zone,
                                        'promotional_copies': zones.promotional_copies_zone,
                                        'correspondents_copies': zones.corresspondents_copies_zone,
                                        'office_copies': zones.office_copies_zone,
                                        'product_uom_qty': zones.total_copies_zone,
                                        'contact_name': regions.id,
                                        # 'contact_name_Duplicate': child.name,
                                        'order_id': self.id,
                                        'add_new_product_ids': partner.id,
                                        'newspaper_date': partner.newspaper_date,
                                    })

    def create_internal_order(self):
        internal_order = []
        partner_id = self.env['res.partner'].search([('name', '=', 'USHODAYA ENTERPRISES PRIVATE LIMITED')])
        internal_order_vals = {
            'partner_id': partner_id.id,
            'internal_order': True
        }
        internal_order.append(self.env['sale.order'].create(internal_order_vals))
        for rec in internal_order:
            printing_units = self.env['res.partner'].search([('is_printing_unit', '=', True)])
            for units in printing_units:
                product = self.env['product.product'].search([('name', 'ilike', units.name)])
                if product:
                    product_line_vals = {
                        'partner_id': units.id,
                        'newspaper_date': fields.Datetime.now() + timedelta(days=1),
                        'product_id': product.id,
                        'order_id': rec.id,
                    }
                    rec.add_new_product.create(product_line_vals).adding_zone_from_addition()
            rec.lines_added()


class AddNewProduct(models.Model):
    _name = 'add.new.product'

    partner_id = fields.Many2one('res.partner', string="Printing Units", domain=[('is_printing_unit', '=', True)])
    newspaper_date = fields.Date('Newspaper Date')  # newsly add
    product_id = fields.Many2one('product.product', string="Products")
    qty = fields.Float('Number of Copies', compute='total_qty')
    with_ads = fields.Float('With Ads', compute='_compute_ads', readonly=False, store=True)
    without_ads = fields.Float('Without Ads', compute='_compute_ads', readonly=False, store=True)
    check_box = fields.Boolean('State')
    check_box2 = fields.Boolean('State')
    order_id = fields.Many2one('sale.order')
    order_line = fields.Many2one('sale.order.line')
    regions_contact = fields.Many2many('res.partner', 'parent_id_regions',
                                       string='Regions')
    edition_contacts = fields.Many2many('res.partner', 'parent_id_edition', string='Editions')
    district_contacts = fields.Many2many('res.partner', 'parent_id_district', string='Districts')
    mains_contact = fields.Many2many('unit.mains', string='Mains')
    hide_add_m = fields.Boolean(default=False)
    hide_add_s = fields.Boolean(default=False)

    @api.onchange('partner_id')
    def adding_zone_from_addition(self):
        for rec in self:
            zone = []
            edition = []
            district = []
            for additions in rec.partner_id.servie_regions:
                edition.append(additions.id)
                for districts in additions.district_o2m:
                    district.append(districts.id)
                    for zones in districts.zone_o2m:
                        zone.append(zones.id)
            else:
                rec.regions_contact = None
                rec.edition_contacts = None
                rec.district_contacts = None
            rec.regions_contact = zone
            rec.edition_contacts = edition
            rec.district_contacts = district

    @api.constrains('product_id', 'mains_contact')
    @api.onchange('mains_contact')
    def main_no_pages(self):
        total = 0
        for rec in self:
            for no in rec.mains_contact:
                total += no.no_paper_with_ads
            for region_no in rec.regions_contact:
                region_no.no_pages = total

    @api.onchange('partner_id')
    def partner_mains(self):
        partner_id_regions = self.env['res.partner'].search([('name', '=', self.partner_id.name)])
        mains = []
        for regions in partner_id_regions.unit_mains_one2many:
            mains.append(regions.mains_id.id)
        else:
            self.mains_contact = None
        self.mains_contact = mains

    def magazine(self):
        product_id = self.env['product.product'].search([('is_magazine', '=', True)])
        self.create({
            'partner_id': self.partner_id.id,
            'product_id': product_id.id,
            'qty': self.qty,
            'regions_contact': self.regions_contact,
            'newspaper_date': self.newspaper_date,
            'order_id': self.order_id.id,
            'edition_contacts': self.edition_contacts,
            'district_contacts': self.district_contacts,
            'hide_add_m': True
        })
        self.order_id.lines_added()

    def special_edition(self):
        product_id = self.env['product.product'].search([('is_special_edition', '=', True)])

        self.create({
            'partner_id': self.partner_id.id,
            'product_id': product_id.id,
            'qty': self.qty,
            'regions_contact': self.regions_contact,
            'newspaper_date': self.newspaper_date,
            'order_id': self.order_id.id,
            'edition_contacts': self.edition_contacts,
            'district_contacts': self.district_contacts,
            'hide_add_s': True,

        })
        self.order_id.lines_added()

    def free_bee(self):
        self.create({
            'partner_id': self.partner_id.id,
            'product_id': 3,
            'qty': 1.0,
            'order_id': self.order_id.id
        })
        for j in self.partner_id.child_ids:
            parent_partner = self.env['sale.order.line'].search([('contact_name', '=', j.id)])
            for qty in parent_partner:
                qty.free_bee_checkbox = True

    # deleting values from add.new.product to sale.order.line
    @api.model
    def unlink(self):
        for unlinking in self:
            self.env['sale.order.line'].search([('add_new_product_ids', '=', unlinking.id)]).unlink()
        super(AddNewProduct, self).unlink()

    # with_ads and without_ads values update
    @api.onchange('partner_id', 'mains_contact')
    def _compute_ads(self):
        for line in self:
            if len(line.mains_contact) > 1:
                line.with_ads = 0.00
                line.without_ads = 0.00
            else:
                set_qty = self.env['unit.mains'].search([('name', '=', line.mains_contact.name)])
                for ads in set_qty:
                    line.with_ads = ads.no_paper_with_ads
                    line.without_ads = ads.no_paper_without_ads

    # updating the qty based total number qty in sale order line for particular agent added to add.new.product .qty field
    def total_qty(self):
        for i in self:
            sum = 0
            for lines in self.order_id.order_line:
                if i.id == lines.add_new_product_ids.id:
                    sum += lines.product_uom_qty
            i.qty = sum


class StockRuleInherit(models.Model):
    _inherit = 'stock.lot'

    newspaper_date = fields.Date('NewsPaper Date')
    return_date = fields.Float('Return Quantity')
    order_qty = fields.Float(string='Order Quantity', readonly=True)


class DeliveryInheritence(models.Model):
    _inherit = 'stock.rule'

    def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, company_id,
                               values):
        res = super(DeliveryInheritence, self)._get_stock_move_values(product_id, product_qty, product_uom, location_id,
                                                                      name, origin, company_id, values)
        res['newspaper_date'] = values.get('newspaper_date', False)
        return res


class QuotationInherit(models.Model):
    _inherit = 'stock.move'

    newspaper_date = fields.Date(string='Date')
    region = fields.Char('Region')


class StockRegion(models.Model):
    _inherit = 'stock.picking'

    regions = fields.Char('Regions')
    sale_bool = fields.Boolean('sale bool')

    def action_assign(self):
        if self.origin.startswith('IO'):
            for rec in self:
                for line in rec.move_line_ids_without_package:
                    if line.product_id.bom_ids.picking_type_id:
                        location = line.product_id.bom_ids.picking_type_id.default_location_dest_id.id
                        line.location_id = location
                for moves in rec.move_ids_without_package:
                    if moves.product_id.bom_ids.picking_type_id:
                        location = moves.product_id.bom_ids.picking_type_id.default_location_dest_id.id
                        moves.location_id = location
        if self.picking_type_code == 'incoming':
            if self.group_id.name.startswith('IO'):
                for rec in self.move_ids_without_package:
                    if rec.product_id.scrap_location:
                        rec.location_dest_id = rec.product_id.scrap_location.id
        return super(StockRegion, self).action_assign()

    def button_validate(self):
        if self.picking_type_code == 'incoming':
            for rec in self.move_line_ids_without_package:
                lot_number = self.env['stock.lot'].search([('name', '=', rec.lot_id.name)])
                for qty in lot_number:
                    total = qty.return_date + rec.qty_done
                    lot_number.update({
                        'return_date': total
                    })
        super(StockRegion, self).button_validate()


