# -*- coding: utf-8 -*-
from openerp import http

# class Conservatori(http.Controller):
#     @http.route('/conservatori/conservatori/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/conservatori/conservatori/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('conservatori.listing', {
#             'root': '/conservatori/conservatori',
#             'objects': http.request.env['conservatori.conservatori'].search([]),
#         })

#     @http.route('/conservatori/conservatori/objects/<model("conservatori.conservatori"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('conservatori.object', {
#             'object': obj
#         })