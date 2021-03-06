# -*- coding: utf-8 -*-

from openerp import models, fields, api
from random import randint
import datetime

class wizard(models.TransientModel):
     _name = 'mmog.wizard'

     def _default_attacker(self):
         return self.env['mmog.fortress'].browse(self._context.get('active_id'))

     fortress_attacker = fields.Many2one('mmog.fortress',default=_default_attacker)
     fortress_target = fields.Many2one('mmog.fortress') 
     soldiers_sent = fields.Integer(default=1)



     @api.multi
     def launch(self):
       if self.fortress_attacker.soldiers >= self.soldiers_sent:
          self.env['mmog.attack'].create({'fortress_attacking':self.fortress_attacker.id,'fortress_defender':self.fortress_target.id,'data':fields.datetime.now(),'soldiers_sent':self.soldiers_sent})
       return {}


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
   #  @api.model
   #  def name_get(self):
   #     res=[]
   #     for i in self:
   #         res.append((i.id,str(i.name)+", "+str(i.id_player.name)))
   #     return res  
#     @api.model
#     def create(self, values):
#        new_id = super(fortress, self).create(values)
#        print values
#        return new_id
#En l'exemple del joc, un model guarda els atacs. Aquests són d'una fortalessa a un altra. En teoria, el jugador pot decidir en quants soldats va a atacar. Des de que es llança l'atac fins a que acaba la batalla passa un temps. Durant eixe temps es suposa que els dos bandos van perdent soldats fins a que un es queda a 0. Els soldats es perden en funció del nivell de la fortalesa, la integritat de la mateixa i la proporció de soldats. Per fer-lo més realista, no es va a fer tot en un cálcul. El que anem a fer és dividir la batalla en atacs en els que en funció dels paràmetres esmentats, els contrincants aniran perdent més o menys soldats. Com que la batalla pot durar hores, durant eixe temps al defensor li pot donar temps a reforçar, pujar el nivell o reparar la integritat de la fortalesa. A l'atacant li pot donar temps a retirar-se o a enviar un altre atac. Cada vegada que es mostre o es modifique algun paràmetre de l'atac o les fortaleses implicades, cal recalcular l'estat de la batalla.
# la batalla tindrà un màxim de 5 hores en les quals, si no a perdut ningú, es considera empat i acaba. Els soldats atacants es retiren
class attack(models.Model):
     _name = 'mmog.attack'
     name = fields.Char()
     fortress_attacking = fields.Many2one('mmog.fortress')
     fortress_defender = fields.Many2one('mmog.fortress')
     data = fields.Datetime()
     last_update = fields.Datetime(default=fields.datetime.now())
     soldiers_sent = fields.Integer()
     attacker_soldiers_killed = fields.Integer()
     defender_soldiers_killed = fields.Integer()
     progress = fields.Float()
     finished = fields.Boolean(default=False)
     distance = fields.Integer(compute='_get_distance')
     arrival_date = fields.Datetime(compute='_get_distance')
     def _get_distance(self):
        for a in self:
            at = a.fortress_attacking
            df = a.fortress_defender
            a.distance=((at.x-df.x)**2+(at.y-df.y)**2)**0.5
            DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
            data1=datetime.datetime.strptime(a.data,DATETIME_FORMAT)
            end=data1+datetime.timedelta(minutes=a.distance)
            #print end.time()
            #print end
            #print data1
            a.arrival_date=end

     @api.model
     def update_progress(self):
        att = self.search([('finished','=',False)])
        DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"                                         
        att.write({'last_update': datetime.datetime.now()})
        print att
        for i in att:
           end=datetime.datetime.strptime(i.arrival_date,DATETIME_FORMAT)                
           if end < datetime.datetime.now():
              diflevel = i.fortress_attacking.level/i.fortress_defender.level
                                                           
              i.write({'progress':10})
              for k in range(0,i.soldiers_sent):
                  if i.fortress_defender.soldiers > 0 and randint(0,100) < 30:
                     i.fortress_defender.write({'soldiers': i.fortress_defender.soldiers - 1})
                     i.write({'defender_soldiers_killed': i.defender_soldiers_killed+1})
              for k in range(0,i.fortress_defender.soldiers):
                  if i.soldiers_sent > 0 and randint(0,100) < 30:
                     i.write({'soldiers_sent': i.soldiers_sent - 1})
                     i.write({'attacker_soldiers_killed': i.attacker_soldiers_killed+1})
              i.write({'progress':min(i.progress+1,100)})                           
              if i.soldiers_sent == 0 or i.fortress_defender.soldiers == 0:
                 i.write({'finished':True,'progress':100}) 
                 i.fortress_attacking.write({'soldiers': i.fortress_attacking.soldiers+i.soldiers_sent}) 
     @api.model
     def create(self, values):
        new_id = super(attack, self).create(values)
        print values
        new_id.fortress_attacking.write({'soldiers': new_id.fortress_attacking.soldiers-new_id.soldiers_sent})
        return new_id
        

     

