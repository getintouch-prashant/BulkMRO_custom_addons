# -*- coding: utf-8 -*-

from openerp import models, fields, api

# class crm_bulkmro(models.Model):
#     _name = 'crm_bulkmro.crm_bulkmro'

#     name = fields.Char()

class crm_lead(models.Model):
    
    _inherit = 'crm.lead'

    
    def get_inq_number(self):
        return self.env['ir.sequence'].get('crm.lead.inquiry.sequence') or ''
        
    inquiry_number = fields.Char(string = "Inquiry Number", default=get_inq_number)

    def name_get(self, cr, user, ids, context=None):
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