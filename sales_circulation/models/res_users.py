import re
import logging
from odoo import api, fields, models, tools
from odoo.osv import expression
from odoo.exceptions import UserError


class ResUsersCustom(models.Model):
    _description = "Agents Create"
    _inherit = 'res.users'

    is_agent = fields.Boolean('Is agent?')

    @api.model_create_multi
    def create(self, vals_list):
        users = super(ResUsersCustom, self).create(vals_list)

        if users.is_agent:
            users.partner_id.is_newsprint_agent = True
            users.partner_id.active_agent = True
            users.partner_id.user_id = users.id

        return users

