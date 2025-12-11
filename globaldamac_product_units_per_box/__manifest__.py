# Copyright 2024 Xtendoo (https://xtendoo.es)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Globaldamac Product Units Per Box",
    "version": "17.0.1.0.0",
    "license": "AGPL-3",
    "author": "Xtendoo",
    "category": "Sales",
    "summary": "Box units management for product variants",
    "description": """
        This module allows configuring units per box in product variants.

        Features:
        - Units per box field in product variants
        - Total units visualization in sale order lines
        - Total units visualization in stock moves and pickings
        - Total units visualization in invoice lines
        - Integration with pricelists for box volume-based pricing
    """,
    "depends": [
        "sale",
        "product",
        "stock",
        "account",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/product_product_views.xml",
        "views/sale_order_views.xml",
        "views/stock_views.xml",
        "views/account_move_views.xml",
        "views/product_pricelist_views.xml",
        "views/report_sale_order.xml",
        "views/report_delivery.xml",
        "views/report_invoice.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
