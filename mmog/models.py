# -*- coding: utf-8 -*-

from openerp import models, fields, api

class player(models.Model):
     _name = 'mmog.player'
#url, email, image, float_time, reference, html, progressbar, statusbar, handle, etc.
# https://github.com/sotogarcia/odoo-development/wiki/Field-widgets-were-found#progressbar
     name = fields.Char()
     active = fields.Boolean()
     points = fields.Integer()
     money = fields.Integer()
     gold = fields.Integer()
     coal = fields.Integer()
     stones = fields.Integer()
     fortress = fields.One2many('mmog.fortress','id_player')
     avatar = fields.Binary()
     @api.model
     def create(self, values):
        new_id = super(player, self).create(values)
        print values
        name_player = new_id.name
        img = self.env['mmog.fortress'].search([('name','=','f1')])[0].icon
        self.env['mmog.fortress'].create({'name':name_player+"-fortress",'level':1,'soldiers':100,'population':10,'food':1000,'integrity':100,'id_player':new_id.id,'icon':img})
        return new_id

class fortress(models.Model):
     _name = 'mmog.fortress'
     name = fields.Char()
     id_player = fields.Many2one('mmog.player')
     level = fields.Integer()
     state = fields.Char()
     soldiers = fields.Integer()
     population = fields.Integer()
     food = fields.Integer()
     integrity = fields.Float()
     x = fields.Integer()
     y = fields.Integer()
     icon = fields.Binary()
#     @api.model
#     def create(self, values):
#        new_id = super(fortress, self).create(values)
#        print values
#        return new_id
#En l'exemple del joc, un model guarda els atacs. Aquests són d'una fortalessa a un altra. En teoria, el jugador pot decidir en quants soldats va a atacar. Des de que es llança l'atac fins a que acaba la batalla passa un temps. Durant eixe temps es suposa que els dos bandos van perdent soldats fins a que un es queda a 0. Els soldats es perden en funció del nivell de la fortalesa, la integritat de la mateixa i la proporció de soldats. Per fer-lo més realista, no es va a fer tot en un cálcul. El que anem a fer és dividir la batalla en atacs en els que en funció dels paràmetres esmentats, els contrincants aniran perdent més o menys soldats. Com que la batalla pot durar hores, durant eixe temps al defensor li pot donar temps a reforçar, pujar el nivell o reparar la integritat de la fortalesa. A l'atacant li pot donar temps a retirar-se o a enviar un altre atac. Cada vegada que es mostre o es modifique algun paràmetre de l'atac o les fortaleses implicades, cal recalcular l'estat de la batalla.

class attack(models.Model):
     _name = 'mmog.attack'
     name = fields.Char()
     fortress_attacking = fields.Many2one('mmog.fortress')
     fortress_defender = fields.Many2one('mmog.fortress')
     data = fields.Datetime()
     soldiers_sent = fields.Integer()
     attacker_soldiers_killed = fields.Integer()
     defender_soldiers_killed = fields.Integer()
     progress = fields.Float()
