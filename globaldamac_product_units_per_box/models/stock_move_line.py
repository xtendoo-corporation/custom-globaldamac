# Copyright 2024 Xtendoo (https://xtendoo.es)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

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
            if not self.quantity or self.quantity == 1.0:
                self.quantity = self.product_id.units_per_box
                self.box_quantity = 1.0

    @api.onchange('box_quantity')
    def _onchange_box_quantity(self):
        """Update quantity when box_quantity changes."""
        if self.box_quantity and self.units_per_box > 1.0:
            self.quantity = self.box_quantity * self.units_per_box

    @api.onchange('quantity')
    def _onchange_quantity(self):
        """Update box_quantity when quantity changes."""
        if self.quantity and self.units_per_box > 1.0:
            self.box_quantity = self.quantity / self.units_per_box

    @api.model_create_multi
    def create(self, vals_list):
        """Calculate box_quantity when creating move lines."""
        lines = super().create(vals_list)
        for line in lines:
            if line.units_per_box > 1.0 and line.quantity:
                if not line.box_quantity:
                    line.box_quantity = line.quantity / line.units_per_box
        return lines

    def write(self, vals):
        """Recalculate box_quantity when updating move lines."""
        res = super().write(vals)
        if 'quantity' in vals or 'product_id' in vals:
            for line in self:
                if line.units_per_box > 1.0 and line.quantity:
                    if not line.box_quantity or 'quantity' in vals:
                        line.box_quantity = line.quantity / line.units_per_box
        return res

