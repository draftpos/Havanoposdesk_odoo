from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    havano_allow_negative_stock = fields.Boolean(
        string="Allow Negative Stock",
        config_parameter="havanoposdesk.allow_negative_stock",
        default=True,
        help="If enabled, you can sell items even if their stock quantity goes below zero. Purchasing items will compensate for the negative balance."
    )

    biz_currency_id = fields.Many2one(
        'res.currency', 
        string="Business Currency",
        readonly=False
    )
    biz_allow_multi_currency = fields.Boolean(
        string="Allow Multi Currency",
        readonly=False
    )

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        tenant = self.env.user.tenant_id
        if tenant:
            res.update(
                biz_currency_id=tenant.currency_id.id,
                biz_allow_multi_currency=tenant.allow_multi_currency,
            )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        tenant = self.env.user.tenant_id
        if tenant:
            tenant.sudo().write({
                'currency_id': self.biz_currency_id.id,
                'allow_multi_currency': self.biz_allow_multi_currency,
            })
