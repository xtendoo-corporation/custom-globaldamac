# Copyright 2024 Xtendoo (https://xtendoo.es)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductPricelistItem(models.Model):
    _inherit = "product.pricelist.item"

    use_box_quantity = fields.Boolean(
        string="Usar Cantidad de Cajas",
        default=False,
        help="Si está marcado, la cantidad mínima se refiere a cajas "
             "en lugar de unidades para productos que se venden por caja.",
    )
    min_box_quantity = fields.Float(
        string="Cantidad Mínima de Cajas",
        default=0.0,
        help="Cantidad mínima de cajas para aplicar esta regla de tarifa.",
    )
    max_box_quantity = fields.Float(
        string="Cantidad Máxima de Cajas",
        default=0.0,
        help="Cantidad máxima de cajas para aplicar esta regla. "
             "0 significa sin límite.",
    )

    @api.model
    def _get_applicable_rules_domain(self, products, date, **kwargs):
        """Override to consider box quantities in pricelist rules."""
        domain = super()._get_applicable_rules_domain(products, date, **kwargs)
        return domain

    def _is_applicable_for_box_product(self, product, box_qty):
        """Check if this pricelist item is applicable based on box quantity."""
        self.ensure_one()
        if not self.use_box_quantity:
            return True
        if not product.is_sold_by_box():
            return True

        # Check minimum box quantity
        if self.min_box_quantity > 0 and box_qty < self.min_box_quantity:
            return False

        # Check maximum box quantity
        if self.max_box_quantity > 0 and box_qty > self.max_box_quantity:
            return False

        return True

