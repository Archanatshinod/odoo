/** @odoo-module */
import { patch } from "@web/core/utils/patch";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { ProductInventoryPopup } from "@tech_zone/js/product_inventory_popup"; // Import custom popup

patch(ProductScreen.prototype, {
    setup() {
        super.setup();
        this.notification = useService("notification"); // Odoo's notification service
    },

    async addProductToOrder(product) {
        console.log("Attempting to add product:", product);

        // 🔹 Check if product is out of stock
        console.log("Stock Info:", { stock_online: product.stock_online, stock_offline: product.stock_offline });

        if (product.stock_online <= 0 && product.stock_offline <= 0) {
            this.notification.add(_t("This product is out of stock"), { type: "warning" });
            return; // ❌ Stops execution (Remove this if you want to allow adding)
        }

        let selectedStockType = null; // Track the selected stock type

        // 🔹 Show inventory selection popup
        await new Promise((resolve) => {
            this.dialog.add(ProductInventoryPopup, {
                title: "Inventory Selection",
                message: `Select inventory for ${product.name}.`,
                product: product,

                setSelectedStockType: (type) => {
                    console.log("Selected stock type:", type);
                    selectedStockType = type; // Store selected type
                },

                close: () => {
                    console.log("Popup closed");

                    // Ensure stock type is selected before proceeding
                    if (!selectedStockType) {
                        console.error("Stock type selection is required.");
                        alert("Please select a stock type before proceeding.");
                        return;
                    }
                    resolve(true); // ✅ Continue execution
                },
            });
        });

        //  Ensure product is added only if a stock type was selected
        if (selectedStockType) {
            console.log("Adding product to cart...");
            super.addProductToOrder(product);
        }
    }
});
