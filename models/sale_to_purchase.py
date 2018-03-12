from odoo import models, fields, api
import odoo.addons.decimal_precision as dp
from odoo.exceptions import Warning

class SaleToPurchase(models.Model):
    _inherit = 'sale.order'
    

    @api.multi
    def action_purchase_orders(self):
        view_id = self.env.ref('sale_to_purchase.wizard_form_purchase_order').id
        context = self._context.copy()
        
        return {
            'name':'Purchase Order',
            'view_type':'form',
            'view_mode':'form',
            'views' : [(view_id,'form')],
            'res_model':'purchase.order.wizard',
            'view_id':view_id,
            'type':'ir.actions.act_window',
            'target':'new',
            'context':context,
        }
        
         
class PurchaseOrderWizard(models.TransientModel):
    _name= 'purchase.order.wizard'
    _description = 'Purchase Order wizard'
    
    partner_id = fields.Many2one('res.partner', string='Vendor',required=True)
    order_line=fields.One2many('purchase.order.line.wizard', 'wizard_order_id', string='Order Lines')
    date_order = fields.Datetime(string='Order Date',required=True)
    company_id = fields.Many2one('res.company', string='Company')
    picking_type_id = fields.Many2one('stock.picking.type', 'Deliver To')
    
    @api.multi
    def generate_purchase_order(self):
        
        orderline_pooler=self.env['purchase.order.line']
        purchase_pooler=self.env['purchase.order']
        pur_id=purchase_pooler.create({'partner_id':self.partner_id.id,
#                                 'currency_id':self.currency_id,
#                                 'order_line':[(6,0,[line_ids])]
                                })
        for i in self.order_line:
            line_ids=orderline_pooler.create({'product_id':i.product_id.id,
                                                'name':i.name,
                                                'product_qty':i.product_qty,
                                                'price_unit':i.price_unit,
                                                'product_uom':1,
                                                'order_id':pur_id.id,
                                                'date_planned':self.date_order
                                                })
        pur_id.button_confirm()
    @api.model
    def default_get(self, fields):
        res = super(PurchaseOrderWizard, self).default_get(fields)
        context=self._context
        record=self.env['sale.order'].search([('id','=',context['active_id'])])
        result1=[]
        subtotal=0
       
        selection = context['o2m_selection']

        print(selection)

        line_selection = selection['order_line']

        # IDs of selected rows
        selected_ids = line_selection['ids']

        for item in record.order_line:
            if item.id in selected_ids:
                result1.append((0, 0, {'product_id': item.product_id.id,
                                    'name':item.name,
                                    'product_qty':item.product_uom_qty,
                                    'price_unit':item.price_unit,
                                    'product_uom':item.product_uom.id,
                                    'price_subtotal':item.price_unit*item.product_uom_qty
                                   
                                   
                                   }))
        res.update({'order_line': result1})   
        return res
    
class PurchaseOrder(models.TransientModel):
    _name = 'purchase.order.line.wizard'
    _description = 'Purchase Order Line wizard'

    
    @api.multi
    @api.depends('product_qty','price_unit')
    def _compute_amount(self):
        for record in self:
            record.price_subtotal=record.product_qty*record.price_unit
    
    
    name = fields.Text(string='Description')
    wizard_order_id=fields.Many2one('purchase.order.wizard')
    product_id = fields.Many2one('product.product', string='Product')
    product_qty = fields.Float(string='Quantity', digits=dp.get_precision('Product Unit of Measure'))
    price_unit = fields.Float(string='Unit Price', digits=dp.get_precision('Product Price'))
    product_uom = fields.Many2one('product.uom', string='Product Unit of Measure')
    price_subtotal = fields.Float(compute='_compute_amount',string='Subtotal')

class SaleOrderLine (models.Model):
    _inherit="sale.order.line"    
    isPurchased = fields.Boolean(string='Замовлено')
        