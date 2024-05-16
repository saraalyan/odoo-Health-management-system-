from odoo import models, fields


class Department(models.Model):
    _name = 'hms.doctor'
    _rec_name = 'doctor_name_frist'

    doctor_name_frist = fields.Char()
    doctor_name_last = fields.Char()
    doctor_image = fields.Binary('image')

