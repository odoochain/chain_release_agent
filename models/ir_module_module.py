# © 2022 Le Filament (<http://www.le-filament.com>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import requests

from odoo import exceptions, models


class IrModule(models.Model):
    _inherit = "ir.module.module"

    # ------------------------------------------------------
    # Common function
    # ------------------------------------------------------
    def _get_modules(self):
        modules = self.sudo().search([("state", "=", "installed")])
        res = modules.mapped(
            lambda m: {
                "name": m.name,
                "author": m.author,
                "latest_version": m.latest_version,
                "author_type": m._get_author_type(),
            }
        )
        return res

    def _get_author_type(self):
        self.ensure_one()
        if "OCA" in self.author:
            return "oca"
        elif "FILAMENT" in self.author.upper():
            return "lefilament"
        elif "Odoo S.A." in self.author:
            return "odoo"
        else:
            return "other"

    def post_modules(self):
        try:
            requests.post(
                url="https://monfil.le-filament.com/post-modules",
                json={"modules": self._get_modules()},
                verify=True,
                timeout=10,
            )
        except Exception as e:
            raise exceptions.UserError(e.__str__())
