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
        format1.set_align('center')
        format2.set_align('center')
        sheet = workbook.add_worksheet('Patient Report')
        # sheet.merge_range(0, 7, 'Medical Report', format1)
        # sheet.set_column(0, 0, 50)#column width method dropped
        # sheet.write(0, 0, 'Medical Report', format1)#column width method dropped
        sheet.merge_range(0, 0, 1, 16, 'Medical Report', format1)#by merging
        # cols = {'p':0,'dis':0,'doc':0,'dep':0} #Not used
        lcols = [0,0,0,0]#for pointing patient disease doct dept
        lcol_label=['Patient','Disease','Doctor','Department']
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
            lcols[0] = 1
        if 'disease' in head_info :
            disease = 'Disease :' + str(header_values['disease']) + ', '
            lcols[1] = 1
        if 'doct' in head_info :
            doct = 'Doctor :' + str(header_values['doct']) + ', '
            lcols[2] = 1
        if 'dept' in head_info :
            dept = 'Department :' + str(header_values['dept']) + ', '
            lcols[3] = 1
        if 'from_dt' in head_info :
            from_dt = 'From :' + str(header_values['from_dt']) + ', '
        if 'date_to' in head_info :
            date_to = 'To :' + str(header_values['date_to'])

        info_str = '(' + patient + disease + doct + dept + from_dt + date_to +')'
        sheet.merge_range(2, 0, 3, 16, info_str, format2)
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
        # sheet.set_column(i, 0, 20)
        #merge and write
        sheet.write(4, 0, 'Serial', format1)#test
        # sheet.merge_range(4, 0, 4, 1, 'Serial', format2)
        #change order
        sheet.merge_range(4, 1, 4, 3, 'Date', format1)
        sheet.merge_range(4, 4, 4, 6, 'OP', format1)

        i = 4
        j = 7
        for k in range(len(lcols)) :
            if lcols[k] == 0 :
                str_val = lcol_label[k]
                sheet.merge_range(i, j, i, j+2, str_val , format1)
                j = j + 3

        #THIRD Method with flexible columns###############################
        i = 5  # for adding data in lines
        for op in ops:
            num = op['num']
            seq = op['seq']
            date = op['date']
            patient = op['patient']
            disease = op['disease']
            doctor = op['doctor']
            department = op['department']

            spe_cols= []#list contents
            #storing current record values to list
            if lcols[0]== 0 :
                spe_cols.append(patient)
            if lcols[1]== 0 :
                spe_cols.append(disease)
            if lcols[2]== 0 :
                spe_cols.append(doctor)
            if lcols[3]== 0 :
                spe_cols.append(department)

            #Abandoned################
            # sheet.write(i, 0, num, format2)
            # sheet.write(i, 1, seq, format2)
            # sheet.write(i, 2, date, format2)
            # sheet.write(i, 3, patient, format2)
            # sheet.write(i, 4, disease, format2)
            # sheet.write(i, 5, doctor, format2)
            # sheet.write(i, 6, department, format2)
            # Abandoned################
            num_val = str(num)
            date_val = str(date)
            seq_val = str(seq)

            sheet.write(i, 0, num, format2)
            sheet.merge_range(i, 1, i, 3, date_val, format2)
            sheet.merge_range(i,4,i, 6, seq_val, format2)


            #TEST###################
            # spe_cols = []  # empty list contents for next records
            # i = 5

            # val = str(k)
            # sheet.write(i,7,patient,format2)
            #TEST#############
            j = 7
            for k in spe_cols:
                val = str(k)
                sheet.merge_range(i, j, i, j + 2, val, format2)
                j = j + 3
                # if lcols[k] == 0:
                #     str_val = lcol_label[k]
                #     sheet.merge_range(i, j, i, j + 2, str_val, format1)
                #     j = j + 3
            i = i+ 1
        #################################################3333
        # sheet.merge_range(4, 6, 4, 8, 'Patient', format2)
        # sheet.merge_range(4, 9, 4, 11, 'Disease', format2)
        # sheet.merge_range(4, 12, 4, 14, 'Doctor', format2)
        # sheet.merge_range(4, 15, 4, 17, 'Department', format2)

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
        # FIRST METHOD- Working fine
        # i = 5  # for adding data in lines
        # for op in ops:
        #     num = op['num']
        #     seq = op['seq']
        #     date = op['date']
        #     patient = op['patient']
        #     disease = op['disease']
        #     doctor = op['doctor']
        #     department = op['department']
        #
        #     # sheet.write(i, 0, num, format2)
        #     # sheet.write(i, 1, seq, format2)
        #     # sheet.write(i, 2, date, format2)
        #     # sheet.write(i, 3, patient, format2)
        #     # sheet.write(i, 4, disease, format2)
        #     # sheet.write(i, 5, doctor, format2)
        #     # sheet.write(i, 6, department, format2)
        #     sheet.write(i, 0, num, format2)
        #     sheet.merge_range(i, 1, i, 3, seq, format2)
        #     sheet.merge_range(i,4,i, 5, date, format2)
            #####method 2

            # if patient != '':
            #     if disease == '' :
            #         sheet.merge_range(i, 6, i, 8, patient, format2)
            #     elif doct == '':
            #         sheet.merge_range(i, 6, i, 8, disease, format2)
            #     elif dept == '' :
            #         sheet.merge_range(i, 6, i, 8, department, format2)
            # else:
            #     sheet.merge_range(i, 6, i, 8, patient, format2)
            #
            # if disease != '' :
            #     if patient!= '' :
            #         if doct == '' :
            #             sheet.merge_range(i, 6, i, 8, doctor, format2)
            #         elif dept == '' :
            #             sheet.merge_range(i, 6, i, 6, department, format2)
            #     else :
            #         if doct == '' :
            #             sheet.merge_range(i, 9, i, 11, doctor, format2)
            #         elif dept == '' :
            #             sheet.merge_range(i, 9, i, 11, department, format2)
            # else :
            #     if patient == '' :
            #         sheet.merge_range(i, 9, i, 11, disease, format2)
            #
            # if
            #
            # #######3#####
            # if patient == '':
            #     sheet.merge_range(i, 6, i, 8, patient, format2)
            #     sheet.merge_range(i, 9, i, 11, disease, format2)
            # else :
            #     sheet.merge_range(i, 6, i, 8, disease, format2)
            #
            # if disease == '' :
            #     if patient == '' :
            #         sheet.merge_range(i, 9, i, 11, disease, format2)
            #         sheet.merge_range(i, 12, i, 14, doctor, format2)
            #     else :
            #         sheet.merge_range(i, 9, i, 11, doctor, format2)
            # else :
            #
            #
            # sheet.merge_range(i, 12, i, 14, doctor, format2)
            # sheet.merge_range(i, 15, i, 17, department, format2)
            #
            # i += 1