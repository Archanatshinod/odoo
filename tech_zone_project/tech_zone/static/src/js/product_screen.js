/** @odoo-module */
import { patch } from "@web/core/utils/patch";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { ProductInventoryPopup } from "@tech_zone/js/product_inventory_popup"; // Importing custom popup


patch(ProductScreen.prototype, {
    setup() {
        super.setup();
        this.notification = useService("notification"); // Odoo's notification service
    },

    async addProductToOrder(product) {
        console.log("Adding product:", product);

        // Check stock levels before adding the product
        if (product.stock_online <= 0 && product.stock_offline <= 0) {
            this.notification.add(_t("This product is out of stock"), {
                type: "warning",
            });
            return; // Stop further execution
        }

      // Open the dialog and wait to close it
        await this.dialog.add(ProductInventoryPopup, {
            title: "Inventory selection",
            message: `Select inventory for ${product.name}.`,
            product: product,
            selectedStockType: "null",
            setSelectedStockType: (type) => {
                console.log("Selected stock type:", type);
            },
            close: () => {
                console.log("Dialog closed");
            },
        });
        // After the dialog is closed, proceed to add the product to the cart
        super.addProductToOrder(product);
    },
});
