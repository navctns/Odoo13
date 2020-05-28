from odoo import models, fields, api
import datetime
import time
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import tools
from odoo.exceptions import UserError

class PatientMedicalReportXlsx(models.AbstractModel):
    _name = 'report.hospital_management.hospital_patient_medical_report_xls'
    _inherit = 'report.odoo_report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, lines):
        print(data)
        ops = data['ops']
        print('ops', ops)
        # seq = ops['seq'] #two slices
        for i in range(1) :
            seq = ops[i]['seq']
        data_1 = data['ops']
        format1 = workbook.add_format({'font_size':16, 'align':'vcenter','bold':True})
        format2 = workbook.add_format({'font_size': 14, 'align': 'vcenter'})
        sheet = workbook.add_worksheet('Patient Report')
        sheet.write(0, 0, 'Serial', format1)
        sheet.write(0, 1, 'OP', format1)
        sheet.write(0, 2, 'Date', format1)
        sheet.write(0, 3, 'Patient', format1)
        sheet.write(0, 4, 'Disease', format1)
        sheet.write(0, 5, 'Doctor', format1)
        sheet.write(0, 6, 'Department', format1)
        sheet.write(1, 1, seq, format1)
        # for obj in partners:
        #     report_name = obj.name
        #     # One sheet by partner
        #     sheet = workbook.add_worksheet(report_name[:31])
        #     bold = workbook.add_format({'bold': True})
        #     sheet.write(0, 0, obj.name, bold)
