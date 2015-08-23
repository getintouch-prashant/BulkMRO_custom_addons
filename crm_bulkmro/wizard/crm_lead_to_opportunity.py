
from openerp.osv import fields, osv
from openerp.tools.translate import _
import re

class crm_lead2opportunity_partner(osv.osv_memory):
#     _name = 'crm.lead2opportunity.partner'
#     _description = 'Lead To Opportunity Partner'
    _inherit = 'crm.lead2opportunity.partner'

    _columns = {
        'inquiry_number': fields.char('Inquiry Number'),
        'opportunity_id': fields.many2one('crm.lead', 'Select Opportunity'),
    }
    
    def action_apply(self, cr, uid, ids, context=None):
        """
        Convert lead to opportunity or merge lead and opportunity and open
        the freshly created opportunity view.
        """
        if context is None:
            context = {}

        lead_obj = self.pool['crm.lead']

        w = self.browse(cr, uid, ids, context=context)[0]
        opp_ids = [o.id for o in w.opportunity_ids]
        vals = {
            'section_id': w.section_id.id,
        }
        if w.partner_id:
            vals['partner_id'] = w.partner_id.id
        if w.name == 'merge':
            lead_id = lead_obj.merge_opportunity(cr, uid, opp_ids, context=context)
            lead_ids = [lead_id]
            lead = lead_obj.read(cr, uid, lead_id, ['type', 'user_id'], context=context)
            if lead['type'] == "lead":
                context = dict(context, active_ids=lead_ids)
                vals.update({'lead_ids': lead_ids, 'user_ids': [w.user_id.id]})
                self._convert_opportunity(cr, uid, ids, vals, context=context)
            elif not context.get('no_force_assignation') or not lead['user_id']:
                vals.update({'user_id': w.user_id.id})
                lead_obj.write(cr, uid, lead_id, vals, context=context)
        else:
            lead_ids = context.get('active_ids', [])
            
            if len(lead_ids) == 1:
                lead_obj.write(cr, uid, lead_ids[0], {'inquiry_number': w.inquiry_number}, context=context)
            
            vals.update({'lead_ids': lead_ids, 'user_ids': [w.user_id.id]})
            self._convert_opportunity(cr, uid, ids, vals, context=context)

        return self.pool.get('crm.lead').redirect_opportunity_view(cr, uid, lead_ids[0], context=context)