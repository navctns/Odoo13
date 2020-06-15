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
        header_values=data['header_vals']
        print(header_values)
        # seq = ops['seq'] #two slices
        # for i in range(1) :
        #     seq = ops[i]['seq']
        # data_1 = data['ops']
        format1 = workbook.add_format({'font_size':16, 'align':'vcenter','bold':True})
        format2 = workbook.add_format({'font_size': 14, 'align': 'vcenter'})
        sheet = workbook.add_worksheet('Patient Report')
        # sheet.merge_range(0, 7, 'Medical Report', format1)
        sheet.merge_range(0, 0, 1, 30, 'Medical Report', format1)
        ##SET header values#######
        patient = ''
        disease = ''
        doct = ''
        dept = ''
        from_dt = ''
        date_to = ''
        head_info = header_values.keys()
        if 'patient' in head_info :
            patient = 'Patient :' + str(header_values['patient']) + ', '
        if 'disease' in head_info :
            disease = 'Disease :' + str(header_values['disease']) + ', '
        if 'doct' in head_info :
            doct = 'Doctor :' + str(header_values['doct']) + ', '
        if 'dept' in head_info :
            dept = 'Department :' + str(header_values['dept']) + ', '
        if 'from_dt' in head_info :
            from_dt = 'From :' + str(header_values['from_dt']) + ', '
        if 'date_to' in head_info :
            date_to = 'To :' + str(header_values['date_to'])

        info_str = '(' + patient + disease + doct + dept + from_dt + date_to +')'
        sheet.merge_range(2, 0, 2, 30, info_str, format2)
        # sheet.merge_range(3, 0, 3, 30).write(patient,format2)

        # Setting the column width
        # sheet.set_column(4, 0, 10)
        # sheet.set_column(4, 1, 30)
        # sheet.set_column(4, 2, 30)
        # sheet.set_column(4, 3, 30)
        # sheet.set_column(4, 4, 30)
        # sheet.set_column(4, 5, 30)
        # sheet.set_column(4, 6, 30)
        # #write data
        # sheet.write(4, 0, 'Serial', format1)
        # sheet.write(4, 1, 'OP', format1)
        # sheet.write(4, 2, 'Date', format1)
        # sheet.write(4, 3, 'Patient', format1)
        # sheet.write(4, 4, 'Disease', format1)
        # sheet.write(4, 5, 'Doctor', format1)
        # sheet.write(4, 6, 'Department', format1)
        # # sheet.write(1, 1, seq, format1)
        #
        #
        # i = 5 #for adding data in lines
        # for op in ops :
        #
        #     num = op['num']
        #     seq = op['seq']
        #     date = op['date']
        #     patient = op['patient']
        #     disease = op['disease']
        #     doctor = op['doctor']
        #     department = op['department']
        #
        #     sheet.write(i, 0, num, format2)
        #     sheet.write(i, 1, seq, format2)
        #     sheet.write(i, 2, date, format2)
        #     sheet.write(i, 3, patient, format2)
        #     sheet.write(i, 4, disease, format2)
        #     sheet.write(i, 5, doctor, format2)
        #     sheet.write(i, 6, department, format2)
        #
        #     i += 1
        ##############################################
        # for obj in partners:
        #     report_name = obj.name
        #     # One sheet by partner
        #     sheet = workbook.add_worksheet(report_name[:31])
        #     bold = workbook.add_format({'bold': True})
        #     sheet.write(0, 0, obj.name, bold)

        #Modifying code with merging method

        #merge and write
        sheet.write(4, 0, 'Serial', format1)
        # sheet.merge_range(4, 0, 4, 1, 'Serial', format2)
        sheet.merge_range(4, 2, 4, 4, 'OP', format2)
        sheet.merge_range(4, 5, 4, 6, 'Date', format2)
        sheet.merge_range(4, 7, 4, 9, 'Patient', format2)
        sheet.merge_range(4, 10, 4, 12, 'Disease', format2)
        sheet.merge_range(4, 13, 4, 15, 'Doctor', format2)
        sheet.merge_range(4, 16, 4, 18, 'Department', format2)
        #set colum width
        # sheet.set_column(4, 0, 10)
        # sheet.set_column(4, 1, 30)
        # sheet.set_column(4, 2, 30)
        # sheet.set_column(4, 3, 30)
        # sheet.set_column(4, 4, 30)
        # sheet.set_column(4, 5, 30)
        # sheet.set_column(4, 6, 30)
        # # write data
        # sheet.write(4, 0, 'Serial', format1)
        # sheet.write(4, 1, 'OP', format1)
        # sheet.write(4, 2, 'Date', format1)
        # sheet.write(4, 3, 'Patient', format1)
        # sheet.write(4, 4, 'Disease', format1)
        # sheet.write(4, 5, 'Doctor', format1)
        # sheet.write(4, 6, 'Department', format1)
        # # sheet.write(1, 1, seq, format1)
        #
        i = 5  # for adding data in lines
        for op in ops:
            num = op['num']
            seq = op['seq']
            date = op['date']
            patient = op['patient']
            disease = op['disease']
            doctor = op['doctor']
            department = op['department']

            # sheet.write(i, 0, num, format2)
            # sheet.write(i, 1, seq, format2)
            # sheet.write(i, 2, date, format2)
            # sheet.write(i, 3, patient, format2)
            # sheet.write(i, 4, disease, format2)
            # sheet.write(i, 5, doctor, format2)
            # sheet.write(i, 6, department, format2)
            sheet.merge_range(i, 2, i, 4, 'OP', format2)
            sheet.merge_range(i,5,i, 6, 'Date', format2)
            sheet.merge_range(i, 7, i, 9, 'Patient', format2)
            sheet.merge_range(i, 10, i, 12, 'Disease', format2)
            sheet.merge_range(i, 13, i, 15, 'Doctor', format2)
            sheet.merge_range(i, 16, i, 18, 'Department', format2)

            i += 1