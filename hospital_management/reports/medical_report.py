from odoo import models, fields, api
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta


class PatientMedicalReport(models.Model):
    _name = 'report.hospital_management.report_hospital_patient_medical'

    def _get_patient_name(self):
        res = []
        for patient in self.env['patient.card'].search([]):
            res.append({'name': patient.patient_id.name})
        return res

    @api.model
    def _get_report_values(self, docids, data = None):
        medical_report = self.env['ir.actions.report']._get_report_from_name('hospital_management.report_hospital_patient_medical')
        docs = self.env['patient.card'].browse(self.ids)
        # return {
        #     'doc_ids': self.ids,
        #     'doc_model': medical_report.model,
        #     'docs': docs,
        #     # 'proforma': True
        # }
        print("model:",medical_report.model)
        docargs = {
            'doc_ids': docids,
            'doc_model': medical_report.model,
            # 'docs':docs,
            # 'docs': self,
            'get_patient_name':self._get_patient_name(),

        }
        return docargs