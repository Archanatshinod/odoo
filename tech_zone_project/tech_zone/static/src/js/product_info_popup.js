/** @odoo-module **/
import { ProductInfoPopup } from "@point_of_sale/app/screens/product_screen/product_info_popup/product_info_popup";
import { patch } from "@web/core/utils/patch";
import { usePos } from "@point_of_sale/app/store/pos_hook";

patch(ProductInfoPopup.prototype, {
    setup() {
        this.pos = usePos();

        if (!this.props.product) {
            console.error("this.props.product is undefined");
            return;
        }

        console.log("Product Props:", this.props.product);

        if (this.props.product?.stock_online !== undefined && this.props.product?.stock_offline !== undefined) {
            console.log("Stock Info:", {
                stock_online: this.props.product.stock_online,
                stock_offline: this.props.product.stock_offline,
            });
        } else {
            console.warn("Stock Info is missing for product:", this.props.product);
        }
    },
});
