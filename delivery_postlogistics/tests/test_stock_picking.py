# Copyright 2025 BizzAppDev Systems Pvt. Ltd.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError

from .common import TestPostlogisticsCommon


class TestStockPicking(TestPostlogisticsCommon):
    @classmethod
    def setUpClass(self):
        super().setUpClass()

        res_partner_env = self.env["res.partner"]
        stock_picking_env = self.env["stock.picking"]
        product_env = self.env["product.product"]
        delivery_carrier_env = self.env["delivery.carrier"]

        self.partner = res_partner_env.create(
            {
                "name": "Test Partner",
                "street": "123 Test St.",
                "city": "Test City",
                "zip": 234567,
                "country_id": self.env.ref("base.us").id,
            }
        )
        self.picking = stock_picking_env.create(
            {
                "name": "Test Picking",
                "delivery_type": "postlogistics",
                "picking_type_id": self.env.ref("stock.picking_type_out").id,
                "partner_id": self.partner.id,
            }
        )
        self.product = product_env.create({"name": "Test Product"})
        self.carrier = delivery_carrier_env.create(
            {
                "name": "PostLogistics",
                "delivery_type": "postlogistics",
                "product_id": self.product.id,
            }
        )

    def test_action_generate_carrier_label_no_carrier(self):
        """Test that an error is raised when generating a carrier label without a
        carrier."""
        with self.assertRaisesRegex(UserError, "Please, set a carrier."):
            self.picking.action_generate_carrier_label()
