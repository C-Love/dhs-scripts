import bzio
import FuncLib

"""Classes of MAXIS Panels"""
"""This script defines classes for all of the panels in MAXIS
Each of the panels will have a gather_data method used to get all of the information listed on the panel.
Calling class_name.gather_data() will create class properties for each of the data elements.
Many of the STAT panels will also have a create_new method to create a new panel."""


class STAT_ABPS_panel:
    """class references STAT/ABPS
    Methods: gather_data -- get all information from existing panel"""

    def __init__(self, case_number, footer_month, footer_year, instance):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year
        self.instance = instance

    # Dictionaries set up with details explaining codes on panels
    # PF1 has this information stored - adding it here for reference within the class
    # it is more helpful to have the explanations of the codes than just the bare codes
    global good_cause_reasons
    good_cause_reasons = {"1": "Potential Phys Harm/Child",
                          "2": "Potential Emotional Harm/Child",
                          "3": "Potential Physical Harm/Caregiver",
                          "4": "Potential Emotional Harm/Caregiver",
                          "5": "Conception Incest/Forced Rape",
                          "6": "Legal Adoption Before Court",
                          "7": "Parent Gets Preadoption Services"}

    global parental_status
    parental_status = {"1": "Absent Parent Known/Alleged",
                       "2": "Absent Parent Unknown",
                       "3": "Absent Parent Deceased",
                       "4": "Parental Rights Severed",
                       "5": "N/A, Minor is Non-Unit Mbr",
                       "6": "Minor Caregiver No Order Support",
                       "7": "Appl/HC Child No Order Support"}

    global custody
    custody = {"1": "Majority Time w/ Caregiver",
               "2": "Majority Time w/ Absent Parent",
               "3": "No Evidence of Seperate Homes",
               "4": "Equal Time w/ Both Parents",
               "5": "N/A, Minor is Non-Unit Mbr",
               "6": "N/A, Minor Caregiver",
               "7": "N/A, HC Child Applicant"}

    def gather_data(self):
        """Will gather all data from STAT/ABPS
        Properties created:
        self.instance -- the panel instance (in command ABPS __ 01 - the '01') - always a 2 digit string
        self.caregiver -- reference number of caregiver of referenced child(ren) - 2 digit string
        self.coop -- support coop from panel (Y or N string)
        self.good_cause -- status of good cause (string of N, P, G, or D)
        self.gc_clm_date -- date of good cause claim from panel
        self.gc_reason_code -- the code from good cause reason for the claim (string of 1, 2, 3, 4, 5, 6, 7, "_")
        self.gc_reason -- details of good cause reason (not just the code number) (full string)
        self.next_gc_review -- date of next good cause review
        self.sup_evidence -- support evidence (Y or N string)
        self.investigation -- investigation (Y or N string)
        self.med_sup -- medical support services only (Y or N string)
        self.last_name -- absent parent last name (string)
        self.first_name -- absent parent first name (string)
        self. middle -- absent parent middle initial (single character string)
        self.full_name -- absent parent first and last name (with middle initial if it exists) (string)
        self.ssn -- absent parent social security number (string in xxx-xx-xxxx format)
        self.dob -- absent parent date of birth (string in xx/xx/xxxx format)
        self.gender -- absent parent gender (string of single character)
        self.hc_ins_order -- Health Care Insurance order (Y or N string)
        self.hc_ins_compliance -- compliance with health care (Y or N string)
        self.children -- dictionary of all children of this absent parent (child ref is the key,
                         value is list of detail of parental status and detail of custody)"""

        # Navigate to the correct panel to gather information from
        FuncLib.navigate_to_MAXIS_screen(self.case, self.month, self.year, "STAT", "ABPS")
        bzio.WriteScreen(self.instance, 20, 79)
        FuncLib.transmit()

        self.caregiver = bzio.ReadScreen(2, 4, 47)      # reading caregiver reference number and additing it to the class property
        self.coop = bzio.ReadScreen(1, 4, 73)           # reading support coop from the panel and adding it to class property
        self.good_cause = bzio.ReadScreen(1, 5, 47)     # Reading good cause from panel and adding it to the class property
        if self.good_cause != "N":                      # if there is good cause indicated additional information willbe gathered
            # reading and formating date of good cause claim
            self.gc_clm_date = "%s/%s/%s" % (bzio.ReadScreen(2, 5, 73), bzio.ReadScreen(2, 5, 76), bzio.ReadScreen(2, 5, 79))
            self.gc_reason_code = bzio.ReadScreen(1, 6, 47)             # reading good cause reason code
            self.gc_reason = good_cause_reasons[self.gc_reason_code]    # assigning the actual code description using dictionary

            # reading and formatting the date of the net good cause review
            self.next_gc_review = "%s/%s/%s" % (bzio.ReadScreen(2, 6, 73), bzio.ReadScreen(2, 6, 76), bzio.ReadScreen(2, 6, 79))
            self.sup_evidence = bzio.ReadScreen(1, 7, 47)       # reading if ther is supporting evidence and/or an investigation
            self.investigation = bzio.ReadScreen(1, 7, 73)

        self.med_sup = bzio.ReadScreen(1, 8, 48)                        # reading if there is medical support only
        self.last_name = bzio.ReadScreen(24, 10, 30).replace("_", "")   # reading last name of the absent parent
        self.first_name = bzio.ReadScreen(12, 10, 63).replace("_", "")  # reading first name of the absent parent
        self.middle = bzio.ReadScreen(1, 10, 80).replace("_", "")       # reading for middle initial
        # combining all name elements for form full name
        if self.middle == "":
            self.full_name = "%s %s" % (self.first_name, self.last_name)
        else:
            self.full_name = "%s %s. %s" % (self.first_name, self.middle, self.last_name)

        # reading and formatting social security number and date of birth of absent parent
        self.ssn = "%s-%s-%s" % (bzio.ReadScreen(3, 11, 30), bzio.ReadScreen(3, 11, 34), bzio.ReadScreen(4, 11, 37))
        self.dob = "%s/%s/%s" % (bzio.ReadScreen(2, 11, 60), bzio.ReadScreen(2, 11, 63), bzio.ReadScreen(4, 11, 66))
        self.gender = bzio.ReadScreen(1, 11, 80).replace("_", "")               # reading absent parent gender
        self.hc_ins_order = bzio.ReadScreen(1, 12, 44).replace("_", "")         # reading hc insurance order and compliance
        self.hc_ins_compliance = bzio.ReadScreen(1, 12, 80).replace("_", "")

        # setting up a dictionary to store all children infroamtion
        self.children = {}
        child_ref = bzio.ReadScreen(2, 15, 35)      # reading the first child reference number
        row = 15                                    # setting the row - this will need to increment
        while child_ref != "__":
            child_ref = bzio.ReadScreen(2, row, 35)                 # reading the reference number to add to dictionary
            parental_status_code = bzio.ReadScreen(1, row, 53)      # reading code for parental status
            custody_code = bzio.ReadScreen(1, row, 67)              # reading code for custody

            # adding this child to the dictionary with details of parental status and custody using dictionaries
            self.children[child_ref] = [parental_status[parental_status_code], custody[custody_code]]

            # code to incrementing to the next row (or next page of the list of children)
            row += 1
            if row == 18:
                FuncLib.ShiftPF8()
                end_check = bzio.ReadScreen(9, 24, 14)
                if end_check == "LAST PAGE":
                    break
                else:
                    row = 15

            child_ref = bzio.ReadScreen(2, row, 35)

    # TODO Create method in STAT_ABPS_panel to add new ADDR panel (this wil only be used in PND1)
    # TODO create method to update good cause for STAT_ABPS_panel
    # TODO create method to add a child to STAT_ABPS_panel
    # TODO create method to update parental status and custody for STAT_ABPS_panel
    # TODO create method to update the absent parent demographical information in STAT_ABPS_panel


class STAT_ACCI_panel:
    """class references STAT/ACCI
    Methods: gather_data -- get all information from existing panel
             create_new -- create a new panel - only fills the top half of the panel
             add_others_involved -- add a person to ACCI panel in the 'Others Involved' area - bottom half of panel"""

    def __init__(self, case_number, footer_month, footer_year, member, instance):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year
        self.member = member
        self.instance = instance

    # Dictionaries set up with details explaining codes on panels
    # PF1 has this information stored - adding it here for reference within the class
    # it is more helpful to have the explanations of the codes than just the bare codes
    global types_of_accidents
    types_of_accidents = {"01": "Auto",
                          "02": "Worker's Comp",
                          "03": "Homeowners",
                          "04": "No-Fault",
                          "05": "Other Tort",
                          "06": "Product Liab",
                          "07": "Medical Malpractice",
                          "08": "Legal Malpractice",
                          "09": "Diving Tort",
                          "10": "Motorcycle",
                          "11": "MTC or Other Bus Tort",
                          "12": "Pedestrian",
                          "13": "Other",
                          "__": "None"}

    global all_resolutions
    all_resolutions = {"1": "Financial Settlement Only",
                       "2": "Financial and Insurance Settlement",
                       "3": "Insurance Settlement Only",
                       "4": "Tort Liability",
                       "5": "Fraud Referral",
                       "6": "Overpayment",
                       "7": "No Recovery",
                       "_": "Blank"}

    global all_others_involved
    all_others_involved = {"1": "Attorney",
                           "2": "Insurance Company",
                           "3": "Liable Party",
                           "6": "Other"}

    def gather_data(self):
        """Will collect all of the information from defined panel. Class Property outputs are:
        self.type -- Accident Type(string)`
        self.injury_date -- Injury Date (string)
        self.med_coop -- Med Cooperation (Y/N) (String - Y/N)
        self.good_cause -- Good Cause (String = Y/N)
        self.claim_date -- Claim Date (String - xx/xx/xx)
        self.evidence -- Evidence (Y/N) (String - Y/N)
        self.pend_lit -- Pend Litigation (Y/N) (String - Y/N)
        self.resolution -- Resolution (String - details from PF1 menu)
        self.HH_MEMB_involved -- Ref Nbr HH Members Involved (List of reference numbers)
        self.others_involved -- ***** Others Involved ******(Dictionary - Key: Name, Value: List with Indicator detail, address, phone number)"""

        # navigating to STAT/ACCI for the member and instance indicated
        FuncLib.navigate_to_MAXIS_screen(self.case, self.month, self.year, "STAT", "ACCI")
        bzio.WriteScreen(self.member, 20, 76)
        bzio.WriteScreen(self.instance, 20, 79)
        FuncLib.transmit()

        # reading all of the panel and assigning each to an above named property
        type_code = bzio.ReadScreen(2, 6, 47)       # reading type of accident code
        self.type = types_of_accidents[type_code]   # assigning detail based on the code found above using dictionary
        self.injury_date = "%s/%s/%s" % (bzio.ReadScreen(2, 6, 73), bzio.ReadScreen(2, 6, 76), bzio.ReadScreen(2, 6, 79))   # formatting as date
        self.med_coop = bzio.ReadScreen(1, 7, 47)
        self.good_cause = bzio.ReadScreen(1, 7, 73)
        self.claim_date = "%s/%s/%s" % (bzio.ReadScreen(2, 8, 47), bzio.ReadScreen(2, 8, 50), bzio.ReadScreen(2, 8, 53))    # formatting as date
        self.evidence = bzio.ReadScreen(1, 8, 73)
        self.pend_lit = bzio.ReadScreen(1, 9, 47)
        resolution_code = bzio.ReadScreen(1, 9, 73)
        self.resolution = all_resolutions[resolution_code]  # assigning detail of resolution based on code - using dictionary

        # Reading any/all of the other HH members listed (will ignore any '__')
        col = 53    # this will increment as the list goes horizontal
        self.HH_MEMB_involved = []                      # defining this property as a list
        memb_invlvd = bzio.ReadScreen(2, 10, col)       # reading the member involved (this may start with __)
        while memb_invlvd != "__":
            self.HH_MEMB_involved.append(memb_invlvd)   # adding to the list
            col += 3                                    # incrementing to the next in the list
            memb_invlvd = bzio.ReadScreen(2, 10, col)   # reading the next HH member - will end loop if this is __

        # setting this property as a dictionary - any others involved will be stored in a dictionary
        self.others_involved = {}
        other_name = bzio.ReadScreen(38, 13, 63).replace("_", "")   # reading the name
        while other_name != "":
            indicator = bzio.ReadScreen(1, 12, 36)
            # dictionary structure:
            # key is the name
            # values are a list of : inidicator detail (from above dictionary), address (in format line1 line2 city, state zip), phone (in format xxx-xxx-xxxx)
            self.others_involved[other_name] = [all_others_involved[indicator], "%s %s %s, %s %s" %
                                                (bzio.ReadScreen(22, 14, 36).replace("_", ""), bzio.ReadScreen(22, 15, 36).replace("_", ""),
                                                 bzio.ReadScreen(15, 16, 36).replace("_", ""), bzio.ReadScreen(2, 16, 59), bzio.ReadScreen(5, 16, 69)),
                                                "%s-%s-%s" % (bzio.ReadScreen(3, 17, 38), bzio.ReadScreen(3, 17, 44), bzio.ReadScreen(4, 17, 48))]
            # checking to see if panel indicates another person is involved
            another_person = bzio.ReadScreen(7, 18, 66)
            if another_person == "More: +":
                FuncLib.ShiftPF8()      # going to the next page
                other_name = bzio.ReadScreen(38, 13, 63).replace("_", "")   # reading the next name
            else:
                other_name = ""          # blanking out the variable to end the loop if there is no indication of another person

    def create_new(self, acci_type, date_of_injury, coop, litigation, date_of_claim=None,
                   good_cause=None, gc_evidence=None, gc_resolution=None, mbrs_invlvd=[]):
        """Function to create a new ACCI panel. This function ONLY fills the top half of the panel.
        Use add_others_involved function to add other parties involved with the accident.
        Argument requirements:
        acci_type -- options are in PF1 menu (01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12, 13) details in dict types_of_accidents
        date_of_injury -- date with month, day, year
        coop -- only options are Y or N
        litigation -- only options are Y or N
        Optionsal Argument Requiremrnts:
        date_of_claim -- date with month, day, year
        good_cause -- only options are N, P, G, D
        gc_evidence -- only options are Y or N
        gc_resolution -- options are in PF1 menu (1, 2, 3, 4, 5, 6, 7) details in all_resolutions dictionary
        mbrs_invlvd -- This is a list with member reference numbers in two digit formats"""

        # Navigating to STAT/ACCI and creating a new panel for the member - leaving it in edit mode
        FuncLib.navigate_to_MAXIS_screen(self.case, self.month, self.year, "STAT", "ACCI")
        bzio.WriteScreen(self.member, 20, 76)
        bzio.WriteScreen("NN", 20, 79)
        FuncLib.transmit()

        instance = bzio.ReadScreen(2, 2, 72).strip()    # assigning the instance to class variable
        if len(instance) == 1:
            instance = "0" + instance
        self.instance = instance

        # TODO Create a function that will check to be sure that a new panel has been created and is in edit mode
        # FIXME Insert safety check method to be sure panel is in edit mode

        bzio.WriteScreen(acci_type, 6, 47)          # Writes the type to the new panel
        self.type = types_of_accidents[acci_type]   # Finds the actual type from the typ code provided and assigns to class variable

        date_split = FuncLib.mainframe_date(date_of_injury, "XX XX XX")  # Creates a list of the mm, dd, yy
        bzio.WriteScreen(date_split[0], 6, 73)                          # Each date itemis written to the new panel.
        bzio.WriteScreen(date_split[1], 6, 76)                          # TODO update mainframe_date function to write the date as well
        bzio.WriteScreen(date_split[2], 6, 79)
        self.injury_date = "%s/%s/%s" % (date_split[0], date_split[1], date_split[2])   # Assigns date to class variable

        bzio.WriteScreen(coop, 7, 47)               # Writes medical coop to new panel and saves to class variable
        self.med_coop = coop

        bzio.WriteScreen(litigation, 9, 47)         # Writes litigation to new panel and saves to class variable
        self.pend_lit = litigation

        if date_of_claim:          # If a claim date is entered the date will be formatted and entered
            date_split = FuncLib.mainframe_date(date_of_claim, "XX XX XX")
            bzio.WriteScreen(date_split[0], 8, 47)
            bzio.WriteScreen(date_split[1], 8, 50)
            bzio.WriteScreen(date_split[2], 8, 53)
            self.claim_date = "%s/%s/%s" % (date_split[0], date_split[1], date_split[2])   # Assigns date to class variable

        if good_cause:
            bzio.WriteScreen(good_cause, 7, 73)
            self.good_cause = good_cause

        if gc_evidence:
            bzio.WriteScreen(gc_evidence, 8, 73)
            self.evidence - gc_evidence

        if gc_resolution:       # if a resolution code was provided, the code will be entered
            bzio.WriteScreen(gc_resolution, 9, 73)
            self.resolution = all_resolutions[gc_resolution]    # Finds the details of the resolution code from all)_resolution dictionary

        if mbrs_invlvd:         # if a list of other hh members involved was provided, they will be entered in turn
            col = 53            # Setting the column as the members are entered on the same row but the column must increment
            for member in mbrs_invlvd:
                bzio.WriteScreen(member, 10, col)       # enters the member reference number
                col += 3                                # column increments by 3 for each new HH Member
            self.HH_MEMB_involved = mbrs_invlvd         # adds list to the class parameter

    def add_others_involved(self, indicator, name, addr_1=None, addr_2=None,
                            city=None, state=None, zip=None, phone=None, ext=None):
        """Function to add one entry to others involved of an already existing ACCI Panel.
        This function needs to be run seperately for every additional person, but it will determine
        if the person is new and will NOT overwrite an existing person involved.
        Arguments:
        indicator -- Options are in PF1 menu - 1, 2, 3, 6 - details in all_others_involved dictionary
        name -- The name of the other person/party involved (string)
        Optional args:
        addr_1 -- line one of an address (string)
        addr_2 -- line 2 of an address (string)
        city -- city of an address (string)
        state -- state abrv code of an address (2 only) (string)
        zip -- 5 digit zip code (string)
        phone -- phone number (string in format xxx-xxx-xxxx)"""

        # Navigating to the correct ACCI panel to add new entry
        FuncLib.navigate_to_MAXIS_screen(self.case, self.month, self.year, "STAT", "ACCI")
        bzio.WriteScreen(self.member, 20, 76)
        bzio.WriteScreen(self.instance, 20, 79)
        FuncLib.transmit()

        # All of the parameters will be written to new panel, if it is NONE then nothing will be entered
        bzio.WriteScreen(indicator, 12, 36)
        bzio.WriteScreen(name, 13, 36)
        bzio.WriteScreen(addr_1, 14, 36)
        bzio.WriteScreen(addr_2, 15, 36)
        bzio.WriteScreen(city, 16, 36)
        bzio.WriteScreen(state, 16, 59)
        bzio.WriteScreen(zip, 16, 69)
        if phone:
            phone_list = phone.split("-")
            bzio.WriteScreen(phone_list[0], 17, 38)
            bzio.WriteScreen(phone_list[1], 17, 44)
            bzio.WriteScreen(phone_list[2], 17, 48)

        # Others involved are saved in a dictionary. This saves all of the arguments to the dictionary
        if self.others_involved is None:    # If there is no dictionary already defined to this parameter - this defines it as a dictionary
            self.others_involved = {}

        # adds a new entry to the dictionary by key (name of other involved)
        self.others_involved[name] = [all_others_involved[indicator], "%s %s %s, %s %s" % (addr_1, addr_2, city, state, zip), phone]


class STAT_ACCT_panel:
    """class references STAT/ACCT
    Methods: gather_data -- get all information from existing panel
             create_new -- creates a new ACCT panel"""
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year
        self.member = member
        self.instance = instance

    # Dictionaries set up with details explaining codes on panels
    # PF1 has this information stored - adding it here for reference within the class
    # it is more helpful to have the explanations of the codes than just the bare codes
    global account_types
    account_types = {"SV": "Savings",
                     "CK": "Checking",
                     "CE": "Certificate of Deposit",
                     "MM": "Money Market",
                     "DC": "Debit Card",
                     "KO": "Keogh Account",
                     "FT": "Federal Thrift Savings Plan",
                     "SL": "State & Local GovernmentRetirement and Certain Tax-Exempt Entities",
                     "RA": "Employee Retirement Annuities",
                     "NP": "Non-Profit Employer Retirement Plans",
                     "IR": "Individual Retirement Account",
                     "RH": "Roth IRA",
                     "FR": "Retirement Plans for Certain Government & Non-Government",
                     "CT": "Corp Retirment Trust Prior to 6/25/1959",
                     "RT": "Other Retirement Fund",
                     "QT": "Qualified Tuition (529)",
                     "CA": "Coverdell SV (530)",
                     "OE": "Other Educational",
                     "OT": "Other Account Type"}

    global acct_verif_codes
    acct_verif_codes = {"1": "Bank Statement",
                        "2": "Agency Verif Form",
                        "3": "Colateral Contact",
                        "5": "Other Document",
                        "6": "Personal Statement",
                        "N": "No Verif Provided",
                        "_": "Blank"}

    def gather_data(self):
        """Method to get all information from ACCT panel indicated.
        Class Properies created:
            self.type -- Type of account (string - detailed from dicationary above)
            self.number -- account number (string - may be empty)
            self.location -- financial institution of account (string - may be empty)
            self.balance -- account balance (string of numbers)
            self.balance_verif -- detailed verification information (string - detail from dicationary)
            self.balance_as_of -- date of balance information (string - in xx/xx/xx format)
            self.withdrawal_penalty -- amount of withdrawal penalty (string of numbers)
            self.withdrawal_yn -- If withdrawal penalty exists (Y or N string)
            self. withdrawal_verif -- verification detail of withdrawal penalty (string - detail from dictionary)
            self.programs_to_count -- LIST of all programs with Count coded as 'Y'
            self.joint_owner -- Joint Owner infromation (string of Y or N)
            self.share_ratio -- IF Y for Joint Owner - the ratio of owned amount (string in x/x format)
            self.next_interest_date -- date of next interest (string of date in MM/YY format) - empty if no date listed on panel"""

        # navigating to the correct ACCT panel - for the right member and instance.
        FuncLib.navigate_to_MAXIS_screen(self.case, self.month, self.year, "STAT", "ACCT")
        bzio.WriteScreen(self.member, 20, 76)
        bzio.WriteScreen(self.instance, 20, 79)
        FuncLib.transmit()

        account_type_code = bzio.ReadScreen(2, 6, 44)   # reading account type code
        self.type = account_types[account_type_code]    # assigning account type detail from dictionary to property

        # reading panel information and assign to class property
        self.number = bzio.ReadScreen(20, 7, 44).replace("_", "")
        self.location = bzio.ReadScreen(20, 8, 44).replace("_", "")

        self.balance = bzio.ReadScreen(8, 10, 46)
        verification = bzio.ReadScreen(1, 10, 64)
        self.balance_verif = acct_verif_codes[verification]     # assigning the verification detail from dictionary
        # formatting date to mm/dd/yy
        self.balance_as_of = "%s/%s/%s" % (bzio.ReadScreen(2, 11, 44), bzio.ReadScreen(2, 11, 47), bzio.ReadScreen(2, 11, 50))
        self.withdrawal_penalty = bzio.ReadScreen(8, 12, 46)
        if self.withdrawal_penalty == "________":               # setting penalty to 0 if blank
            self.withdrawal_penalty = "0"
        self.withdrawal_yn = bzio.ReadScreen(1, 12, 64)
        verification = bzio.ReadScreen(1, 12, 72)
        self.withdrawal_verif = acct_verif_codes[verification]  # assigning the verification detail from dictionary

        self.programs_to_count = []                     # setting this property to a list
        if bzio.ReadScreen(1, 14, 50) == "Y":           # for each program if code is Y it will be added to list
            self.programs_to_count.append("Cash")
        if bzio.ReadScreen(1, 14, 57) == "Y":
            self.programs_to_count.append("SNAP")
        if bzio.ReadScreen(1, 14, 64) == "Y":
            self.programs_to_count.append("HC")
        if bzio.ReadScreen(1, 14, 72) == "Y":
            self.programs_to_count.append("GRH")
        if bzio.ReadScreen(1, 14, 80) == "Y":
            self.programs_to_count.append("IV-E")
        self.joint_owner = bzio.ReadScreen(1, 15, 44)
        if self.joint_owner == "Y":                     # only looks for share ratio if joint owner is indicated
            self.share_ratio = "%s/%s" % (bzio.ReadScreen(1, 15, 76), bzio.ReadScreen(1, 15, 80))
        if bzio.ReadScreen(2, 17, 57) != "__":          # only saves next interest date if not blank
            self.next_interest_date = "%s/%s" % (bzio.ReadScreen(2, 17, 57), bzio.ReadScreen(2, 17, 60))

    def create_new(self, account_type, balance, balance_verif, balance_date, account_number=None, account_location=None,
                   withdrawal_penalty=None, withdrawal_verif=None, programs_counted=[], share_ratio=None, interest_date=None):
        """Function to create a new ACCT panel. Member is defined from the class initialization.
        Argument requirements:
            account_type -- 2 digit string of one of possible account types
            balance -- string or float of numbers
            balance_verif -- verification code - Options: 1, 2, 3, 5, 6, N
            balance_date -- date with month, day, year for balance effective date
        Optional args:
            account_number -- string of numbers or integer for the account number
            account_location -- String of financial institution name
            withdrawal_penalty -- string of numbers or float for the amount of the penalty
                               -- anything other than 'None' entered here will code Withdrawal Penalty as Y
            withdrawal_verif -- verification code for the withdrawal penalty
            programs_counted -- list of programs that this account counts for (Options are Cash, SNAP/FS, HC, GRH, IV-E)
            share_ratio -- format of x/x for percentage of amount owned by indicated member
                        -- if this is 'None' joint owner will be coded as 'N', otherwise it will be coded as 'Y'
            interest_date -- date in format mm/yy"""

        # navigating to ACCT for the correct member and creates a new panel
        FuncLib.navigate_to_MAXIS_screen(self.case, self.month, self.year, "STAT", "ACCT")
        bzio.WriteScreen(self.member, 20, 76)
        bzio.WriteScreen("NN", 20, 79)
        FuncLib.transmit()

        # setting the instance of the created panel to the correct class property
        instance = bzio.ReadScreen(2, 2, 72).strip()
        if len(instance) == 1:
            instance = "0" + instance
        self.instance = instance

        # FIXME add function (that needs to be created) to check and ensure the panel is created and in edit mode

        # writing each parameter to the new pannel and saving each to the class property
        account_type.upper()                    # sometimes MAXIS prefers uppercase
        bzio.WriteScreen(account_type, 6, 44)
        self.type = account_types[account_type]     # setting the property to detailed verifciation information from dictionary
        bzio.WriteScreen(balance, 10, 46)
        self.balance = balance
        bzio.WriteScreen(balance_verif, 10, 64)
        self.balance_verif = acct_verif_codes[balance_verif]    # setting the property to detailed verification info from dictionary

        # FIXME - update this code once the function is updated to write the date as well
        date_split = FuncLib.mainframe_date(balance_date, "XX XX XX")       # seperating the date infromation to a list
        bzio.WriteScreen(date_split[0], 11, 44)                             # writing each date element to MAXIS
        bzio.WriteScreen(date_split[1], 11, 47)
        bzio.WriteScreen(date_split[2], 11, 50)
        self.balance_as_of = "%s/%s/%s" % (date_split[0], date_split[1], date_split[2])  # setting property to mm/dd/yy format

        # for each optional argument - they will only be entered if not None
        self.number = account_number
        bzio.WriteScreen(account_number, 7, 44)

        self.location = account_location
        bzio.WriteScreen(account_location, 8, 44)

        # if these arg is None, an entry should still happen in the class property
        if withdrawal_penalty:
            bzio.WriteScreen(withdrawal_penalty, 12, 46)
            bzio.WriteScreen("Y", 12, 64)
            self.withdrawal_penalty = withdrawal_penalty
            self.withdrawal_yn = "Y"
        else:
            self.withdrawal_penalty = "0"

        if withdrawal_verif:
            bzio.WriteScreen(withdrawal_verif, 12, 72)
            self.withdrawal_verif = acct_verif_codes[withdrawal_verif]
        else:
            self.withdrawal_verif = "Blank"

        self.programs_to_count = []                   # creating a list
        if programs_counted:
            for prog in programs_counted:             # looks at each program listed
                if prog.upper() == "CASH":            # each program has different coordinates to enter 'Y'
                    bzio.WriteScreen("Y", 14, 50)
                    self.programs_to_count.append("Cash")
                elif prog.upper() == "SNAP" or "FS":
                    bzio.WriteScreen("Y", 14, 57)
                    self.programs_to_count.append("SNAP")
                elif prog.upper() == "HC":
                    bzio.WriteScreen("Y", 14, 64)
                    self.programs_to_count.append("HC")
                elif prog.upper() == "GRH":
                    bzio.WriteScreen("Y", 14, 72)
                    self.programs_to_count.append("GRH")
                elif prog.upper() == "IV-E":
                    bzio.WriteScreen("Y", 14, 80)
                    self.programs_to_count.append("IV-E")
        # TODO need to add code to ACCT create_new to code program count as 'N'

        if interest_date:
            date_split = FuncLib.mainframe_date(interest_date, "XX XX")     # creating a list of each date element
            bzio.WriteScreen(date_split[0], 17, 57)                         # FIXME update the code here when mainframe_date is updated
            bzio.WriteScreen(date_split[1], 17, 60)
            self.next_interest_date = "%s/%s" % (date_split[0], date_split[1])  # adding to property in mm/yy format

        # if share ratio is None - seperate code will update joint owner differently
        if share_ratio:
            self.joint_owner = "Y"
            bzio.WriteScreen(share_ratio[0], 15, 76)
            bzio.WriteScreen(share_ratio[-1], 15, 80)
            self.share_ratio = "%s/%s" % (share_ratio[0], share_ratio[-1])
        else:
            self.joint_owner = "N"
            bzio.WriteScreen("N", 15, 44)

        # transmitting here saves the panel
        FuncLib.transmit()
        warning_check = bzio.ReadScreen(7, 24, 2)   # sometimes there is a warning that must be transmitted past
        if warning_check == "WARNING":
            FuncLib.transmit()

    # TODO create update balance method for STAT_ACCT_panel
    # TODO create update verification method for STAT_ACCT_panel


class STAT_ACUT_panel:
    def __init__(self, case_number, footer_month, footer_year):
        pass

    def gather_data(self):
        pass


class STAT_ADDR_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    global all_res_codes
    all_res_codes = {"BD": "Bois Forte - Deer Creek",
                     "BN": "Bois Forte - Nett Lake",
                     "BV": "Bois Forte - Vermillion Lk",
                     "FL": "Fond du Lac",
                     "GP": "Grand Portage",
                     "LL": "Leach Lake",
                     "LS": "Lower Sioux",
                     "ML": "Mille Lacs",
                     "PL": "Prairie Islandd Community",
                     "RL": "Red Lake",
                     "SM": "Shakopee Mdewakanton",
                     "US": "Upper Sioux",
                     "WE": "White Earth",
                     "__": "UNKNOWN"}

    global addr_verif_codes
    addr_verif_codes = {"SF": "Shelter Form",
                        "CO": "Colateral Statement",
                        "LE": "Lease/Renta Document",
                        "MO": "Mortgage Papers",
                        "TX": "Property Tax Statement",
                        "CD": "Contract for Deed",
                        "UT": "Utility Statement",
                        "DL": "Drivers License/State ID",
                        "OT": "Other Document",
                        "NO": "No Verification Provided"}

    def gather_data(self):
        """Method to gather information from ADDR and fill class properties"""

        FuncLib.navigate_to_MAXIS_screen(self.case, self.month, self.year, "STAT", "ADDR")

        eff_month = bzio.ReadScreen(2, 4, 43)
        eff_day = bzio.ReadScreen(2, 4, 46)
        eff_year = bzio.ReadScreen(2, 4, 49)

        self.effective_date = "%s/%s/%s" % (eff_month, eff_day, eff_year)

        self.resi1 = bzio.ReadScreen(22, 6, 43).replace("_", "")
        self.resi2 = bzio.ReadScreen(22, 7, 43).replace("_", "")
        self.resi_city = bzio.ReadScreen(15, 8, 43).replace("_", "")
        self.resi_state = bzio.ReadScreen(2, 8, 66).replace("_", "")
        self.resi_zip = bzio.ReadScreen(5, 9, 43)
        self.resi_cty = bzio.ReadScreen(2, 9, 66)
        verif_code = bzio.ReadScreen(2, 9, 74)
        self.resi_verif = addr_verif_codes[verif_code]
        if bzio.ReadScreen(1, 10, 43).replace("_", "") == "Y":
            self.homeless = True
        else:
            self.homeless = False
        if bzio.ReadScreen(1, 10, 74) == "Y":
            self.reservation = True
            self.reservation_code = bzio.ReadScreen(2, 11, 74)
            self.reservation_name = all_res_codes[self.reservation_code]
        else:
            self.reservation = False

        self.living_situation = bzio.ReadScreen(22, 6, 43).replace("_", "")

        if bzio.ReadScreen(22, 13, 43).replace("_", "") != "":
            self.diff_mail = True
            self.mail1 = bzio.ReadScreen(22, 13, 43).replace("_", "")
            self.mail2 = bzio.ReadScreen(22, 14, 43).replace("_", "")
            self.mail_city = bzio.ReadScreen(15, 15, 43).replace("_", "")
            self.mail_state = bzio.ReadScreen(2, 16, 43).replace("_", "")
            self.mail_zip = bzio.ReadScreen(5, 16, 52).replace("_", "")
        else:
            self.diff_mail = False

        self.phone_one = "%s-%s-%s" % (bzio.ReadScreen(3, 17, 45), bzio.ReadScreen(3, 17, 51), bzio.ReadScreen(4, 17, 55))
        self.phone_two = "%s-%s-%s" % (bzio.ReadScreen(3, 18, 45), bzio.ReadScreen(3, 18, 51), bzio.ReadScreen(4, 18, 55))
        self.phone_three = "%s-%s-%s" % (bzio.ReadScreen(3, 19, 45), bzio.ReadScreen(3, 19, 51), bzio.ReadScreen(4, 19, 55))

        self.phone_list = []
        if self.phone_one != "___-___-____":
            self.phone_list.append(self.phone_one)
        if self.phone_two != "___-___-____":
            self.phone_list.append(self.phone_two)
        if self.phone_three != "___-___-____":
            self.phone_list.append(self.phone_three)

    # TODO make create_new method for STAT_ADDR_panel
    # TODO create method for updating phone numbers in STAT_ADDR_panel
    # TODO create method for updating residence address in STAT_ADDR_panel
    # TODO create method for updating mailing address in STAT_ADDR_panel
    # TODO create method for updating verification on STAT_ADDR_panel


class STAT_ADME_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_ALIA_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_ALTP_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_AREP_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_BILS_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_BUDG_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_BUSI_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_CARS_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_CASH_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_COEX_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_DCEX_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_DFLN_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_DIET_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_DISA_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_DISQ_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_DSTT_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_EATS_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_EMMA_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_EMPS_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_FACI_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_FCFC_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_FCPL_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_FMED_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_HCMI_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_HCRE_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_HEST_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_IMIG_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_INSA_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_JOBS_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_LUMP_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_MEDI_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_MEMB_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_MEMI_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_MISC_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_MMSA_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_MSUR_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_OTHR_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_PACT_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_PARE_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_PBEN_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_PDED_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_PREG_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_PROG_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_RBIC_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_REMO_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_RESI_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_REST_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_REVW_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_SANC_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_SCHL_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_SECU_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_SHEL_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_SIBL_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_SPON_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_STEC_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_STIN_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_STRK_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_STWK_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_SWKR_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_TIME_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_TRAC_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_TRAN_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_TYPE_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_UNEA_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_WKEX_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass


class STAT_WREG_panel:
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        pass

    def gather_data(self):
        pass
