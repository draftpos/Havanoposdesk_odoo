from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HavanoposdeskShop(models.Model):
    _name = 'havanoposdesk.shop'
    _description = 'Shop/Store'

    name = fields.Char(string='Shop Name', required=True)
    tenant_id = fields.Many2one('havanoposdesk.tenant', string='Tenant', required=True)
    active = fields.Boolean(string='Active', default=True)

    # Computed statistics fields to avoid undefined errors in list view
    terminal_count = fields.Integer(string='Terminals', compute='_compute_shop_statistics')
    last_open = fields.Date(string='Last Open', compute='_compute_shop_statistics')
    sales_count = fields.Integer(string='Sales Count', compute='_compute_shop_statistics')
    purchases_count = fields.Integer(string='Purchases Count', compute='_compute_shop_statistics')
    sale_value = fields.Float(string='Sales Value', compute='_compute_shop_statistics')
    users_count = fields.Integer(string='Users Count', compute='_compute_shop_statistics')

    def _compute_shop_statistics(self):
        for shop in self:
            # Terminals
            terminals = self.env['havanoposdesk.pos.terminal'].search([('shop_id', '=', shop.id)])
            shop.terminal_count = len(terminals)
            
            # Users
            shop.users_count = self.env['res.users'].search_count([('shop_ids', 'in', shop.id)])
            
            # Sales & Purchases (using store name string)
            sales = self.env['havanoposdesk.sale'].search([('store', '=', shop.name)])
            shop.sales_count = len(sales)
            shop.sale_value = sum(sales.mapped('line_ids.amount'))
            
            purchases = self.env['havanoposdesk.purchase'].search([('store', '=', shop.name)])
            shop.purchases_count = len(purchases)
            
            # Last open (from last sale date)
            if sales:
                last_sale = max(sales, key=lambda s: s.posting_date)
                shop.last_open = last_sale.posting_date
            else:
                shop.last_open = False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if self.env.user.havano_role == 'super_admin':
                continue
                
            tenant_id = vals.get('tenant_id') or self.env.user.tenant_id.id
            if not tenant_id:
                raise ValidationError('Cannot create a shop without an associated tenant.')
                
            tenant = self.env['havanoposdesk.tenant'].browse(tenant_id)
            if tenant.subscription_state != 'active':
                raise ValidationError('Cannot create a shop. The tenant subscription is not active.')
                
            plan = tenant.subscription_plan_id
            if not plan:
                raise ValidationError('Please pick a subscription plan to start creating shops.')
                
            if plan.max_shops and plan.max_shops > 0:
                current = self.search_count([('tenant_id', '=', tenant.id)])
                if current >= plan.max_shops:
                    raise ValidationError(f'Maximum number of shops ({plan.max_shops}) reached for this subscription plan.')
                    
            # Ensure the tenant_id is correctly forced
            vals['tenant_id'] = tenant_id

        return super().create(vals_list)


