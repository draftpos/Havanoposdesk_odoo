/** @odoo-module **/

import { registry } from "@web/core/registry";
import { session } from "@web/session";

const userMenuRegistry = registry.category("user_menuitems");

// If the user is NOT a system admin, remove standard profile dropdown items.
if (!session.is_system) {
    const itemsToRemove = [
        "support",
        "shortcuts",
        "preferences",
        "odoo_account",
        "install_pwa",
        "separator"
    ];
    
    itemsToRemove.forEach((item) => {
        if (userMenuRegistry.contains(item)) {
            userMenuRegistry.remove(item);
        }
    });
}
