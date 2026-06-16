from odoo import models, fields

class ResUsers(models.Model):
    _inherit = "res.users"
    
    tenant_id = fields.Many2one("havanoposdesk.tenant", string="Tenant")
