# -*- coding: utf-8 -*-

from openerp import models, fields, api
 
class music(models.Model):
     _name = 'conservatori.music'
 
     name = fields.Char()
     instrument = fields.Char()
     grup = fields.Many2one('conservatori.grup')
     reforc = fields.Many2many('conservatori.grup','m2mrefoc','reforcos','reforc')
     grupantic = fields.Many2many('conservatori.grup','m2mantic','musicantic','grupantic')
     phone = fields.Char(related='grup.director.phone', store=False)
     foto = fields.Binary('Photo')
     numero = fields.Integer('Numero')

class grup(models.Model):
     _name = 'conservatori.grup'
     name = fields.Char()
     director = fields.Many2one('res.partner')
     titulars = fields.One2many('conservatori.music','grup')
     reforcos = fields.Many2many('conservatori.music','m2mrefoc','reforc','reforcos')
     musicantic = fields.Many2many('conservatori.music','m2mantic','grupantic','musicantic')
