# -*- coding: utf-8 -*-

from openerp import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class crm_lead(models.Model):
    
    _inherit = 'crm.lead'

    
    def get_inq_number(self):
        return self.env['ir.sequence'].get('crm.lead.inquiry.sequence') or ''
        
    inquiry_number = fields.Char(string = "Inquiry Number", default=get_inq_number)

    def name_get(self, cr, user, ids, context=None):
        if type(ids) is int:
            ids = [ids]
        if not len(ids):
            return []
        if context is None:
            context = {}
        leads = self.read(cr, user, ids, ['name','inquiry_number'], context)
        leads_list = []
        for lead in leads:
            name = ("["+lead['inquiry_number']+"]" if lead['inquiry_number'] else "" ) + lead['name']
            leads_list.append([lead['id'], name])
        return leads_list
        
    
    def name_search(self, cr, uid, name = "", args=None, operator='ilike', context=None, limit=100):       
        if not args:
            args = []
        if context is None:
            context = {}
        args = args[:]
        lead_ids = self.search(cr, uid, ['|',('inquiry_number', 'ilike', '%%%s%%' % name),('name', 'ilike', '%%%s%%' % name)]+args, limit=limit, context=context)
        return self.name_get(cr, uid, lead_ids, context=context)
     
# Fetch Mail from seller@bulkmro.com and convert to Opportunity
#    @api.multi
    def case_mark_seller_lead(self, cr, uid, id, context = {}):
        
        """ Mark the case as one of the Seller stage: state=  and probability=0
        """
#	_logger.warning("Seller IDS %s and context %s"%(ids, context))
#	if context.get('active_model', False) == 'crm.lead':
        seller_stage = self.pool.get('crm.case.stage').search(cr, uid, [('name','=', 'Seller Lead')])
        if len(seller_stage):
            self.write(cr, uid, id, {'type': 'lead','stage_id': seller_stage[0]}, context)

#        if context is None:
#            context = {}
#        stage_id = self.pool.get('crm.case.stage').search(cr, uid, [('name','=','Introduction Mail to Supplier')], context)
#        try:
#            self.write(cr, uid, ids, {'stage_id': stage_id}, context=context)
#        except Exception:
#            _logger.error(Exception)
#        return True


#         if not args:
#             args = []
#         if name and operator in ('=', 'ilike', '=ilike', 'like', '=like'):
# 
#             self.check_access_rights(cr, uid, 'read')
#             where_query = self._where_calc(cr, uid, args, context=context)
#             self._apply_ir_rules(cr, uid, where_query, 'read', context=context)
#             from_clause, where_clause, where_clause_params = where_query.get_sql()
#             where_str = where_clause and (" WHERE %s AND " % where_clause) or ' WHERE '
# 
#             # search on the name of the contacts and of its company
#             search_name = name
#             if operator in ('ilike', 'like'):
#                 search_name = '%%%s%%' % name
#             if operator in ('=ilike', '=like'):
#                 operator = operator[1:]
# 
#             unaccent = get_unaccent_wrapper(cr)
# 
#             query = """SELECT id
#                          FROM res_partner
#                       {where} ({email} {operator} {percent}
#                            OR {phone} {operator} {percent}
#                            OR {display_name} {operator} {percent})
#                      ORDER BY {display_name}
#                     """.format(where=where_str, operator=operator,
#                                email=unaccent('email'),
#                                 phone=unaccent('phone'),
#                                display_name=unaccent('display_name'),
#                                percent=unaccent('%s'))
#             
#             where_clause_params += [search_name, search_name, search_name ]
#             if limit:
#                 query += ' limit %s'
#                 where_clause_params.append(limit)
#             
#             
#             cr.execute(query, where_clause_params)
#             ids = map(lambda x: x[0], cr.fetchall())
# 
#             if ids:
#                 return self.name_get(cr, uid, ids, context)
#             else:
#                 return []
