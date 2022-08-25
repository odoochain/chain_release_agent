# Copyright 2022 Le Filament (https://le-filament.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

import json

from odoo import exceptions, http
from odoo.http import request


class ReleaseAgent(http.Controller):
    # ------------------------------------------------------
    # Routes
    # ------------------------------------------------------
    @http.route(
        ["/get-modules"],
        type="http",
        auth="none",
        method=["GET"],
        csrf=False,
    )
    def get_modules(self):
        db_header = request.httprequest.headers.get("DbName", False)
        if db_header and db_header == request.db:
            modules = (
                request.env["ir.module.module"]
                .sudo()
                .search([("state", "=", "installed")])
            )
            res = modules.mapped(
                lambda m: {
                    "name": m.name,
                    "author": m.author,
                    "author_type": self.get_author_type(m),
                }
            )
            return http.Response(
                response=json.dumps(res),
                headers=[("Content-Type", "application/json")],
            )
        else:
            return exceptions.AccessDenied()

    # ------------------------------------------------------
    # Common functions
    # ------------------------------------------------------
    def get_author_type(self, module):
        if "OCA" in module.author:
            return "oca"
        elif "FILAMENT" in module.author.upper():
            return "lefilament"
        elif "Odoo S.A." in module.author:
            return "odoo"
        else:
            return "other"
