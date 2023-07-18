from odoo import fields, models, api, _
import math
from odoo.exceptions import AccessError, UserError, ValidationError
from datetime import datetime, timedelta


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    advertisement_line_ids = fields.One2many('advertisement.content.line', 'advertisement_line_id', string="Advertisement line ref")
    advertisement_language = fields.Selection([
        ('telugu','Telugu'),
        ('english','English')
        ], string="Advertisement Language", default='telugu')

    scheduling_line_ids = fields.One2many('scheduling.lines', 'scheduling_line_id', string="Scheduling Lines ref")
    is_schedule_done = fields.Boolean('Is Schedule Done?', default=False, compute="compute_done_schedule")
    scheduling_date = fields.Selection([
        ('specific_date','Specific Date'),
        ('multiple_date','Multiple Date')], string="Publish Type")
    specific_date = fields.Date('Specific Date')
    from_date = fields.Date('From Date')
    to_date = fields.Date('To Date')
    publish_start_date = fields.Date('Publish Start Date')
    no_of_occurence = fields.Integer('Number Of Occurance')
    time_interval = fields.Integer('Time Interval')

    sale_related_document_ids = fields.One2many('sale.related.documents', 'sale_related_document_id', string='Related Documents lines ref')

    is_terms_and_conditions = fields.Boolean('Accept Terms and conditions')
    is_consent_form = fields.Boolean('Accept Consent')

    cio_paid_amount = fields.Monetary('Amount Paid', currency_field='currency_id')
    cio_amount_due = fields.Monetary('Amount Due', currency_field='currency_id', compute="_compute_cio_amount_due")

    is_fully_paid = fields.Boolean('Is CIO Paid?', compute='_compute_is_cio_paid')

    cio_payment_count = fields.Integer('Payment Count', compute='_compute_payemnt_count')

    def _compute_payemnt_count(self):
        for rec in self:
            account_payment_obj = self.env['account.payment'].search([('sale_order_id', '=', rec.id)])

            rec.cio_payment_count = len(account_payment_obj)

    @api.depends('cio_paid_amount','amount_total')
    def _compute_cio_amount_due(self):
        for rec in self:
            rec.cio_amount_due = rec.amount_total - rec.cio_paid_amount

    @api.depends('cio_amount_due')
    def _compute_is_cio_paid(self):
        for rec in self:
            if rec.cio_amount_due == 0.00:
                rec.is_fully_paid = True
            else:
                rec.is_fully_paid = False


    @api.depends('scheduling_line_ids')
    def compute_done_schedule(self):
        for rec in self:
            if self.scheduling_line_ids:
                i = 0
                for line in rec.scheduling_line_ids:
                    if line.scheduling_status:
                        i += 1
                    else:
                        i = i
                if len(rec.scheduling_line_ids) == i:
                    rec.is_schedule_done = True
                else:
                    rec.is_schedule_done = False
            else:
                rec.is_schedule_done = False

    def action_confirm(self):
        result = super(SaleOrder, self).action_confirm()

        if self.reta_bool_field or self.classified_bool_field:
            if not self.is_terms_and_conditions and not self.is_consent_form:
                raise ValidationError('Please Accept the Consent Form and Terms&conditions')

        return result

    def open_consent_form(self):
        return

    def add_order_line(self):
        for line in self.advertisement_line_ids:
            product_line = []
            product_id = self.env['product.product'].search([('name', '=', 'Advertisement Line')])
            product_present = False
            for order_line in self.order_line:
                if order_line.product_id.id == product_id.id:
                    product_present = True
            if product_present == True:
                sale_order_line_obj = self.env['sale.order.line'].search([('product_id', '=', product_id.id),('order_id', '=', self.id)],limit=1)
                sale_order_line_obj.product_uom_qty = line.no_of_lines
            else:
                product_line.append((0, 0, {
                    'product_id': product_id.id,
                    'name': line.advertisement_description,
                    'product_uom_qty': line.no_of_lines,
                    'price_unit': product_id.list_price,
                    'product_uom': product_id.uom_id.id,
                    'order_id': self.id,
                }))
                self.order_line = product_line

    def send_for_scheduling(self):
        scheduling_line = []
        if self.reta_bool_field:
            for line in self.reta_order_line:
                if self.scheduling_date == 'specific_date':
                    scheduling_line.append((0,0, {
                            'product_id': line.product_id.id,
                            'name': line.name,
                            'length': line.length,
                            'width': line.width,
                            'page_no': line.page.id,
                            'ad_position': line.ad_position.id,
                            'publish_date': self.specific_date,
                        }))
                else:
                    for i in range(0,self.no_of_occurence):
                        if i == 0:
                            scheduling_line.append((0,0, {
                                    'product_id': line.product_id.id,
                                    'name': line.name,
                                    'length': line.length,
                                    'width': line.width,
                                    'page_no': line.page.id,
                                    'ad_position': line.ad_position.id,
                                    'publish_date': self.publish_start_date,
                                }))
                            publishing_date = self.publish_start_date
                        else:
                            new_date = publishing_date + timedelta(days=self.time_interval)
                            publishing_date = new_date

                            scheduling_line.append((0,0, {
                                    'product_id': line.product_id.id,
                                    'name': line.name,
                                    'length': line.length,
                                    'width': line.width,
                                    'page_no': line.page.id,
                                    'ad_position': line.ad_position.id,
                                    'publish_date': publishing_date,
                                }))
        elif self.classified_bool_field:
            for line in self.classified_order_line:
                if self.scheduling_date == 'specific_date':
                    scheduling_line.append((0,0, {
                            'product_id': line.product_id.id,
                            'name': line.name,
                            'length': line.length,
                            'width': line.width,                            
                            'page_no': line.page.id,
                            'ad_position': line.ad_position.id,
                            'publish_date': self.specific_date,
                        }))
                else:
                    for i in range(0,self.no_of_occurence):
                        if i == 0:
                            scheduling_line.append((0,0, {
                                    'product_id': line.product_id.id,
                                    'name': line.name,
                                    'length': line.length,
                                    'width': line.width,
                                    'page_no': line.page.id,
                                    'ad_position': line.ad_position.id,
                                    'publish_date': self.publish_start_date,
                                }))
                            publishing_date = self.publish_start_date
                        else:
                            new_date = publishing_date + timedelta(days=self.time_interval)
                            publishing_date = new_date

                            scheduling_line.append((0,0, {
                                    'product_id': line.product_id.id,
                                    'name': line.name,
                                    'length': line.length,
                                    'width': line.width,
                                    'page_no': line.page.id,
                                    'ad_position': line.ad_position.id,
                                    'publish_date': publishing_date,
                                }))

        self.scheduling_line_ids.unlink()
        self.scheduling_line_ids = scheduling_line
        self.state = 'sent'


    def action_view_payments(self):

        return {
            'name': _('View Payments'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.payment',
            'domain': [('sale_order_id', '=', self[0].id)],
            'views_id': False,
            'views': [(self.env.ref('account.view_account_payment_tree').id or False, 'tree'),
                      (self.env.ref('account.view_account_payment_form').id or False, 'form')],
        }


class AdvertisementContentLine(models.Model):
    _name = 'advertisement.content.line'

    advertisement_language = fields.Selection([
        ('telugu','Telugu'),
        ('english','English')
        ], string="Advertisement Language", default='telugu')
    advertisement_description = fields.Text('Description')
    advertisement_description_as_per_lipi = fields.Text('Converted Description')
    no_of_characters = fields.Integer('No of Characters')
    no_of_lines = fields.Integer('No of Lines')
    advertisement_line_id = fields.Many2one('sale.order',string='Sale Order Ref')


    @api.onchange('advertisement_description')
    def onchange_advertisement_description(self):
        if self.advertisement_description:
            description_len = len(str(self.advertisement_description))
            if self.advertisement_language == 'english':
                description_line = int(description_len)/18
            else:
                description_line = int(description_len)/15
            if math.ceil(description_line) > 18:
                raise UserError('Advertisement Description can not be greater than 18 Lines')
            else:
                self.no_of_characters = description_len
                self.no_of_lines = math.ceil(description_line)

            ascii_list = []
            for char in self.advertisement_description:
                ascii_value = ord(char)
                ascii_list.append(ascii_value)
            self.advertisement_description_as_per_lipi = ascii_list


class SchedulingLines(models.Model):
    _name = 'scheduling.lines'

    product_id = fields.Many2one('product.product', string="Product")
    name = fields.Char('Description')
    length = fields.Integer('Length')
    width = fields.Integer('Width')
    page = fields.Integer('Page No')
    page_no = fields.Many2one('newspaper.page.details', string='Page No')
    ad_position = fields.Many2one('advertisement.position', string="Position")
    publish_date = fields.Date('Publish Date', readonly=True)
    scheduling_status = fields.Selection([
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
        ], string="Status", readonly=True)
    rejected_reason = fields.Char('Reject Reason', readonly=True)
    scheduling_line_id = fields.Many2one('sale.order', string="Sale Order ref")

    def action_approve_schedule(self):
        self.scheduling_status = 'approved'

    def open_position_help(self):
        position_help_obj = self.env['scheduling.position.details'].search([('publish_date', '=', self.publish_date)])
        return {
            'name': _('Position Help'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'scheduling.position.details',
            'domain': [('id', '=', position_help_obj.ids)],
            'views_id': False,
            'views': [(self.env.ref('eenadu_reta.scheduling_position_details_form_view').id or False, 'tree'),
                      (self.env.ref('eenadu_reta.newspaper_page_details_tree_view').id or False, 'form')],
        }


class SaleRelatedDocuments(models.Model):
    _name = 'sale.related.documents'

    name = fields.Many2one('sale.document.type', string='Name')
    related_document = fields.Binary('Attachment')
    sale_related_document_id = fields.Many2one('sale.order', string='Sale Order ref')