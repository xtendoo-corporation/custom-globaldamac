# Copyright 2024 Xtendoo (https://xtendoo.es)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    units_per_box = fields.Float(
        string="Unidades por Caja",
        default=1.0,
        help="Numero de unidades que contiene cada caja. "
             "Este valor se usara para calcular las unidades totales. "
             "Si es mayor a 1, el producto se vende por cajas.",
    )

    def get_units_per_box(self):
        """Return the units per box for this product variant."""
        self.ensure_one()
        return self.units_per_box or 1.0

    def is_sold_by_box(self):
        """Check if this product is sold by box (units_per_box > 1)."""
        self.ensure_one()
        return self.units_per_box > 1.0

