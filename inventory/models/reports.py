from odoo import models, fields

class StockValuation(models.Model):
    _name = 'havanoposdesk.stock.valuation'
    _description = 'Stock Valuation'

    item_name = fields.Char(string='Item Name')
    item_code = fields.Char(string='Code')
    category_id = fields.Many2one('havanoposdesk.category', string='Category')
    store = fields.Char(string='Store')
    on_hand_qty = fields.Float(string='On Hand Qty')
    value_cost = fields.Float(string='Value Cost')
    value_selling = fields.Float(string='Value Selling')

class StockLedger(models.Model):
    _name = 'havanoposdesk.stock.ledger'
    _description = 'Stock Ledger'

    item_name = fields.Char(string='Item Name')
    item_code = fields.Char(string='Code')
    uom_id = fields.Many2one('havanoposdesk.uom', string='UOM')
    in_qty = fields.Float(string='In Qty')
    out_qty = fields.Float(string='Out Qty')
    balance_qty = fields.Float(string='Balance Qty')
    store = fields.Char(string='Store')
    category_id = fields.Many2one('havanoposdesk.category', string='Item Category')
    in_value = fields.Float(string='In Value')
    out_value = fields.Float(string='Out Value')
    cost_price = fields.Float(string='Cost Price')
    type = fields.Char(string='Type')
    doc_no = fields.Char(string='Doc No')
    balance_value = fields.Float(string='Balance Value')
