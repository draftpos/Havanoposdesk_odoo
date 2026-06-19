from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    havano_allow_negative_stock = fields.Boolean(
        string="Allow Negative Stock",
        config_parameter="havanoposdesk.allow_negative_stock",
        default=True,
        help="If enabled, you can sell items even if their stock quantity goes below zero. Purchasing items will compensate for the negative balance."
    )

    havano_currency_id = fields.Many2one(
        'res.currency', 
        string="Business Currency",
        related='env.user.tenant_id.currency_id',
        readonly=False
    )
    havano_allow_multi_currency = fields.Boolean(
        string="Allow Multi Currency",
        related='env.user.tenant_id.allow_multi_currency',
        readonly=False
    )
