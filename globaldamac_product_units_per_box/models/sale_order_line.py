# Copyright 2024 Xtendoo (https://xtendoo.es)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    units_per_box = fields.Float(
        string="Unidades por Caja",
        related="product_id.units_per_box",
        store=True,
        readonly=True,
        help="Numero de unidades que contiene cada caja.",
    )
    box_quantity = fields.Float(
        string="Cantidad de Cajas",
        digits='Product Unit of Measure',
        help="Numero de cajas. Al cambiar este valor se actualizara la cantidad de unidades.",
    )

    @api.onchange('product_id')
    def _onchange_product_id_set_quantity(self):
        """Set default quantity to units_per_box when product is selected."""
        if self.product_id and self.product_id.units_per_box > 1.0:
            self.product_uom_qty = self.product_id.units_per_box
            self.box_quantity = 1.0

    @api.onchange('box_quantity')
    def _onchange_box_quantity(self):
        """Update product_uom_qty when box_quantity changes."""
        if self.box_quantity and self.units_per_box > 1.0:
            self.product_uom_qty = self.box_quantity * self.units_per_box

    @api.onchange('product_uom_qty')
    def _onchange_product_uom_qty(self):
        """Update box_quantity when product_uom_qty changes."""
        if self.product_uom_qty and self.units_per_box > 1.0:
            self.box_quantity = self.product_uom_qty / self.units_per_box

    def _prepare_procurement_values(self, group_id=False):
        """Pass box_quantity to stock moves."""
        values = super()._prepare_procurement_values(group_id=group_id)
        values['box_quantity'] = self.box_quantity
        return values

