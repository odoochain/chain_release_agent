# Copyright 2022 Le Filament (https://le-filament.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from odoo import models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    def action_sync_modules(self):
        self.env["ir.module.module"].sudo().post_modules()
