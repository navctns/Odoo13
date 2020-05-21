from odoo import models, fields, api
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import tools


# class PatientMedicalReport(models.Model):
#     _name = 'report.hospital_management.report_hospital_patient_medical'
#
#     seq = fields.Char(string='Patient Reference', readonly=True)
#     patient_id=fields.Many2one("res.partner",string="Patient Name",readonly=True)
#     patient_card_id = fields.Many2one('patient.card', 'Patient #', readonly=True)
#
#     def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
#         with_ = ("WITH %s" % with_clause) if with_clause else ""
#
#         select_ = """
#
#             pc.seq as seq,
#             pc.patient_id as patient_id,
#             pc.id as patient_card_id
#         """
#
#         from_ = """
#
#             patient_card pc
#                 join res_partner partner on pc.patient_id = partner.id
#             %s
#         """ % from_clause
#
#         groupby_ = """
#                     pc.seq,
#                     pc.patient_id,
#                     pc.id %s
#                 """ % (groupby)
#
#         return '%s (SELECT %s FROM %s  GROUP BY %s)' % (with_, select_, from_, groupby_)
#
#     def init(self):
#         # self._table = sale_report
#         # tools.drop_view_if_exists(self.env.cr, self._table)
#         self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query()))
#
#     def _get_patient_name(self):
#         res = []
#         for patient in self.env['patient.card'].search([('id','=',self.id)]):
#             res.append({'name': patient.patient_id.name})
#         return res
#
#     @api.model
#     def _get_report_values(self, docids, data):
#
#         # model_id = data['model_id']
#         # value = []
#         # query = """SELECT *
#         #     FROM patient_card as pc
#         #     WHERE pc.id = %s"""
#         # value.append(model_id)
#         # self._cr.execute(query, value)
#         # record = self._cr.dictfetchall()
#         # return {
#         #     'docs': record,
#         #     # 'date_today': fields.Datetime.now(),
#         # }
#         """
#         # return {
#         #     'doc_ids': self.ids,
#         #     'doc_model': medical_report.model,
#         #     'docs': docs,
#         #     # 'proforma': True
#         # }
#         """
#         medical_report = self.env['ir.actions.report']._get_report_from_name('hospital_management.report_hospital_patient_medical')
#         print("model:",medical_report.model)
#         docargs = {
#             'doc_ids': docids,
#             'doc_model': medical_report.model,
#             # 'docs':docs,
#             # 'docs': self,
#             'get_patient_name':self._get_patient_name(),
#
#         }
#         return docargs

class PatientMedicalReport(models.Model):
    _name = 'report.hospital'

    seq = fields.Char(string='Patient Reference', readonly=True)
    patient_id = fields.Many2one("res.partner", string="Patient Name", readonly=True)
    patient_card_id = fields.Many2one('patient.card', 'Patient #', readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        with_ = ("WITH %s" % with_clause) if with_clause else ""

        select_ = """

            pc.seq as seq,
            pc.patient_id as patient_id,
            pc.id as patient_card_id
        """

        from_ = """

            patient_card pc
                join res_partner partner on pc.patient_id = partner.id
            %s
        """ % from_clause

        groupby_ = """
                    pc.seq,
                    pc.patient_id,
                    pc.id %s 
                """ % (groupby)

        return '%s (SELECT %s FROM %s  GROUP BY %s)' % (with_, select_, from_, groupby_)

    def init(self):
        # self._table = sale_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query()))

    def _get_patient_name(self):
        res = []
        for patient in self.env['patient.card'].search([('id', '=', self.id)]):
            res.append({'name': patient.patient_id.name})
        return res

    @api.model
    def _get_report_values(self, docids, data):
        # model_id = data['model_id']
        # value = []
        # query = """SELECT *
        #     FROM patient_card as pc
        #     WHERE pc.id = %s"""
        # value.append(model_id)
        # self._cr.execute(query, value)
        # record = self._cr.dictfetchall()
        # return {
        #     'docs': record,
        #     # 'date_today': fields.Datetime.now(),
        # }
        """
        # return {
        #     'doc_ids': self.ids,
        #     'doc_model': medical_report.model,
        #     'docs': docs,
        #     # 'proforma': True
        # }
        """
        medical_report = self.env['ir.actions.report']._get_report_from_name(
            'hospital_management.report_hospital_patient_medical')
        print("model:", medical_report.model)
        docargs = {
            'doc_ids': docids,
            'doc_model': medical_report.model,
            # 'docs':docs,
            # 'docs': self,
            'get_patient_name': self._get_patient_name(),

        }
        return docargs



