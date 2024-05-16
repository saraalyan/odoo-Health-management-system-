from odoo import models, fields, api
from odoo.exceptions import UserError


class Customer(models.Model):
    _inherit = 'res.partner'
    related_patient_id = fields.Many2one('hms.patient')
    # vat = fields.char(required = True)

    # @api.constrains('related_patient_id')
    # def _check_patient_mail(self):
    #     if self.email == self.related_patient_id.Email:
    #         raise UserError("Can't be Linking, Existing E-mail!")
    @api.constrains('related_patient_id')
    def _check_patient_email_unique(self):
        for customer in self:
            if customer.related_patient_id and customer.email:
                existing_customer = self.env['res.partner'].search([
                    ('related_patient_id.Email', '=', customer.related_patient_id.Email),
                    ('id', '!=', customer.id)
                ])
                if existing_customer:
                    raise UserError(
                        "Cannot link a patient with an email that is already assigned to a different customer.")

    def unlink(self):
        if self.related_patient_id:
            raise UserError("You can't delete this customer")
        super().unlink()
