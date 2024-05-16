from odoo import models, fields,api
from odoo.exceptions import  ValidationError
from datetime import date
class log_history(models.Model):
    _name = 'hms.log.history'

    Description = fields.Text()
    patient_id = fields.Many2one('hms.patient')
class HMS(models.Model):
    _name = 'hms.patient'
    _rec_name='firstName'

    firstName = fields.Char(required=True)
    lastName = fields.Char(required=True)
    Email = fields.Char()
    date_birth = fields.Date()
    history = fields.Html()
    cr_ratio = fields.Float()
    address = fields.Text()
    age = fields.Integer(compute='_compute_age', store=True)
    blood_type = fields.Selection([
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('O', 'O'),])
    pcr = fields.Boolean()
    image = fields.Binary('image')
    state = fields.Selection([
        ('undetermined', 'undetermined'),
        ('good', 'good'),
        ('fair', 'fair'),
        ('serious', 'serious'),
    ], default='undetermined')
    department_name_id = fields.Many2one('hms.department')
    department_capacity = fields.Integer(related='department_name_id.Capacity')
    doctor_name_id = fields.Many2many('hms.doctor')

    @api.onchange('age')
    def changeAge(self):
        if self.age and self.age < 30:
            self.pcr = True
            return {
                'warning' : {
                    'message' : 'Pcr Automatic select if age < 30 ' ,
                }
            }
    log_history_id = fields.One2many('hms.log.history', 'patient_id')
#-----------------------------------


    def change_state(self):
        for patient in self:
            if patient.state == 'undetermined':
                patient.state = 'good'
            elif patient.state == 'good':
                patient.state = 'fair'
            elif patient.state == 'fair':
                patient.state = 'serious'

    @api.onchange('state')
    def create_state_log(self):
        if self.state:
            vals = {
                'Description': 'change state to %s' % (self.state),
                'patient_id': self.id,
            }
            self.env['hms.log.history'].create(vals)

    # @api.constrains('age')
    # def check_age(self):
    #     if self.age < 50:
    #         raise ValidationError('patient Age can\'t be less than 50')
    @api.depends('date_birth')
    def _compute_age(self):
        for rec in self:
            if rec.date_birth:
                today = date.today()
                rec.age = today.year - rec.date_birth.year - (
                        (today.month, today.day) < (rec.date_birth.month, rec.date_birth.day))

            else:
                rec.age = 40
