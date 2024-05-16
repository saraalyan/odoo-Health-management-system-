from odoo import models, fields,api
from odoo.exceptions import ValidationError

class Department(models.Model):
    _name = 'hms.department'
    _rec_name = 'Department_name'

    Department_name = fields.Char()
    Capacity = fields.Integer()
    is_opened = fields.Boolean()
    patient_ids = fields.One2many('hms.patient', 'department_name_id')
    @api.constrains('Capacity')
    def check_Capacity(self):
        if self.Capacity < 50:
            raise ValidationError('Capacity Age can\'t be less than 50')

    _sql_constraints = [
        ('unique_department_name1', 'UNIQUE(Department_name)', 'Department name should be unique')
    ]

