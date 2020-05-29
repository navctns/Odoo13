from odoo import models, fields, api
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError



class Appointment(models.Model):
    _name="hospital.appointment"
    _description="Hospital Appointment"
    _rec_name = "appointment_seq"

    card_id = fields.Many2one("patient.card", string = "Patient card", required = True)
    patient_name = fields.Char(string = "Patient name")
    doctor_id = fields.Many2one('hr.employee', required = True, domain = [('job_id', 'like', 'Doctor')])
    department_id = fields.Char(string = "Department")
    date = fields.Date(string = "Date", default = fields.Date.today())
    token = fields.Integer(string = 'Token No')
    state = fields.Selection(
        string="State",
        selection=[
            ('draft', 'Draft'),
            ('appointment', 'Appointment'),
            ('op', 'OP'),
        ], default='draft', required=True, compute = '_state_change')
    op_ids = fields.One2many('hospital.op', 'appointment_id', string="OP ids")
    op_count = fields.Integer(default =0, compute = '_compute_op_count')
    appointment_seq = fields.Char(string='Appointment Number', required=True, copy=False, readonly=True,
                                  default='New')
    active = fields.Boolean('Active', default=True)
    confirm_op = fields.Boolean(string="Confirm op", default=False)


    @api.depends('op_ids')
    def _compute_op_count(self):
        # for op in self:
        #     op.op_count = self.env['hospital.op'].search_count([('appointment_id', '=', self.id)])
        # print('op count', self.op_count)
        for r in self:
            if r.op_ids.appointment_id.id == self.id:
                self.op_count += 1
        if self.op_count == 1:
            self.state = 'op'
        print('op count', self.op_count)

    # @api.onchange('op_ids')
    # def _onchange_op_ids(self):
    #     if self.op_ids :
    #         self.state = 'op'

    @api.model
    def create(self, vals):
        if vals.get('appointment_seq', 'New') == 'New':
            vals['appointment_seq'] = self.env['ir.sequence'].next_by_code(
                'hospital.appointmentnum') or 'New'
        result = super(Appointment, self).create(vals)
        return result

    @api.onchange('op_ids')
    def _onchange_op_ids(self):
        if self.op_ids.appointment_id :
            self.state = 'op'



    @api.onchange('op_count')
    def _onchange_op_count(self):
        if self.op_count == 1 :
            # self.state = 'op'
            self.write({
                'state': 'op',
            })

    confirm = 0
    @api.depends('op_count', 'confirm_op')
    def _state_change(self):
        # if self.state != 'draft' :
        # if self.state == 'appointment':
        if self.op_count == 1:
            # self.state = 'op'
            self.write({
                'state': 'op',
            })



        elif self.confirm_op :
            self.write({
                'state': 'appointment',
            })
            self.confirm_op = False

        else :
            self.write({
                'state': 'draft',
            })

    # python constraint
    @api.constrains('token')
    def _check_token(self):
        tokens = []
        for r in self.env['hospital.op'].search([('date_op', '=', fields.Date.today())]):
            # if r.date_op == fields.Date.today():#todays tokens
            tokens.append(r.token_no)
        # print('today tokens', tokens)
        r = self.env['hospital.op'].search([('date_op', '=', fields.Date.today())])
        # if len(r) != 0:
        #     tokens[-1] = None  # because it loads the current entry also
        if self.token in tokens:
            raise ValidationError("Token number should be unique")


    # @api.depends('op_count')
    # def _compute_state(self):
    #
    #     if self.state == 'appointment':
    #         if self.op_count > 0:
    #             self.state = 'op'
    @api.onchange('appointment_seq')
    def _onchange_appointment_seq(self):

        r = self.env['hospital.op'].search([('date_op', '=', fields.Date.today())])
        print('today count', len(r))
        self.state = 'draft'

        # if len(r) == 1:
        #     # for t in self:
        #     #     if t.token != 1 :
        #     #         self.token = 1
        #     tokens_1 = []
        #
        #     for r in self.env['hospital.op'].search([('date_op', '=', fields.Date.today())]):
        #         tokens_1.append(r.token_no)
        #     if 1 not in tokens_1:
        #         self.token = 1

        if len(r) == 0:
            for i in self.env['hospital.op'].search([]):
                i.token_no = None  # delete token numbers everyday
            # set initial token of the day
            self.token = 1

        elif len(r) == 1:
            # for t in self:
            #     if t.token != 1 :
            #         self.token = 1
            tokens_1 = []

            for r in self.env['hospital.op'].search([('date_op', '=', fields.Date.today())]):
                tokens_1.append(r.token_no)
            if 1 not in tokens_1:
                self.token = 1
        else:
            existing_tokens = []

            for r in self.env['hospital.op'].search([('date_op', '=', fields.Date.today())]):
                existing_tokens.append(r.token_no)
            #token check on appointment(new add)
            for r in self.env['hospital.appointment'].search([('date', '=', fields.Date.today())]):
                existing_tokens.append(r.token)
                # check for duplication of token
            for i in sorted(existing_tokens):
                n = i + 1
                if n not in existing_tokens:
                    self.token = i + 1
                    break
            print('tokens ex', existing_tokens)


    @api.onchange('card_id')
    def _onchange_card_id(self):
        self.patient_name = self.card_id.patient_id.name

        # # get number of records today
        # r = self.env['hospital.op'].search([('date_op', '=', fields.Date.today())])
        # print('today count', len(r))
        #
        # if len(r) == 0:
        #     for i in self.env['hospital.op'].search([]):
        #         i.token = None  # delete token numbers everyday
        #     # set initial token of the day
        #     self.token = 1
        # else:
        #     existing_tokens = []
        #
        #     for r in self.env['hospital.op'].search([('date_op', '=', fields.Date.today())]):
        #         existing_tokens.append(r.token_no)
        #         # check for duplication of token
        #     for i in sorted(existing_tokens):
        #         n = i + 1
        #         if n not in existing_tokens:
        #             self.token = i + 1 #or n
        #             break
        #     print('tokens ex', existing_tokens)

    @api.onchange('doctor_id')
    def _onchange_doctor_id(self):

        self.department_id = self.doctor_id.department_id.name



    def action_confirm(self):
        confirm = 1
        # for rec in self:
        #     rec.state = 'appointment'
        self.confirm_op = True
        # self.write({
        #     'state': 'appointment',
        # })

    def action_convert_to_op(self):
        self.ensure_one()
        # if self.op_count == 1 :
        #     self.state = 'op'
        action = {

            'type': 'ir.actions.act_window',
            'card_id': self.card_id,
            'doctor_id': self.doctor_id,
        }
        return {
            'type': 'ir.actions.act_window',
            'name': 'OP Form',
            'view_mode': 'form',
            'res_model': 'hospital.op',
            'context': {'default_card_id': self.card_id.id, 'default_doctor_id': self.doctor_id.id,
                        'default_token_no':self.token, 'default_appointment_id':self.id,
                        'mark_app_as_op': True,
                        },
            # 'target': 'self',
            # 'state': 'op',
            }
    #when returning to appointment from op
    @api.returns('hospital.op', lambda value: value.id)
    def op_post(self, **kwargs):
        if self.env.context.get('mark_app_as_op'):
            self.filtered(lambda o: o.state == 'appointment').with_context(tracking_disable=True).write({'state': 'op'})
        return super(Appointment, self.with_context(op_post_autofollow=True)).message_post(**kwargs)



    #method 2
    def action_redirect_to_appointment(self):
        #check for existing tokens#
        tokens = []
        for r in self.env['hospital.op'].search([('date_op', '=', fields.Date.today())]):
            # if r.date_op == fields.Date.today():#todays tokens
            tokens.append(r.token_no)
        print('today tokens', tokens)
        r = self.env['hospital.op'].search([('date_op', '=', fields.Date.today())])
        # if len(r) != 0:
        #     tokens[-1] = None  # because it loads the current entry also
        if self.token in tokens:
            raise ValidationError("Token number should be unique")
        #end check for existing tokens
        else:
            action = self.env.ref('hospital_management.action_patientcard').read()[0]
            # action['domain'] = [('campaign_id', '=', self.id)]
            action['context'] = {'default_card_id': self.card_id.id, 'default_doctor_id': self.doctor_id.id,
                                 'default_token_no':self.token}
            #write return action for appointment with context
            action['views'] = 'form_view'

            return action
    #method 2

    # @api.constrains('token')
    # def _check_token(self):
    #     tokens = []
    #     for r in self.env['hospital.op'].search([('date_op', '=', fields.Date.today())]):
    #         # if r.date_op == fields.Date.today():#todays tokens
    #         tokens.append(r.token_no)
    #     print('today tokens', tokens)
    #     r = self.env['hospital.op'].search([('date_op', '=', fields.Date.today())])
    #     if len(r) != 0:
    #         tokens[-1] = None  # because it loads the current entry also
    #     if self.token in tokens:
    #         raise ValidationError("Token number should be unique")


    def get_ops(self):

        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'OPs',
            'view_mode': 'form',
            'res_model': 'hospital.op',
            # 'domain': "[('id', 'in', " + str(self.op_ids.ids) + ")]",
            'domain': [('appointment_id', '=', self.id)]
            # 'context': {'default_card_id': self.card_id.id, 'default_doctor_id': self.doctor_id.id,
            #                      'default_token_no':self.token},

        }

        #method 2
    def get_ops_form(self):
        # action = self.env.ref('hospital_management.action_patientcard').read()[0]
        # action['view_mode'] = 'form'
        #
        # action['domain'] = [('card_id', '=', self.card_id)]
        # return action
        '''
        action = self.env.ref('hospital_management.action_patientcard').read()[0]

        action['views'] = [
            (self.env.ref('hospital_management.op_form_view').id, 'form'),
        ]
        action['domain'] = [('appointment_id','=',self.id)]
        action['context'] = action.context
        '''
        op_obj = self.env['hospital.op'].search([('appointment_id', '=', self.id)])
        op_ids = []
        for each in op_obj:
            op_ids.append(each.id)

        view_id = self.env.ref('hospital_management.op_form_view').id
        ctx = dict(
            create=False,

        )

        if op_ids:
            if len(op_ids) <= 1:
                value = {
                    'view_mode': 'form',
                    'res_model': 'hospital.op',
                    'view_id': view_id,
                    'type': 'ir.actions.act_window',
                    'name': 'Op',
                    'context': ctx,
                    'res_id': op_ids and op_ids[0]
                }
            else:
                value = {
                    'domain': str([('id', 'in', op_ids)]),
                    'view_mode': 'tree,form',
                    'res_model': 'hospital.op',
                    'view_id': False,
                    'type': 'ir.actions.act_window',
                    'context': ctx,
                    'name': 'Op',
                    'res_id': op_ids
                }

        return value

