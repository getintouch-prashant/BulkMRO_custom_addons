# -*- coding: utf-8 -*-

from openerp import models, fields, api

# class crm_bulkmro(models.Model):
#     _name = 'crm_bulkmro.crm_bulkmro'

#     name = fields.Char()

class crm_lead(models.Model):
    
    _inherit = 'crm.lead'

    
    def get_inq_number(self):
        return self.env['ir.sequence'].get('crm.lead.inquiry.sequence') or '/'
        
    inquiry_number = fields.Char(string = "Inquiry Number", default=get_inq_number)

