/** @odoo-module */
import { Component, useState } from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";

export class ProductInventoryPopup extends Component {
    static template = "tech_zone.ProductInventoryPopup";
    static components = { Dialog };

    setup() {
        // Initialize state to track the selected stock type
        this.state = useState({ selectedStockType: null });
    }

    setSelectedStockType(stockType) {
        this.state.selectedStockType = this.state.selectedStockType === stockType ? null : stockType;
    }
}
