from odoo import models,fields

class ITIStudent(models.Model):
    _name ="iti_student"


    name = fields.Char()
    age = fields.Integer()

    gender = fields.Selection([("Male","Male"),("Female","female")])
    date_birth=fields.Date()

    is_accepted = fields.Boolean()
    cv = fields.Html()

    salary =fields.Float()