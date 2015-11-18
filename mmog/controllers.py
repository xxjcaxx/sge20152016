# -*- coding: utf-8 -*-
from openerp import http

# class Mmog(http.Controller):
#     @http.route('/mmog/mmog/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mmog/mmog/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mmog.listing', {
#             'root': '/mmog/mmog',
#             'objects': http.request.env['mmog.mmog'].search([]),
#         })

#     @http.route('/mmog/mmog/objects/<model("mmog.mmog"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mmog.object', {
#             'object': obj
#         })