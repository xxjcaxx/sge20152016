# -*- coding: utf-8 -*-

from openerp import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class camion(models.Model):
     _name = 'cooperativa.camion'

     name = fields.Char()
     matricula = fields.Char()
     cajones = fields.Integer()
     id_socio = fields.Many2one('cooperativa.socio')
     arrobas = fields.Float(compute='_cal_arrobas',store=True)

     @api.depends('cajones')
     def _cal_arrobas(self):
         for i in self:
             i.arrobas = i.cajones*12.5

class socio(models.Model):
     _name = 'cooperativa.socio'
     name = fields.Char()
     camiones = fields.One2many('cooperativa.camion','id_socio')
     n_camiones = fields.Integer(compute='_n_camiones')
     arrobas = fields.Float(compute='_n_camiones')     
     foto = fields.Binary()     

     def _n_camiones(self):
        for i in self:
            for j in i.camiones:
                i.n_camiones = i.n_camiones+1
                i.arrobas = i.arrobas + j.arrobas
                _logger.warning("Hola")
