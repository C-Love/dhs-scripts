# client-contact
import datetime

import wx
import wx.xrc
# ADD widget classes here


# now = datetime.datetime.now()

# contact_time = now.strftime("%m-%d-%Y %H:%M")

###########################################################################
# Class MAXISClientContact
###########################################################################

class MAXISClientContact (wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Client Contact", pos=wx.DefaultPosition, size=wx.Size(-1, -1), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer2 = wx.BoxSizer(wx.VERTICAL)

        self.m_panel2 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        gbSizer1 = wx.GridBagSizer(0, 0)
        gbSizer1.SetFlexibleDirection(wx.BOTH)
        gbSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.textContactType = wx.StaticText(self.m_panel2, wx.ID_ANY, u"Contact type:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.textContactType.Wrap(-1)
        gbSizer1.Add(self.textContactType, wx.GBPosition(0, 0), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_RIGHT, 5)

        combo_contact_typeChoices = [u"Phone call", u"Voicemail", u"Email", u"Office visit", u"Letter"]
        self.combo_contact_type = wx.ComboBox(self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, combo_contact_typeChoices, 0)
        gbSizer1.Add(self.combo_contact_type, wx.GBPosition(0, 1), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        choice_contact_dirChoices = [u"from", u"to"]
        self.choice_contact_dir = wx.Choice(self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choice_contact_dirChoices, 0)
        self.choice_contact_dir.SetSelection(0)
        gbSizer1.Add(self.choice_contact_dir, wx.GBPosition(0, 2), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        combo_contact_personChoices = [u"Client", u"AREP", u"Non-AREP", u"SWKR", u"Facility", u"Employer", u"Landlord", u"Utility Company"]
        self.combo_contact_person = wx.ComboBox(self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, combo_contact_personChoices, 0)
        gbSizer1.Add(self.combo_contact_person, wx.GBPosition(0, 3), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.text_regarding = wx.StaticText(self.m_panel2, wx.ID_ANY, u"Re:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_regarding.Wrap(-1)
        gbSizer1.Add(self.text_regarding, wx.GBPosition(1, 0), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_RIGHT, 5)

        self.editbox_regarding = wx.TextCtrl(self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.editbox_regarding, wx.GBPosition(1, 1), wx.GBSpan(1, 3), wx.ALL | wx.EXPAND, 5)

        self.text_PhonteNumber = wx.StaticText(self.m_panel2, wx.ID_ANY, u"Phone Number:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_PhonteNumber.Wrap(-1)
        gbSizer1.Add(self.text_PhonteNumber, wx.GBPosition(2, 0), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_RIGHT, 5)

        combo_phone_numberChoices = [u"651-555-1234"]
        self.combo_phone_number = wx.ComboBox(self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, combo_phone_numberChoices, 0)
        gbSizer1.Add(self.combo_phone_number, wx.GBPosition(2, 1), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.text_DateTime = wx.StaticText(self.m_panel2, wx.ID_ANY, u"Date/Time of Contact:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_DateTime.Wrap(-1)
        gbSizer1.Add(self.text_DateTime, wx.GBPosition(2, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.editbox_date_time = wx.TextCtrl(self.m_panel2, wx.ID_ANY, now_time, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.editbox_date_time, wx.GBPosition(2, 3), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.text_CaseNumber = wx.StaticText(self.m_panel2, wx.ID_ANY, u"Case number:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_CaseNumber.Wrap(-1)
        gbSizer1.Add(self.text_CaseNumber, wx.GBPosition(3, 0), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_RIGHT, 5)

        self.editbox_MAXIS_case_number = wx.TextCtrl(self.m_panel2, wx.ID_ANY, MAXIS_case_number, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.editbox_MAXIS_case_number, wx.GBPosition(3, 1), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.checkbox_used_interpreter = wx.CheckBox(self.m_panel2, wx.ID_ANY, u"Used Interpreter", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.checkbox_used_interpreter, wx.GBPosition(3, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.text_mnsureICNumber = wx.StaticText(self.m_panel2, wx.ID_ANY, u"MNSure IC number:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_mnsureICNumber.Wrap(-1)
        gbSizer1.Add(self.text_mnsureICNumber, wx.GBPosition(4, 0), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_RIGHT, 5)

        self.editbox_mets_ic_number = wx.TextCtrl(self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.editbox_mets_ic_number, wx.GBPosition(4, 1), wx.GBSpan(1, 1), wx.ALL | wx.EXPAND, 5)

        self.text_ContactReason = wx.StaticText(self.m_panel2, wx.ID_ANY, u"Reason for Contact:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_ContactReason.Wrap(-1)
        gbSizer1.Add(self.text_ContactReason, wx.GBPosition(5, 0), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_RIGHT, 5)

        self.editbox_contact_reason = wx.TextCtrl(self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.editbox_contact_reason, wx.GBPosition(5, 1), wx.GBSpan(1, 3), wx.ALL | wx.EXPAND, 5)

        self.text_ActionTaken = wx.StaticText(self.m_panel2, wx.ID_ANY, u"Action taken:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_ActionTaken.Wrap(-1)
        gbSizer1.Add(self.text_ActionTaken, wx.GBPosition(6, 0), wx.GBSpan(1, 1), wx.ALL | wx.ALIGN_RIGHT, 5)

        self.editbox_action_taken = wx.TextCtrl(self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.editbox_action_taken, wx.GBPosition(6, 1), wx.GBSpan(1, 3), wx.ALL | wx.EXPAND, 5)

        sbSizer1 = wx.StaticBoxSizer(wx.StaticBox(self.m_panel2, wx.ID_ANY, u"Helpful info for call centers (or front desks) to pass on to clients"), wx.VERTICAL)

        fgSizer1 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer1.AddGrowableCol(1)
        fgSizer1.SetFlexibleDirection(wx.BOTH)
        fgSizer1.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.text_VerifsNeeded = wx.StaticText(sbSizer1.GetStaticBox(), wx.ID_ANY, u"Verifs needed:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_VerifsNeeded.Wrap(-1)
        fgSizer1.Add(self.text_VerifsNeeded, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        self.editbox_verifs_needed = wx.TextCtrl(sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer1.Add(self.editbox_verifs_needed, 0, wx.ALL | wx.EXPAND, 5)

        self.text_CaseStatus = wx.StaticText(sbSizer1.GetStaticBox(), wx.ID_ANY, u"Case status:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_CaseStatus.Wrap(-1)
        fgSizer1.Add(self.text_CaseStatus, 0, wx.ALL | wx.ALIGN_RIGHT, 5)

        self.editbox_case_status = wx.TextCtrl(sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer1.Add(self.editbox_case_status, 0, wx.ALL | wx.EXPAND, 5)

        self.text_InstrucMsg = wx.StaticText(sbSizer1.GetStaticBox(), wx.ID_ANY, u"Instructions.message:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_InstrucMsg.Wrap(-1)
        fgSizer1.Add(self.text_InstrucMsg, 0, wx.ALL, 5)

        self.editbox_instructions = wx.TextCtrl(sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer1.Add(self.editbox_instructions, 0, wx.ALL | wx.EXPAND, 5)

        sbSizer1.Add(fgSizer1, 1, wx.EXPAND, 5)

        gbSizer1.Add(sbSizer1, wx.GBPosition(7, 0), wx.GBSpan(3, 4), wx.EXPAND, 5)

        self.checkbox_tikl = wx.CheckBox(self.m_panel2, wx.ID_ANY, u"Check here if you want to TIKL out for this case after the case note is done.", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.checkbox_tikl, wx.GBPosition(10, 0), wx.GBSpan(1, 4), wx.ALL, 5)

        self.checkbox_CAF1_reminder = wx.CheckBox(self.m_panel2, wx.ID_ANY, u"Check here if you reminded client about the importance of the CAF 1. ", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.checkbox_CAF1_reminder, wx.GBPosition(11, 0), wx.GBSpan(1, 4), wx.ALL, 5)

        self.checkbox_forms_to_AREP = wx.CheckBox(self.m_panel2, wx.ID_ANY, u"Check here if you sent forms to AREP.", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.checkbox_forms_to_AREP, wx.GBPosition(12, 0), wx.GBSpan(1, 4), wx.ALL, 5)

        self.checkbox_follow_up = wx.CheckBox(self.m_panel2, wx.ID_ANY, u"Check here if follow-up is needed.", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.checkbox_follow_up, wx.GBPosition(13, 0), wx.GBSpan(1, 4), wx.ALL, 5)

        self.checkbox_callback = wx.CheckBox(self.m_panel2, wx.ID_ANY, u"Check here if you left a voicemail requesting a call back.", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.checkbox_callback, wx.GBPosition(14, 0), wx.GBSpan(1, 4), wx.ALL, 5)

        sbSizer2 = wx.StaticBoxSizer(wx.StaticBox(self.m_panel2, wx.ID_ANY, u"Call Center:"), wx.VERTICAL)

        self.checkbox_callctr_answered = wx.CheckBox(sbSizer2.GetStaticBox(), wx.ID_ANY, u"Answered caller's question.", wx.DefaultPosition, wx.DefaultSize, 0)
        sbSizer2.Add(self.checkbox_callctr_answered, 0, wx.ALL, 5)

        self.checkbox_callctr_transfer = wx.CheckBox(sbSizer2.GetStaticBox(), wx.ID_ANY, u"Transferred caller to Worker.", wx.DefaultPosition, wx.DefaultSize, 0)
        sbSizer2.Add(self.checkbox_callctr_transfer, 0, wx.ALL, 5)

        gbSizer1.Add(sbSizer2, wx.GBPosition(16, 0), wx.GBSpan(2, 2), wx.EXPAND, 5)

        self.text_SignNote = wx.StaticText(self.m_panel2, wx.ID_ANY, u"Sign your case note:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_SignNote.Wrap(-1)
        gbSizer1.Add(self.text_SignNote, wx.GBPosition(18, 0), wx.GBSpan(1, 2), wx.ALL | wx.ALIGN_RIGHT, 5)

        self.editbox_worker_signature = wx.TextCtrl(self.m_panel2, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer1.Add(self.editbox_worker_signature, wx.GBPosition(18, 2), wx.GBSpan(1, 2), wx.ALL | wx.EXPAND, 5)

        m_sdbSizer1 = wx.StdDialogButtonSizer()
        self.m_sdbSizer1OK = wx.Button(self.m_panel2, wx.ID_OK)
        m_sdbSizer1.AddButton(self.m_sdbSizer1OK)
        self.m_sdbSizer1Cancel = wx.Button(self.m_panel2, wx.ID_CANCEL)
        m_sdbSizer1.AddButton(self.m_sdbSizer1Cancel)
        m_sdbSizer1.Realize()

        gbSizer1.Add(m_sdbSizer1, wx.GBPosition(19, 2), wx.GBSpan(1, 2), wx.EXPAND, 5)

        self.m_panel2.SetSizer(gbSizer1)
        self.m_panel2.Layout()
        gbSizer1.Fit(self.m_panel2)
        bSizer2.Add(self.m_panel2, 1, wx.EXPAND | wx.ALL, 5)

        self.SetSizer(bSizer2)
        self.Layout()
        bSizer2.Fit(self)

        self.Centre(wx.BOTH)

        global contact_type
        # Connect Events
        # self.combo_contact_type.Bind(wx.EVT_COMBOBOX, self.returnComboBox, self.combo_contact_type, contact_type)
        # self.combo_contact_dir.Bind(wx.EVT_CHOICE, self.returnContactDir)
        # self.combo_contact_person.Bind(wx.EVT_COMBOBOX, self.returnContactPerson)
        # self.editbox_regarding.Bind(wx.EVT_TEXT, self.returnRegarding)
        self.m_sdbSizer1Cancel.Bind(wx.EVT_BUTTON, self.cancel_confirmation)
        self.m_sdbSizer1OK.Bind(wx.EVT_BUTTON, self.click_OK)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def cancel_confirmation(self, event):
        # event.Skip()
        print("Cancel")
        # self.Close()

        dial = wx.MessageDialog(None, 'Are you sure to quit?', 'Question', wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)

        ret = dial.ShowModal()

        if ret == wx.ID_YES:
            self.Destroy()
            quit()
        # else:
            # self.Veto()

    def click_OK(self, event):
        # event.Skip()
        info_complete = True
        err_msg = "Please resolve the following: \n \n"

        global contact_type
        self.phaseSelection = self.combo_contact_type.GetValue()
        contact_type = self.phaseSelection
        if contact_type is wx.EmptyString:
            info_complete = False
            err_msg = err_msg + "* Indicate the type of contact. \n"
            self.combo_contact_type.SetBackgroundColour(wx.Colour(255, 255, 128))
        else:
            self.combo_contact_type.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        global contact_dir
        n = self.choice_contact_dir.GetCurrentSelection()
        contact_dir = self.choice_contact_dir.GetString(n)

        global contact_person
        self.phaseSelection = self.combo_contact_person.GetValue()
        contact_person = self.phaseSelection
        if contact_person is wx.EmptyString:
            info_complete = False
            err_msg = err_msg + "* Indicate who was contacted. \n"
            self.combo_contact_person.SetBackgroundColour(wx.Colour(255, 255, 128))
        else:
            self.combo_contact_person.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        global contact_re
        self.phaseSelection = self.editbox_regarding.GetValue()
        contact_re = self.phaseSelection

        global contact_time
        contact_time = self.editbox_date_time.GetValue()
        if contact_time is wx.EmptyString:
            info_complete = False
            err_msg = err_msg + "* Date/time contact was made. \n"
            self.editbox_date_time.SetBackgroundColour(wx.Colour(255, 255, 128))
        else:
            self.editbox_date_time.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        global MAXIS_case_number
        MAXIS_case_number = self.editbox_MAXIS_case_number.GetValue()
        try:
            len(MAXIS_case_number) < 9
            MAXIS_case_number = int(MAXIS_case_number)
        except:
            info_complete = False
            err_msg = err_msg + "* Enter a valid MAXIS case number. \n"
            self.editbox_MAXIS_case_number.SetBackgroundColour(wx.Colour(255, 255, 128))
        else:
            self.editbox_MAXIS_case_number.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        global interpreter_checkbox
        interpreter_checkbox = self.checkbox_used_interpreter.GetValue()

        global phone_number
        phone_number = self.combo_phone_number.GetValue()

        global mets_ic_number
        mets_ic_number = self.editbox_mets_ic_number.GetValue()


        global contact_reason
        contact_reason = self.editbox_contact_reason.GetValue()
        if contact_reason is wx.EmptyString:
            info_complete = False
            err_msg = err_msg + "* What is the reason for the contact. \n"
            self.editbox_contact_reason.SetBackgroundColour(wx.Colour(255, 255, 128))
        else:
            self.editbox_contact_reason.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        global actions_taken
        actions_taken = self.editbox_action_taken.GetValue()

        global verifs_needed
        verifs_needed = self.editbox_verifs_needed.GetValue()

        global client_instructions
        client_instructions = self.editbox_instructions.GetValue()

        global case_status
        case_status = self.editbox_case_status.GetValue()

        global caf_1_checkbox
        caf_1_checkbox = self.checkbox_CAF1_reminder.GetValue()

        global sent_arep_checkbox
        sent_arep_checkbox = self.checkbox_forms_to_AREP.GetValue()

        global call_center_answer_checkbox
        call_center_answer_checkbox = self.checkbox_callctr_answered.GetValue()

        global call_center_transfer_checkbox
        call_center_transfer_checkbox = self.checkbox_callctr_transfer.GetValue()

        global follow_up_checkbox
        follow_up_checkbox = self.checkbox_follow_up.GetValue()

        global worker_singature
        worker_singature = self.editbox_worker_signature.GetValue()
        if worker_singature is wx.EmptyString:
            info_complete = False
            err_msg = err_msg + "* Enter your signature. \n"
            self.editbox_worker_signature.SetBackgroundColour(wx.Colour(255, 255, 128))
        else:
            self.editbox_worker_signature.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        print("OK")
        if info_complete:
            self.Close()
        else:
            #self.Veto()
            print("Nope")
            print(err_msg)
###########################################################################
## Class PRISMClientContact
###########################################################################

class PRISMClientContact (wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__ (self, parent, id = wx.ID_ANY, title = u"Client Contact", pos = wx.DefaultPosition, size = wx.Size(-1,-1), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL)

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer3 = wx.BoxSizer(wx.VERTICAL)

        self.m_panel3 = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        gbSizer2 = wx.GridBagSizer(0, 0)
        gbSizer2.SetFlexibleDirection(wx.BOTH)
        gbSizer2.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        sbSizer3 = wx.StaticBoxSizer(wx.StaticBox(self.m_panel3, wx.ID_ANY, u"Select on contact type from this group, based on CAAD note requirement"), wx.VERTICAL)

        fgSizer2 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer2.AddGrowableCol(1)
        fgSizer2.SetFlexibleDirection(wx.BOTH)
        fgSizer2.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.text_CPContactType = wx.StaticText(sbSizer3.GetStaticBox(), wx.ID_ANY, u"CP contact type:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_CPContactType.Wrap(-1)
        fgSizer2.Add(self.text_CPContactType, 0, wx.ALL|wx.ALIGN_RIGHT, 5)

        choice_cp_contactChoices = [u"T0050 PHONE CALL TO CP", u"T0051 PHONE CALL FR CP", u"T0052 PHONE CALL RET TO CP", u"T0053 PHONE CALL RET FR CP", u"T0054 PHONE CALL ATMPT TO RET TO CP", u"T0093 CONTACT WITH CP SPOUSE", u"T0101 PHONE CONTACT CP'S ATTORNEY", u"T0201 CONTACT WITH CP EMPLOYER", u"M3910 INTERVIEW WITH CP", u"M2121 LETTER RECD FROM CP"]
        self.choice_cp_contact = wx.Choice(sbSizer3.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choice_cp_contactChoices, 0)
        self.choice_cp_contact.SetSelection(0)
        fgSizer2.Add(self.choice_cp_contact, 0, wx.ALL|wx.EXPAND, 5)

        self.text_NCPContactType = wx.StaticText(sbSizer3.GetStaticBox(), wx.ID_ANY, u"NCP contact type:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_NCPContactType.Wrap(-1)
        fgSizer2.Add(self.text_NCPContactType, 0, wx.ALL|wx.ALIGN_RIGHT, 5)

        choice_ncp_contactChoices = [u"T0058 PHONE CALL RET FR NCP", u"M2122 LETTER RECD FROM NCP", u"M3911 INTERVIEW WITH NCP", u"T0092 CONTACT WITH NCP SPOUSE", u"T0069 PHONE CALL ATMPT RET TO NCP AY", u"T0068 PHONE CALL RET FR NCP AY", u"T0067 PHONE CALL RET TO NCP AY", u"T0066 PHONE CALL FR NCP AY", u"T0065 PHONE CALL TO NCP AY", u"T0064 PHONE CALL ATMPT RET TO NCP EMP", u"T0063 PHONE CALL RET FR NCP EMP", u"T0062 PHONE CALL RET TO NCP EMP", u"T0061 PHONE CALL FROM NCP EMP", u"T0060 PHONE CALL TO NCP EMP", u"T0059 PHONE CALL ATMT TO RET TO NCP", u"T0058 PHONE CALL STMT TO RET TO NCP", u"T0057 PHONE CALL RET TO NCP", u"T0056 PHONE CALL FR NCP", u"T0055 PHONE CALL TO NCP"]
        self.choice_ncp_contact = wx.Choice(sbSizer3.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choice_ncp_contactChoices, 0)
        self.choice_ncp_contact.SetSelection(0)
        fgSizer2.Add(self.choice_ncp_contact, 0, wx.ALL|wx.EXPAND, 5)

        self.text_OtherContact = wx.StaticText(sbSizer3.GetStaticBox(), wx.ID_ANY, u"Other contact type:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_OtherContact.Wrap(-1)
        fgSizer2.Add(self.text_OtherContact, 0, wx.ALL|wx.ALIGN_RIGHT, 5)

        choice_other_contactChoices = [u"T0111 CONTACT WITH OTHER STATE AGENCY", u"T0105 PHONE CONTACT WITH CSPC", u"T1107 CONTACT WITH VITAL RECORDS", wx.EmptyString, u"T0104 PHONE CONTACT WITH FINANCIAL WORKER", u"T0103 PHONE CONTACT WITH OTHER STATE WORKER", u"T0102 PHONE CONTACT WITH COUNTY ATTORNEY", u"T0100 PHONE CONTACT WITH OTHER STATE'S CENTRAL REGISTRY", u"T0098 CONTACT WITH WORKER FROM ANOTHER MN COUNTY", u"T0095 CONTACT WITH SOCIAL WORKER", u"T0090 CONTACT WITH NCP/CP UNION", u"T0087 CONTACT WITH PROBATION OFFICER", u"T0085 CONTACT WITH LAW ENFORCEMENT", u"T0080 CONTACT WITH COURT ADMINISTRATOR", u"T0075 CONTACT WITH HEALTH CARRIER", u"T0074 CONTACT WITH STATE HELP DESK", u"T0070 PHONE CALL/OTHER", u"M0410 CONTACT WITH CCC WORKER"]
        self.choice_other_contact = wx.Choice(sbSizer3.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choice_other_contactChoices, 0)
        self.choice_other_contact.SetSelection(0)
        fgSizer2.Add(self.choice_other_contact, 0, wx.ALL|wx.EXPAND, 5)


        sbSizer3.Add(fgSizer2, 1, wx.EXPAND, 5)


        gbSizer2.Add(sbSizer3, wx.GBPosition(0, 0), wx.GBSpan(3, 5), wx.EXPAND, 5)

        self.text_PRISMCaseNumber = wx.StaticText(self.m_panel3, wx.ID_ANY, u"PRISM case number (XXXXXXXXXX-XX format):", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_PRISMCaseNumber.Wrap(-1)
        gbSizer2.Add(self.text_PRISMCaseNumber, wx.GBPosition(4, 0), wx.GBSpan(2, 2), wx.ALL, 5)

        self.editbox_PRISM_case_number = wx.TextCtrl(self.m_panel3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer2.Add(self.editbox_PRISM_case_number, wx.GBPosition(4, 2), wx.GBSpan(1, 1), wx.ALL, 5)

        self.text_ContactDate = wx.StaticText(self.m_panel3, wx.ID_ANY, u"Date of contact:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_ContactDate.Wrap(-1)
        gbSizer2.Add(self.text_ContactDate, wx.GBPosition(4, 3), wx.GBSpan(1, 1), wx.ALL, 5)

        self.editbox_date_of_contact = wx.TextCtrl(self.m_panel3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer2.Add(self.editbox_date_of_contact, wx.GBPosition(4, 4), wx.GBSpan(1, 1), wx.ALL, 5)

        sbSizer4 = wx.StaticBoxSizer(wx.StaticBox(self.m_panel3, wx.ID_ANY, u"Optional contact info:"), wx.VERTICAL)

        fgSizer3 = wx.FlexGridSizer(0, 4, 0, 0)
        fgSizer3.AddGrowableCol(0)
        fgSizer3.AddGrowableCol(1)
        fgSizer3.AddGrowableCol(2)
        fgSizer3.AddGrowableCol(3)
        fgSizer3.SetFlexibleDirection(wx.BOTH)
        fgSizer3.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.text_PhoneNumber = wx.StaticText(sbSizer4.GetStaticBox(), wx.ID_ANY, u"Phone number:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_PhoneNumber.Wrap(-1)
        fgSizer3.Add(self.text_PhoneNumber, 0, wx.ALL|wx.ALIGN_RIGHT, 5)

        self.editbox_phone_number = wx.TextCtrl(sbSizer4.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer3.Add(self.editbox_phone_number, 0, wx.ALL|wx.EXPAND, 5)

        self.text_ContactTime = wx.StaticText(sbSizer4.GetStaticBox(), wx.ID_ANY, u"Time contact was made:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_ContactTime.Wrap(-1)
        fgSizer3.Add(self.text_ContactTime, 0, wx.ALL|wx.ALIGN_RIGHT, 5)

        self.editbox_contact_time = wx.TextCtrl(sbSizer4.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer3.Add(self.editbox_contact_time, 0, wx.ALL|wx.EXPAND, 5)


        sbSizer4.Add(fgSizer3, 1, wx.EXPAND, 5)


        gbSizer2.Add(sbSizer4, wx.GBPosition(6, 0), wx.GBSpan(1, 5), wx.EXPAND, 5)

        self.text_IssueSubject = wx.StaticText(self.m_panel3, wx.ID_ANY, u"Issue/subject:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_IssueSubject.Wrap(-1)
        gbSizer2.Add(self.text_IssueSubject, wx.GBPosition(7, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        self.editbox_subject = wx.TextCtrl(self.m_panel3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer2.Add(self.editbox_subject, wx.GBPosition(7, 1), wx.GBSpan(1, 4), wx.ALL|wx.EXPAND, 5)

        self.text_ActionTaken = wx.StaticText(self.m_panel3, wx.ID_ANY, u"Action Taken:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_ActionTaken.Wrap(-1)
        gbSizer2.Add(self.text_ActionTaken, wx.GBPosition(8, 0), wx.GBSpan(1, 1), wx.ALL, 5)

        self.editbox_action_taken = wx.TextCtrl(self.m_panel3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer2.Add(self.editbox_action_taken, wx.GBPosition(8, 1), wx.GBSpan(1, 4), wx.ALL|wx.EXPAND, 5)

        sbSizer5 = wx.StaticBoxSizer(wx.StaticBox(self.m_panel3, wx.ID_ANY, u"Helpful optional case info"), wx.VERTICAL)

        fgSizer4 = wx.FlexGridSizer(0, 2, 0, 0)
        fgSizer4.AddGrowableCol(1)
        fgSizer4.SetFlexibleDirection(wx.BOTH)
        fgSizer4.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_SPECIFIED)

        self.text_VerifsNeeded = wx.StaticText(sbSizer5.GetStaticBox(), wx.ID_ANY, u"Verifs needed:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_VerifsNeeded.Wrap(-1)
        fgSizer4.Add(self.text_VerifsNeeded, 0, wx.ALL|wx.ALIGN_RIGHT, 5)

        self.m_textCtrl20 = wx.TextCtrl(sbSizer5.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer4.Add(self.m_textCtrl20, 0, wx.ALL|wx.EXPAND, 5)

        self.text_SpecialInstructions = wx.StaticText(sbSizer5.GetStaticBox(), wx.ID_ANY, u"Special instructions for client:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_SpecialInstructions.Wrap(-1)
        fgSizer4.Add(self.text_SpecialInstructions, 0, wx.ALL, 5)

        self.editbox_special_instructions = wx.TextCtrl(sbSizer5.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        fgSizer4.Add(self.editbox_special_instructions, 0, wx.ALL|wx.EXPAND, 5)


        sbSizer5.Add(fgSizer4, 1, wx.EXPAND, 5)


        gbSizer2.Add(sbSizer5, wx.GBPosition(9, 0), wx.GBSpan(2, 5), wx.EXPAND, 5)

        self.checkbox_verif_id = wx.CheckBox(self.m_panel3, wx.ID_ANY, u"Check here if your verified ID. ", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer2.Add(self.checkbox_verif_id, wx.GBPosition(12, 0), wx.GBSpan(1, 2), wx.ALL, 5)

        self.checkbox_msg_callback = wx.CheckBox(self.m_panel3, wx.ID_ANY, u"Check here if if you left a generic message requesting they return call.", wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer2.Add(self.checkbox_msg_callback, wx.GBPosition(13, 0), wx.GBSpan(1, 4), wx.ALL, 5)

        self.text_SignNote = wx.StaticText(self.m_panel3, wx.ID_ANY, u"Sign your case note:", wx.DefaultPosition, wx.DefaultSize, 0)
        self.text_SignNote.Wrap(-1)
        gbSizer2.Add(self.text_SignNote, wx.GBPosition(14, 0), wx.GBSpan(1, 2), wx.ALL|wx.ALIGN_RIGHT, 5)

        self.editbox_worker_signature = wx.TextCtrl(self.m_panel3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        gbSizer2.Add(self.editbox_worker_signature, wx.GBPosition(14, 2), wx.GBSpan(1, 3), wx.ALL|wx.ALIGN_BOTTOM|wx.EXPAND, 5)

        m_sdbSizer2 = wx.StdDialogButtonSizer()
        self.m_sdbSizer2OK = wx.Button(self.m_panel3, wx.ID_OK)
        m_sdbSizer2.AddButton(self.m_sdbSizer2OK)
        self.m_sdbSizer2Cancel = wx.Button(self.m_panel3, wx.ID_CANCEL)
        m_sdbSizer2.AddButton(self.m_sdbSizer2Cancel)
        m_sdbSizer2.Realize();

        gbSizer2.Add(m_sdbSizer2, wx.GBPosition(15, 3), wx.GBSpan(1, 2), wx.EXPAND, 5)


        self.m_panel3.SetSizer(gbSizer2)
        self.m_panel3.Layout()
        gbSizer2.Fit(self.m_panel3)
        bSizer3.Add(self.m_panel3, 1, wx.EXPAND |wx.ALL, 5)


        self.SetSizer(bSizer3)
        self.Layout()
        bSizer3.Fit(self)

        self.Centre(wx.BOTH)

    def __del__(self):
        pass

def text_needed_validate(self, win):
    textCtrl = self.GetWindow()
    text = textCtrl.GetValue()

    if len(text) == 0:
        err_msg = err_msg + "\n FIELD is required."
        textCtrl.SetBackgroundColor("yellow")
        textCtrl.SetFocus()
        textCtrl.Refresh()
        return False
    else:
        textCtrl.SetBackgroundColor(wx.SystemSettings_GetColor(wx.SYS_COLOR_WINDOW))
        textCtrl.Refresh()
        return True

def cancel_confirmation():
    pass

# Find Determine if worker is PRISM or MAXIS
# Create a FuncLic function to do this - that would allow workers to select one IF a worker is defined as 'BOTH'
worker_type = "MAXIS"
# Find Case number

def write_bullet_and_variable(bullet, option):
    if len(option) > 0:
        print("* %s: %s" % (bullet, option))

now = datetime.datetime.now()

now_time = now.strftime("%m-%d-%Y %H:%M")

MAXIS_case_number = str(123423)

app = wx.App()

if worker_type == "MAXIS":
    frame = MAXISClientContact(None)
if worker_type == "PRISM":
    frame = PRISMClientContact(None)
frame.Show()
app.MainLoop()

# print("Contact Direction is %s" % (contact_dir))

if worker_type is "MAXIS":
    print("Client contact was run for a %s worker." % (worker_type))
    print("Case number: %s" % (MAXIS_case_number))
    print(" ")
    if contact_re is wx.EmptyString:
        print("%s %s %s" % (contact_type, contact_dir, contact_person))
    else:
        print("%s %s %s Re: %s" % (contact_type, contact_dir, contact_person, contact_re))
    if interpreter_checkbox:
        print("* Contact was made: %s w/ interperter" % (contact_time))
    else:
        print("* Contact was made: %s" % (contact_time))

    write_bullet_and_variable("Phone Number", phone_number)
    write_bullet_and_variable("MNSURE/IC number", mets_ic_number)
    write_bullet_and_variable("Reason for contact", contact_reason)
    write_bullet_and_variable("Actions taken", actions_taken)
    write_bullet_and_variable("Verifs needed", verifs_needed)
    write_bullet_and_variable("Instructions/Message for client", client_instructions)
    write_bullet_and_variable("Case status", case_status)

    if caf_1_checkbox:
        print("* Reminded client about the importance of submitting the CAF 1.")
    if sent_arep_checkbox:
        print("*Sent forms(s) to AREP.")
    if call_center_answer_checkbox:
        print("* Call center answered caller's question.")
    if call_center_transfer_checkbox:
        print("* Call center transferred call to a worker.")
    if follow_up_checkbox:
        print("* Follow-up is needed.")

    print("---")
    print(worker_singature)

if worker_type is "PRISM":
    print("PRISM")
