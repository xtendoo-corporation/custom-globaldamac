import json
import logging
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('grid_product_tmpl_id')
    def _set_grid_up(self):
        if self.grid_product_tmpl_id:
            self.grid_update = False
            matrix = self._get_matrix(self.grid_product_tmpl_id)
            self.grid = json.dumps(matrix)

    @api.onchange('grid')
    def _apply_grid(self):
        if self.grid and self.grid_update:
            grid = json.loads(self.grid)
            product_template = self.env['product.template'].browse(grid['product_template_id'])
            dirty_cells = grid['changes']
            Attrib = self.env['product.template.attribute.value']
            default_so_line_vals = {}
            new_lines = []
            for cell in dirty_cells:
                combination = Attrib.browse(cell['ptav_ids'])
                no_variant_attribute_values = combination - combination._without_no_variant_attributes()
                # create or find product variant from combination
                product = product_template._create_product_variant(combination)
                order_lines = self.order_line.filtered(
                    lambda line: line.product_id.id == product.id
                                 and line.product_no_variant_attribute_value_ids.ids == no_variant_attribute_values.ids
                )
                old_qty = sum(order_lines.mapped('product_uom_qty'))
                qty = cell['qty']
                diff = qty - old_qty
                if not diff:
                    continue
                if order_lines:
                    if qty == 0:
                        if self.state in ['draft', 'sent']:
                            self.order_line -= order_lines
                        else:
                            order_lines.update({'product_uom_qty': 0.0})
                    else:
                        if len(order_lines) > 1:
                            raise ValidationError(
                                _("You cannot change the quantity of a product present in multiple sale lines."))
                        else:
                            order_line = order_lines[0]
                            order_line.product_uom_qty = qty
                            # Calcular y asignar box_quantity
                            units_per_box = getattr(order_line, 'units_per_box', 0.0) or 0.0
                            if units_per_box > 0:
                                box_qty = qty / units_per_box
                            else:
                                box_qty = 0.0
                            order_line.box_quantity = box_qty
                else:
                    if not default_so_line_vals:
                        OrderLine = self.env['sale.order.line']
                        default_so_line_vals = OrderLine.default_get(OrderLine._fields.keys())
                    last_sequence = self.order_line[-1:].sequence
                    if last_sequence:
                        default_so_line_vals['sequence'] = last_sequence
                    # Obtener units_per_box del producto
                    units_per_box = getattr(product, 'units_per_box', 0.0) or 0.0
                    if units_per_box > 0:
                        box_qty = qty / units_per_box
                    else:
                        box_qty = 0.0
                    new_line_vals = dict(
                        default_so_line_vals,
                        product_id=product.id,
                        product_uom_qty=qty,
                        product_no_variant_attribute_value_ids=no_variant_attribute_values.ids,
                        box_quantity=box_qty
                    )
                    new_lines.append((0, 0, new_line_vals))
            if new_lines:
                self.update(dict(order_line=new_lines))
