import bzio
import FuncLib

"""Classes of MAXIS Panels"""
"""This script defines classes for all of the panels in MAXIS
Each of the panels will have a gather_data method used to get all of the information listed on the panel.
Calling class_name.gather_data() will create class properties for each of the data elements.
Many of the STAT panels will also have a create_new method to create a new panel."""


class FUNC_COMD_panel:
    """Template of MAXIS Panel classes"""
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        self.case = case_number         
        self.month = footer_month
        self.year = footer_year
        self.member = member
        self.instance = instance

    def gather_data(self):
        """This method never takes arguments and outputs all of the information from the panel."""



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
                FuncLib.PF20()
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
                FuncLib.PF20()      # going to the next page
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
        FuncLib.PF9()           # Put panel in edit mode

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
    """class to reference STAT/ACUT - needs member reference
    Methods: gather_data -- get all infroamtion from existing panel
             create_new -- creates a new ACUT panel for the member specified"""
    def __init__(self, case_number, footer_month, footer_year, member):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year
        self.member = member

    # No dictionaries for this class at this time

    def gather_data(self):
        """Method to get all information from STAT/ACUT for the specified member.
        Class Propertied defined in this method:
            self.shared -- Boolean for if shared or not
            self.retro_heat_verif -- String of Y or N - would be None if left blank on panel
            self.retro_heat_amount -- float of the amount on panel - would be None if left blank on the panel
            self.prosp_heat_verif -- String of Y or N - would be None if left blank on panel
            self.prosp_heat_amount -- float of the amount on panel - would be None if left blank on the panel
            self.retro_air_verif -- String of Y or N - would be None if left blank on panel
            self.retro_air_amount -- float of the amount on panel - would be None if left blank on the panel
            self.prosp_air_verif -- String of Y or N - would be None if left blank on panel
            self.prosp_air_amount -- float of the amount on panel - would be None if left blank on the panel
            self.retro_elect_verif -- String of Y or N - would be None if left blank on panel
            self.retro_elect_amount -- float of the amount on panel - would be None if left blank on the panel
            self.prosp_elect_verif -- String of Y or N - would be None if left blank on panel
            self.prosp_elect_amount -- float of the amount on panel - would be None if left blank on the panel
            self.retro_fuel_verif -- String of Y or N - would be None if left blank on panel
            self.retro_fuel_amount -- float of the amount on panel - would be None if left blank on the panel
            self.prosp_fuel_verif -- String of Y or N - would be None if left blank on panel
            self.prosp_fuel_amount -- float of the amount on panel - would be None if left blank on the panel
            self.retro_garbage_verif -- String of Y or N - would be None if left blank on panel
            self.retro_garbage_amount -- float of the amount on panel - would be None if left blank on the panel
            self.prosp_garbage_verif -- String of Y or N - would be None if left blank on panel
            self.prosp_garbage_amount -- float of the amount on panel - would be None if left blank on the panel
            self.retro_water_verif -- String of Y or N - would be None if left blank on panel
            self.retro_water_amount -- float of the amount on panel - would be None if left blank on the panel
            self.prosp_water_verif -- String of Y or N - would be None if left blank on panel
            self.prosp_water_amount -- float of the amount on panel - would be None if left blank on the panel
            self.retro_sewer_verif -- String of Y or N - would be None if left blank on panel
            self.retro_sewer_amount -- float of the amount on panel - would be None if left blank on the panel
            self.prosp_sewer_verif -- String of Y or N - would be None if left blank on panel
            self.prosp_sewer_amount -- float of the amount on panel - would be None if left blank on the panel
            self.retro_other_verif -- String of Y or N - would be None if left blank on panel
            self.retro_other_amount -- float of the amount on panel - would be None if left blank on the panel
            self.prosp_other_verif -- String of Y or N - would be None if left blank on panel
            self.prosp_other_amount -- float of the amount on panel - would be None if left blank on the panel
            self.dwp_phone -- boolean of if phone is used "_" defaults to False
            self.dwp_amount -- float of the amount on panel - would be blank if no dwp phone"""
        # navigate to STAT/ACUT for member
        FuncLib.navigate_to_MAXIS_screen(self.case, self.month, self.year, "STAT", "ACUT")
        bzio.WriteScreen(self.member, 20, 76)
        FuncLib.transmit()

        if bzio.ReadScreen(1, 6, 42) == "Y":        # reading the Y/N code for cshared and setting proprty as T/F
            self.shared = True
        else:
            self.shared = False

        # each line is read and the retro and prospective verifs and amounts are assigned to a property
        # numbers are converted to floats
        # HEAT
        self.retro_heat_verif = bzio.ReadScreen(1, 10, 35).replace("_", "")
        self.retro_heat_amount = bzio.ReadScreen(8, 10, 41).strip().replace("_", "")
        if self.retro_heat_amount:
            self.retro_heat_amount = float(self.retro_heat_amount)
        self.prosp_heat_verif = bzio.ReadScreen(1, 10, 55).replace("_", "")
        self.prosp_heat_amount = bzio.ReadScreen(8, 10, 61).strip().replace("_", "")
        if self.prosp_heat_amount:
            self.prosp_heat_amount = float(self.prosp_heat_amount)

        # AIR
        self.retro_air_verif = bzio.ReadScreen(1, 11, 35).replace("_", "")
        self.retro_air_amount = bzio.ReadScreen(8, 11, 41).strip().replace("_", "")
        if self.retro_air_amount:
            self.retro_air_amount = float(self.retro_air_amount)
        self.prosp_air_verif = bzio.ReadScreen(1, 11, 55).replace("_", "")
        self.prosp_air_amount = bzio.ReadScreen(8, 11, 61).strip().replace("_", "")
        if self.prosp_air_amount:
            self.prosp_air_amount = float(self.prosp_air_amount)

        # ELECTRIC
        self.retro_elect_verif = bzio.ReadScreen(1, 12, 35).replace("_", "")
        self.retro_elect_amount = bzio.ReadScreen(8, 12, 41).strip().replace("_", "")
        if self.retro_elect_amount:
            self.retro_elect_amount = float(self.retro_elect_amount)
        self.prosp_elect_verif = bzio.ReadScreen(1, 12, 55).replace("_", "")
        self.prosp_elect_amount = bzio.ReadScreen(8, 12, 61).strip().replace("_", "")
        if self.prosp_elect_amount:
            self.prosp_elect_amount = float(self.prosp_elect_amount)

        # FUEL
        self.retro_fuel_verif = bzio.ReadScreen(1, 13, 35).replace("_", "")
        self.retro_fuel_amount = bzio.ReadScreen(8, 13, 41).strip().replace("_", "")
        if self.retro_fuel_amount:
            self.retro_fuel_amount = float(self.retro_fuel_amount)
        self.prosp_fuel_verif = bzio.ReadScreen(1, 13, 55).replace("_", "")
        self.prosp_fuel_amount = bzio.ReadScreen(8, 13, 61).strip().replace("_", "")
        if self.prosp_fuel_amount:
            self.prosp_fuel_amount = float(self.prosp_fuel_amount)

        # GARBAGE
        self.retro_garbage_verif = bzio.ReadScreen(1, 14, 35).replace("_", "")
        self.retro_garbage_amount = bzio.ReadScreen(8, 14, 41).strip().replace("_", "")
        if self.retro_garbage_amount:
            self.retro_garbage_amount = float(self.retro_garbage_amount)
        self.prosp_garbage_verif = bzio.ReadScreen(1, 14, 55).replace("_", "")
        self.prosp_garbage_amount = bzio.ReadScreen(8, 14, 61).strip().replace("_", "")
        if self.prosp_garbage_amount:
            self.prosp_garbage_amount = float(self.prosp_garbage_amount)

        # WATER
        self.retro_water_verif = bzio.ReadScreen(1, 15, 35).replace("_", "")
        self.retro_water_amount = bzio.ReadScreen(8, 15, 41).strip().replace("_", "")
        if self.retro_water_amount:
            self.retro_water_amount = float(self.retro_water_amount)
        self.prosp_water_verif = bzio.ReadScreen(1, 15, 55).replace("_", "")
        self.prosp_water_amount = bzio.ReadScreen(8, 15, 61).strip().replace("_", "")
        if self.prosp_water_amount:
            self.prosp_water_amount = float(self.prosp_water_amount)

        # SEWER
        self.retro_sewer_verif = bzio.ReadScreen(1, 16, 35).replace("_", "")
        self.retro_sewer_amount = bzio.ReadScreen(8, 16, 41).strip().replace("_", "")
        if self.retro_sewer_amount:
            self.retro_sewer_amount = float(self.retro_sewer_amount)
        self.prosp_sewer_verif = bzio.ReadScreen(1, 16, 55).replace("_", "")
        self.prosp_sewer_amount = bzio.ReadScreen(8, 16, 61).strip().replace("_", "")
        if self.prosp_sewer_amount:
            self.prosp_sewer_amount = float(self.prosp_sewer_amount)

        # OTHER
        self.retro_other_verif = bzio.ReadScreen(1, 17, 35).replace("_", "")
        self.retro_other_amount = bzio.ReadScreen(8, 17, 41).strip().replace("_", "")
        if self.retro_other_amount:
            self.retro_other_amount = float(self.retro_other_amount)
        self.prosp_other_verif = bzio.ReadScreen(1, 17, 55).replace("_", "")
        self.prosp_other_amount = bzio.ReadScreen(8, 17, 61).strip().replace("_", "")
        if self.prosp_other_amount:
            self.prosp_other_amount = float(self.prosp_other_amount)

        # Reads if DWP phone is indicated and assigns T/F to property
        if bzio.ReadScreen(1, 18, 55) is "Y":
            self.dwp_phone = True
            self.dwp_amount = float(bzio.ReadScreen(8, 18, 61))
        else:
            self.dwp_phone = False
            self.dwp_amount = ""

    def create_new(self, shared, heat=[], air=[], electric=[], fuel=[], garbage=[], water=[], sewer=[], other=[], phone=False):
        """Method to add a new ACUT panel to the case
        Note on optional arguments - they are all optional - however failing input at least one will not successfully create a new panel.
        Argument Requirements:
        shared -- Boolean
        heat -- LIST in order - [retro verif, retro amount, prospective verif, prospective amount]
        air -- LIST in order - [retro verif, retro amount, prospective verif, prospective amount]
        electric -- LIST in order - [retro verif, retro amount, prospective verif, prospective amount]
        fuel -- LIST in order - [retro verif, retro amount, prospective verif, prospective amount]
        garbage -- LIST in order - [retro verif, retro amount, prospective verif, prospective amount]
        water -- LIST in order - [retro verif, retro amount, prospective verif, prospective amount]
        sewer -- LIST in order - [retro verif, retro amount, prospective verif, prospective amount]
        other -- LIST in order - [retro verif, retro amount, prospective verif, prospective amount]
        phone -- boolean - defaulted to false"""
        # navigate to STAT/ACUT for member and creates a new panel
        FuncLib.navigate_to_MAXIS_screen(self.case, self.month, self.year, "STAT", "ACUT")
        bzio.WriteScreen(self.member, 20, 76)
        bzio.WriteScreen("NN", 20, 79)
        FuncLib.transmit()

        # FIXME add function to check and ensure that new panel has been created and is in edit mode.

        # Enters the code Y or N for shared based on the Boolean and sets the property for the class
        if shared:
            bzio.WriteScreen("Y", 6, 42)
        else:
            bzio.WriteScreen("N", 6, 42)
        self.shared = shared

        if heat:                                        # checks if heat has a value
            bzio.WriteScreen(heat[0], 10, 35)           # writes retro verif to panel and assign to property
            self.retro_heat_verif = heat[0]

            bzio.WriteScreen(heat[1], 10, 41)           # writes retro amount to panel and assign to property
            self.retro_heat_amount = float(heat[1])

            bzio.WriteScreen(heat[2], 10, 55)           # writes prospective verif to panel and assign to property
            self.prosp_heat_verif = heat[2]

            bzio.WriteScreen(heat[3], 10, 61)           # writes prospective amount to panel and assigns to property
            self.prosp_heat_amount = float(heat[3])
        else:                                           # if list is empty the property names are called and defined as null
            self.retro_heat_verif = None
            self.retro_heat_amount = None
            self.prosp_heat_verif = None
            self.prosp_heat_amount = None

        if air:
            bzio.WriteScreen(air[0], 11, 35)           # writes retro verif to panel and assign to property
            self.retro_air_verif = air[0]

            bzio.WriteScreen(air[1], 11, 41)           # writes retro amount to panel and assign to property
            self.retro_air_amount = float(air[1])

            bzio.WriteScreen(air[2], 11, 55)           # writes prospective verif to panel and assign to property
            self.prosp_air_verif = air[2]

            bzio.WriteScreen(air[3], 11, 61)           # writes prospective amount to panel and assigns to property
            self.prosp_air_amount = float(air[3])
        else:                                           # if list is empty the property names are called and defined as null
            self.retro_air_verif = None
            self.retro_air_amount = None
            self.prosp_air_verif = None
            self.prosp_air_amount = None

        if electric:
            bzio.WriteScreen(electric[0], 12, 35)           # writes retro verif to panel and assign to property
            self.retro_elect_verif = electric[0]

            bzio.WriteScreen(electric[1], 12, 41)           # writes retro amount to panel and assign to property
            self.retro_elect_amount = float(electric[1])

            bzio.WriteScreen(electric[2], 12, 55)           # writes prospective verif to panel and assign to property
            self.prosp_elect_verif = electric[2]

            bzio.WriteScreen(electric[3], 12, 61)           # writes prospective amount to panel and assigns to property
            self.prosp_elect_amount = float(electric[3])
        else:                                           # if list is empty the property names are called and defined as null
            self.retro_elect_verif = None
            self.retro_elect_amount = None
            self.prosp_elect_verif = None
            self.prosp_elect_amount = None

        if fuel:
            bzio.WriteScreen(fuel[0], 13, 35)           # writes retro verif to panel and assign to property
            self.retro_fuel_verif = fuel[0]

            bzio.WriteScreen(fuel[1], 13, 41)           # writes retro amount to panel and assign to property
            self.retro_fuel_amount = float(fuel[1])

            bzio.WriteScreen(fuel[2], 13, 55)           # writes prospective verif to panel and assign to property
            self.prosp_fuel_verif = fuel[2]

            bzio.WriteScreen(fuel[3], 13, 61)           # writes prospective amount to panel and assigns to property
            self.prosp_fuel_amount = float(fuel[3])
        else:                                           # if list is empty the property names are called and defined as null
            self.retro_fuel_verif = None
            self.retro_fuel_amount = None
            self.prosp_fuel_verif = None
            self.prosp_fuel_amount = None

        if garbage:
            bzio.WriteScreen(garbage[0], 14, 35)           # writes retro verif to panel and assign to property
            self.retro_garbage_verif = garbage[0]

            bzio.WriteScreen(garbage[1], 14, 41)           # writes retro amount to panel and assign to property
            self.retro_garbage_amount = float(garbage[1])

            bzio.WriteScreen(garbage[2], 14, 55)           # writes prospective verif to panel and assign to property
            self.prosp_garbage_verif = garbage[2]

            bzio.WriteScreen(garbage[3], 14, 61)           # writes prospective amount to panel and assigns to property
            self.prosp_garbage_amount = float(garbage[3])
        else:                                           # if list is empty the property names are called and defined as null
            self.retro_garbage_verif = None
            self.retro_garbage_amount = None
            self.prosp_garbage_verif = None
            self.prosp_garbage_amount = None

        if water:
            bzio.WriteScreen(water[0], 15, 35)           # writes retro verif to panel and assign to property
            self.retro_water_verif = water[0]

            bzio.WriteScreen(water[1], 15, 41)           # writes retro amount to panel and assign to property
            self.retro_water_amount = float(water[1])

            bzio.WriteScreen(water[2], 15, 55)           # writes prospective verif to panel and assign to property
            self.prosp_water_verif = water[2]

            bzio.WriteScreen(water[3], 15, 61)           # writes prospective amount to panel and assigns to property
            self.prosp_water_amount = float(water[3])
        else:                                           # if list is empty the property names are called and defined as null
            self.retro_water_verif = None
            self.retro_water_amount = None
            self.prosp_water_verif = None
            self.prosp_water_amount = None

        if sewer:
            bzio.WriteScreen(sewer[0], 16, 35)           # writes retro verif to panel and assign to property
            self.retro_sewer_verif = sewer[0]

            bzio.WriteScreen(sewer[1], 16, 41)           # writes retro amount to panel and assign to property
            self.retro_sewer_amount = float(sewer[1])

            bzio.WriteScreen(sewer[2], 16, 55)           # writes prospective verif to panel and assign to property
            self.prosp_sewer_verif = sewer[2]

            bzio.WriteScreen(sewer[3], 16, 61)           # writes prospective amount to panel and assigns to property
            self.prosp_sewer_amount = float(sewer[3])
        else:                                           # if list is empty the property names are called and defined as null
            self.retro_sewer_verif = None
            self.retro_sewer_amount = None
            self.prosp_sewer_verif = None
            self.prosp_sewer_amount = None

        if other:
            bzio.WriteScreen(other[0], 17, 35)           # writes retro verif to panel and assign to property
            self.retro_other_verif = other[0]

            bzio.WriteScreen(other[1], 17, 41)           # writes retro amount to panel and assign to property
            self.retro_other_amount = float(other[1])

            bzio.WriteScreen(other[2], 17, 55)           # writes prospective verif to panel and assign to property
            self.prosp_other_verif = other[2]

            bzio.WriteScreen(other[3], 17, 61)           # writes prospective amount to panel and assigns to property
            self.prosp_other_amount = float(other[3])
        else:                                           # if list is empty the property names are called and defined as null
            self.retro_other_verif = None
            self.retro_other_amount = None
            self.prosp_other_verif = None
            self.prosp_other_amount = None

        # if phone is set to true then Y willbe entered to the panel
        # otherwise the phone indicator will be blank on the panel
        if phone:
            bzio.WriteScreen("Y", 18, 55)
        self.dwp_phone = phone      # setting the phone boolean to the class property

        FuncLib.transmit()

        self.dwp_amount = bzio.ReadScreen(8, 18, 61)
        self.dwp_amount = self.dwp_amount.strip()
        if self.dwp_amount:
            self.dwp_amount = float(self.dwp_amount)

    # TODO create method to change a specific expense amount (should take parameter for which expense to change and a ditionary for each option)
    # TODO create a method to change shared boolean and dwp phone boolean

class STAT_ADDR_panel:
    """class references STAT/ADDR
    Methods: gather_data -- get all information from existing panel"""
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    # Dictionaries set up with details explaining codes on panels
    # PF1 has this information stored - adding it here for reference within the class
    # it is more helpful to have the explanations of the codes than just the bare codes
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

        # Navigates to STAT/ADDR - no instance or member needed as there is only 1 in each case
        FuncLib.navigate_to_MAXIS_screen(self.case, self.month, self.year, "STAT", "ADDR")

        # reading all information from the panel and assigning it to class properties
        self.effective_date = "%s/%s/%s" % (bzio.ReadScreen(2, 4, 43), bzio.ReadScreen(2, 4, 46), bzio.ReadScreen(2, 4, 49))  # formatting date as mm/dd/yy

        # string variables have '_' in line - removing those because we don't write like that
        self.resi1 = bzio.ReadScreen(22, 6, 43).replace("_", "")
        self.resi2 = bzio.ReadScreen(22, 7, 43).replace("_", "")
        self.resi_city = bzio.ReadScreen(15, 8, 43).replace("_", "")
        self.resi_state = bzio.ReadScreen(2, 8, 66).replace("_", "")
        self.resi_zip = bzio.ReadScreen(5, 9, 43)
        self.resi_cty = bzio.ReadScreen(2, 9, 66)
        verif_code = bzio.ReadScreen(2, 9, 74)
        self.resi_verif = addr_verif_codes[verif_code]      # setting the verification to information from dictionary

        if bzio.ReadScreen(1, 10, 43) == "Y":               # setting this property as a boolean instead of Y/N because that makes more sense
            self.homeless = True
        else:
            self.homeless = False

        if bzio.ReadScreen(1, 10, 74) == "Y":               # only if on reservation will the script pull reservation information
            self.reservation = True
            self.reservation_code = bzio.ReadScreen(2, 11, 74)
            self.reservation_name = all_res_codes[self.reservation_code]    # name set by dictionary defined above
        else:
            self.reservation = False

        self.living_situation = bzio.ReadScreen(22, 6, 43).replace("_", "")

        if bzio.ReadScreen(22, 13, 43).replace("_", "") != "":      # only reading all of the mailing address if it appears there is a mailing address
            self.diff_mail = True                                   # sets a property to help identify if there is a mailing address
            self.mail1 = bzio.ReadScreen(22, 13, 43).replace("_", "")
            self.mail2 = bzio.ReadScreen(22, 14, 43).replace("_", "")
            self.mail_city = bzio.ReadScreen(15, 15, 43).replace("_", "")
            self.mail_state = bzio.ReadScreen(2, 16, 43).replace("_", "")
            self.mail_zip = bzio.ReadScreen(5, 16, 52).replace("_", "")
        else:
            self.diff_mail = False

        # reading phone information and creating a list.
        self.phone_one = "%s-%s-%s" % (bzio.ReadScreen(3, 17, 45), bzio.ReadScreen(3, 17, 51), bzio.ReadScreen(4, 17, 55))
        self.phone_two = "%s-%s-%s" % (bzio.ReadScreen(3, 18, 45), bzio.ReadScreen(3, 18, 51), bzio.ReadScreen(4, 18, 55))
        self.phone_three = "%s-%s-%s" % (bzio.ReadScreen(3, 19, 45), bzio.ReadScreen(3, 19, 51), bzio.ReadScreen(4, 19, 55))

        # this list can be used in a combobox so that a dialog can have the option to select known phone numbers
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
    """Class that references STAT/ADME - needs member input
    Methods in this class: gather_data - to read all information on panel
                           create_new - to create a new ADME panel for a specified member"""
    def __init__(self, case_number, footer_month, footer_year, member):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year
        self.member = member

    def gather_data(self):
        """This method will read the panel and save to class properties
        Class Properties: self.birthdate -- listed on ADME in mm/dd/yy format
                          self.arrival_date -- date as listed on ADME in mm/dd/yy format
                          self.cash_add_date -- date listed on ADME in mm/dd/yy format - will be None if date is not filled in
                          self.emer_add_date -- date listed on ADME in mm/dd/yy format - will be None if date is not filled in
                          self.snap_add_date -- date listed on ADME in mm/dd/yy format - will be None if date is not filled in"""

        # navigate to the correct STAT/ADME panel
        FuncLib.navigate_to_MAXIS_screen(self.case, self.month, self.year, "STAT", "ADME")
        bzio.WriteScreen(self.member, 20, 76)
        FuncLib.transmit()

        if bzio.ReadScreen(1, 2, 73) != "0":                # checking to be sure a panel exists
            self.birthdate = bzio.ReadScreen(8, 5, 36)      # reading birthdate and arrival date from ADME
            self.arrival_date = bzio.ReadScreen(8, 7, 38)

            # reads cash addendum/reporting date for each program and formats it in mm/dd/yy
            self.cash_add_date = "%s/%s/%s" % (bzio.ReadScreen(8, 12, 38), bzio.ReadScreen(8, 12, 41), bzio.ReadScreen(8, 12, 44))     # cash
            if self.cash_add_date == "__/__/__":        # if the date is not entered reset the property to None
                self.cash_add_date = None

            self.cash_add_date = "%s/%s/%s" % (bzio.ReadScreen(8, 14, 38), bzio.ReadScreen(8, 14, 41), bzio.ReadScreen(8, 14, 44))     # emergency
            if self.cash_add_date == "__/__/__":        # if the date is not entered reset the property to None
                self.cash_add_date = None

            self.cash_add_date = "%s/%s/%s" % (bzio.ReadScreen(8, 16, 38), bzio.ReadScreen(8, 16, 41), bzio.ReadScreen(8, 16, 44))     # snap
            if self.cash_add_date == "__/__/__":        # if the date is not entered reset the property to None
                self.cash_add_date = None
        else:
            self.birthdate = None
            self.arrival_date = None
            self.cash_add_date = None
            self.emer_add_date = None
            self.snap_add_date = None

    def create_new(self, cash_date, emer_date, fs_date):
        """Method to create a new ADME panel for the specified member
        Arguments: cash_date -- date to add person for cash
                   emer_date -- date to add person for emergency assistance
                   fs_date -- date to add person for fs/snap
        All arguments are required - script must determine which are important."""

        # navigate to the correct STAT/ADME panel
        FuncLib.navigate_to_MAXIS_screen(self.case, self.month, self.year, "STAT", "ADME")
        bzio.WriteScreen(self.member, 20, 76)
        bzio.WriteScreen("NN", 20, 79)
        FuncLib.transmit()

        # FIXME Add function to check to be sure the panel is in edit mode

        self.cash_add_date = cash_date          # assign cash date to class property
        if self.cash_add_date:
            FuncLib.write_mainframe_date(self.cash_add_date, "XX XX XX", [12, 38], [12, 41], [12, 44])

        self.emer_add_date = emer_date          # assign emer date to class property
        if self.emer_add_date:
            FuncLib.write_mainframe_date(self.emer_add_date, "XX XX XX", [14, 38], [14, 41], [14, 44])

        self.snap_add_date = fs_date            # assign fs date to class property
        if self.snap_add_date:
            FuncLib.write_mainframe_date(self.snap_add_date, "XX XX XX", [16, 38], [16, 41], [16, 44])

        FuncLib.transmit()      # transmit to save the panel. The arrival date and birth date will autopopulate once panel is saved

        self.birthdate = bzio.ReadScreen(8, 5, 36)      # reading birthdate and arrival date from ADME
        self.arrival_date = bzio.ReadScreen(8, 7, 38)


class STAT_ALIA_panel:
    """Class to reference STAT/ALIA - member reference needed
    Methods in this class: gather_data -- collect information from ALIA panel and assign to properties
                           add_alias_name -- add one name to the ALIA panel
                           add_secondary_ssn -- add one SSN to the ALIA panel"""
    def __init__(self, case_number, footer_month, footer_year, member):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year
        self.member = member

    def gather_data(self):
        """Method to gather information for STAT/ALIA for the specific member indicated.
        Properties created: self.alias_names -- Dictionary of names in ALIA - key is the MAXIS row, value is a list last name, first name, middle initial
                            self.secondary_ssns -- Dictionary of ssns in ALIA - key is row, col, value is the ssn and verif
                            self.alias_exists -- boolean to identify if any information is listed for member as alias names
                            self.secondary_ssn_exists -- boolean to identify if a secondary ssn exists"""

        # navigate to the correct STAT/ALIA panel
        FuncLib.navigate_to_MAXIS_screen(self.case, self.month, self.year, "STAT", "ALIA")
        bzio.WriteScreen(self.member, 20, 76)
        FuncLib.transmit()

        self.alias_names = {}               # setting the property to a dictionary so that adding key and value pairs is easiest
        self.alias_exists = True            # setting this as true for the default - easier to read for a a false and reset if false.

        row = 7
        last_name = bzio.ReadScreen(17, row, 26).replace("_", "")          # reading the first line of the names
        first_name = bzio.ReadScreen(12, row, 53).replace("_", "")
        middle_initial = bzio.ReadScreen(1, row, 75).replace("_", "")

        if first_name == "" and last_name == "":                            # if the first line is blank, setting the property to false
            self.alias_exists = False

        while last_name != "" and first_name != "":
            self.alias_names[row] = [last_name, first_name, middle_initial]

            row += 1
            last_name = bzio.ReadScreen(17, row, 26).replace("_", "")          # reading each row in turn until a blank line is hit.
            first_name = bzio.ReadScreen(12, row, 53).replace("_", "")
            middle_initial = bzio.ReadScreen(1, row, 75).replace("_", "")

        self.secondary_ssns = {}            # setting the property to a dictionary so adding key an value pairs is easist
        self.secondary_ssn_exists = True    # setting to true as default - easier to identify if this is false, will reset if false

        row = 15
        col = 28

        soc_sec_nbr = "%s-%s-%s" % (bzio.ReadScreen(3, row, col), bzio.ReadScreen(2, row, col + 4), bzio.ReadScreen(4, row, col + 7))

        if soc_sec_nbr == "___-__-____":
            self.secondary_ssn_exists = False

        while soc_sec_nbr != "___-__-____":
            ssn_verif = bzio.ReadScreen(1, row, col + 18)
            if ssn_verif == "P":
                ssn_code = "SSN Provided"
            else:
                ssn_code = "System Entered SSN Ver via an Interface"
            self.secondary_ssns[row, col] = [soc_sec_nbr, ssn_code]

            col += 25
            if col == 78:
                row += 1
                col = 28

            if row == 18:
                break

            soc_sec_nbr = "%s-%s-%s" % (bzio.ReadScreen(3, row, col), bzio.ReadScreen(2, row, col + 4), bzio.ReadScreen(4, row, col + 7))

    def add_alias_name(self, last_name, first_name, middle):
        """Method to add an alias name to the panel
        This panel dows not need to be created as it is automatically created - it only needs to be updated.
        Arguments: last_name -- last name to be entered in to ALIA
                   first_name -- first name to be entered in to ALIA
                   middle -- middle initial to be entered in ALIA"""

        # navigate to the correct STAT/ALIA panel
        FuncLib.navigate_to_MAXIS_screen(self.case, self.month, self.year, "STAT", "ALIA")
        bzio.WriteScreen(self.member, 20, 76)
        FuncLib.transmit()
        FuncLib.PF9()           # Put panel in edit mode

        # TODO May need error handling for if the ALIA name lines are FULL
        # name is written on the last line.
        # MAXIS will move the name to the top most available line once changes are submitted.
        bzio.WriteScreen(last_name, 12, 26)
        bzio.WriteScreen(first_name, 12, 53)
        bzio.WriteScreen(middle, 12, 75)

        FuncLib.transmit()                  # submits the information to the page and saves
        self.gather_data()                  # gets the panel properties

    def add_secondary_ssn(self, ssn):
        """Method to add a ssn to the ALIA panel.
        This panel does not need to be created as it is automatically created - it only needs to be updated.
        Arguments: ssn -- the secondary ssn to document on ALIA. FORMAT: xxx-xx-xxxx
                   do not need to assign a verif as the only worker entry is 'P'"""

        # navigate to the correct STAT/ALIA panel
        FuncLib.navigate_to_MAXIS_screen(self.case, self.month, self.year, "STAT", "ALIA")
        bzio.WriteScreen(self.member, 20, 76)
        FuncLib.transmit()
        FuncLib.PF9()           # Put panel in edit mode

        # TODO May need error handling for if the ALIA ssn lines are FULL
        # ssn is written to the last place for ssns.
        # MAXIS will move the ssn to the top most availablt line once hacanges are submitted.
        ssn_list = ssn.split("-")                       # seperates each element of the ssn and writes them seperately into the panel
        bzio.WriteScreen(ssn_list[0], 17, 53)
        bzio.WriteScreen(ssn_list[1], 17, 57)
        bzio.WriteScreen(ssn_list[2], 17, 60)
        bzio.WriteScreen("P", 17, 71)                   # enters the verif code of 'P' as that is the only valid worker entry

        FuncLib.transmit()                  # submits the information to the page and saves
        self.gather_data()                  # gets the panel properties


class STAT_ALTP_panel:
    """Class to reference STAT/ALTP - NO instance/member needed
    Methods in this class: gather_data() -- get information from ALTP panel and assign to properties
                           create_new() -- create a new ALTP panel/add Alt Payee to case.
                           end_payee() -- set date for payee to end
                           change_payee() -- if current payee exists, will change the payee to new entry"""
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    global payee_reason
    payee_reason = {"1": "Voluntary",
                    "3": "IV-D N/Coop",
                    "4": "Money Mismanagemnt",
                    "5": "Death of Payee",
                    "6": "Temp Absence of Payee",
                    "7": "Guardian",
                    "8": "Emergency Payee",
                    "9": "MFIP Minor Residing with Parent"}

    def gather_data(self):
        """Method to read the ALTP panel and add all inforamtion to class properties.
        Properties created: reason -- Information about why payee exists (full detail from PF1 menu)
                            start_date -- date that payee change starts - format mm/dd/yy
                            end_date -- date that payee ends - format mm/dd/yy - may be 'None' if blank
                            name -- Name of payee
                            street -- address house and street (line 1 and line 2)
                            city -- city of address
                            state -- 2 digit state abr code for address
                            zip -- 5 digit zip code for address
                            phone -- phone number of alt payee - format xxx-xxx-xxxx
                            phone_ext -- estension """

        # navigate to the STAT/ALTP panel
        FuncLib.navigate_to_MAXIS_screen(self.case, self.month, self.year, "STAT", "ALTP")

        reason_code = bzio.ReadScreen(1, 5, 37)
        self.reason = payee_reason[reason_code]
        self.start_date = "%s/%s/%s" % (bzio.ReadScreen(2, 8, 37), bzio.ReadScreen(2, 8, 40), bzio.ReadScreen(2, 8, 43))
        self.end_date = "%s/%s/%s" % (bzio.ReadScreen(2, 8, 60), bzio.ReadScreen(2, 8, 63), bzio.ReadScreen(2, 8, 66))
        if self.end_date == "__/__/__":
            self.end_date = None

        self.name = bzio.ReadScreen(30, 11, 37).replace("_", "")
        self.street = "%s %s" % (bzio.ReadScreen(22, 12, 37).replace("_", ""), bzio.ReadScreen(22, 13, 37).replace("_", ""))
        self.city = bzio.ReadScreen(15, 14, 37).replace("_", "")
        self.state = bzio.ReadScreen(2, 14, 60).replace("_", "")
        self.zip = bzio.ReadScreen(5, 14, 69).replace("_", "")

        self.phone = "%s-%s-%s" % (bzio.ReadScreen(3, 16, 39), bzio.ReadScreen(3, 16, 45), bzio.ReadScreen(4, 16, 49))
        if self.phone == "___-___-____":
            self.phone = None
        self.phone_ext = bzio.ReadScreen(3, 16, 60).replace("_", "")

    def create_new(self, reason_code, start_date, name, street, city, state, zip, end_date=None, phone=None, ext=None):
        """This method will create a new ALTP panel with alternate payee information provided by arguments.
        Argument requirements: reason_code -- single digit code to explain the reason for alt payee (options: 1, 3, 4, 5, 6, 7, 8, 9)
                               start_date -- date the alternate payee to begin
                               name -- Name of the Alt Payee
                               street -- street address of alt payee (lines 1 and 2 together)
                               city -- city of address of alt payee
                               state - state abbreviation of alt payee address
                               zip -- 5 digit zip code of alt payee address
            Optional Arguments:
                               end_date -- date alt payee to be ended
                               phone -- phone number of alt payee - format xxx-xxx-xxxx
                               ext -- extension of phone number of alt payee"""

        # navigate to the STAT/ALTP panel
        FuncLib.navigate_to_MAXIS_screen(self.case, self.month, self.year, "STAT", "ALTP")
        bzio.WriteScreen("NN", 20, 79)      # create new panel and transmit to put it in edit mode
        FuncLib.transmit()

        # writing arguments to the panel
        bzio.WriteScreen(reason_code, 5, 37)
        FuncLib.write_mainframe_date(start_date, "XX XX XX", [8, 37], [8, 40], [8, 43])     # using function to seperate and write date in panel
        bzio.WriteScreen(name, 11, 37)
        if len(street) <= 22:                       # addresses may be on more than one line
            bzio.WriteScreen(street, 12, 37)        # maximum length of line is 22, if the address is smaller, one line is suficient
        else:
            row = 12
            col = 37
            word_list = street.split()              # split the address into a list of words
            for word in word_list:                  # each word will be written seperately
                if col + len(word) >= 58:           # evaluates location, to ensure the line break happens at the right place
                    if row == 13:                   # if we have already reached the end of the second line - the loop will end - some words may be missed
                        break
                    row = 13
                    col = 37
                word = word + " "                   # add 1 space to the end of the word
                bzio.WriteScreen(word, row, col)
                col += len(word)                    # move to the next word location
        bzio.WriteScreen(city, 14, 37)
        bzio.WriteScreen(state, 14, 60)
        bzio.WriteScreen(zip, 14, 69)

        if end_date:                               # if there is an end date entered - date will be written to panel
            FuncLib.write_mainframe_date(end_date, "XX XX XX", [8, 60], [8, 63], [8, 66])

        if phone:                                   # if a phone number is entered
            phone_list = phone.split("-")           # seperating phone number in to individual elements for entry
            bzio.WriteScreen(phone_list[0], 16, 39)     # each element is written to the panel
            bzio.WriteScreen(phone_list[1], 16, 45)
            bzio.WriteScreen(phone_list[2], 16, 49)

        if ext:                                     # if an extension is provided
            bzio.WriteScreen(ext, 16, 60)           # it will be written to the panel

        FuncLib.transmit()                          # transmit to save the date written to the panel
        self.gather_data()                          # fill all the class properties using the gather_data method.

    def end_payee(self, end_date):
        """Method used to enter the end of alt payee
        Argument: end_date -- date to end the alt payee"""
        # navigate to the STAT/ALTP panel and put it in edit mode
        FuncLib.navigate_to_MAXIS_screen(self.case, self.month, self.year, "STAT", "ALTP")
        FuncLib.PF9()

        # FIXME add function to be sure the panel is in edit mode

        # entering the end date to the panel
        FuncLib.write_mainframe_date(end_date, "XX XX XX", [8, 60], [8, 63], [8, 66])

        FuncLib.transmit()                          # transmit to save the date written to the panel
        # rereading the end date information and saving it to the class property
        # doing it this way to make sure the property is formatted the same way as if it had been read using gather_data Method
        self.end_date = "%s/%s/%s" % (bzio.ReadScreen(2, 8, 60), bzio.ReadScreen(2, 8, 63), bzio.ReadScreen(2, 8, 66))

    def change_payee(self, reason_code, start_date, name, street, city, state, zip, end_date=None, phone=None, ext=None):
        """Method to change the payee information on ALTP
        Argument requirements: reason_code -- single digit code to explain the reason for alt payee (options: 1, 3, 4, 5, 6, 7, 8, 9)
                               start_date -- date the alternate payee to begin
                               name -- Name of the Alt Payee
                               street -- street address of alt payee (lines 1 and 2 together)
                               city -- city of address of alt payee
                               state - state abbreviation of alt payee address
                               zip -- 5 digit zip code of alt payee address
            Optional Arguments:
                               end_date -- date alt payee to be ended
                               phone -- phone number of alt payee - format xxx-xxx-xxxx
                               ext -- extension of phone number of alt payee"""
        # navigate to the STAT/ALTP panel and put it in edit mode
        FuncLib.navigate_to_MAXIS_screen(self.case, self.month, self.year, "STAT", "ALTP")
        FuncLib.PF9()

        # FIXME add function to be sure the panel is in edit mode

        # writing arguments to the panel
        bzio.WriteScreen(reason_code, 5, 37)
        FuncLib.write_mainframe_date(start_date, "XX XX XX", [8, 37], [8, 40], [8, 43])     # using function to seperate and write date in panel

        spaces_to_add = 30 - len(name)              # add whitespace to the end of the string to be sure any old data is deleted
        name = name.ljust(spaces_to_add)
        bzio.WriteScreen(name, 11, 37)

        bzio.WriteScreen(" " * 22, 12, 37)          # blanking out the address spaces before entering new data since writing here is more complex
        bzio.WriteScreen(" " * 22, 13, 37)

        if len(street) <= 22:                       # addresses may be on more than one line
            bzio.WriteScreen(street, 12, 37)        # maximum length of line is 22, if the address is smaller, one line is suficient
        else:
            row = 12
            col = 37
            word_list = street.split()              # split the address into a list of words
            for word in word_list:                  # each word will be written seperately
                if col + len(word) >= 58:           # evaluates location, to ensure the line break happens at the right place
                    if row == 13:                   # if we have already reached the end of the second line - the loop will end - some words may be missed
                        break
                    row = 13
                    col = 37
                word = word + " "                   # add 1 space to the end of the word
                bzio.WriteScreen(word, row, col)
                col += len(word)                    # move to the next word location

        spaces_to_add = 15 - len(city)              # add white space to the end of the string to be sure any old data is deleted
        city = city.ljust(spaces_to_add)
        bzio.WriteScreen(city, 14, 37)              # write info and whitespace to the panel

        bzio.WriteScreen(state, 14, 60)
        bzio.WriteScreen(zip, 14, 69)

        if end_date:                               # if there is an end date entered - date will be written to panel
            FuncLib.write_mainframe_date(end_date, "XX XX XX", [8, 60], [8, 63], [8, 66])
        else:
            bzio.WriteScreen("  ", 8, 60)           # if no end date provided - blanking out the field in case old data is there
            bzio.WriteScreen("  ", 8, 63)
            bzio.WriteScreen("  ", 8, 66)

        if phone:                                   # if a phone number is entered
            phone_list = phone.split("-")           # seperating phone number in to individual elements for entry
            bzio.WriteScreen(phone_list[0], 16, 39)     # each element is written to the panel
            bzio.WriteScreen(phone_list[1], 16, 45)
            bzio.WriteScreen(phone_list[2], 16, 49)
        else:                                       # if no phone information provided - blanking out the field in case old data is here
            bzio.WriteScreen("   ", 16, 39)
            bzio.WriteScreen("   ", 16, 45)
            bzio.WriteScreen("    ", 16, 49)

        if ext:                                     # if an extension is provided
            bzio.WriteScreen(ext, 16, 60)           # it will be written to the panel
        else:                                       # if no extension provided - blanking out the field in case old data is here
            bzio.WriteScreen("   ", 16, 60)

        FuncLib.transmit()                          # transmit to save the date written to the panel
        self.gather_data()                          # fill all the class properties using the gather_data method.


class STAT_AREP_panel:
    """This class references the STAT/AREP panel
    NO member or instance needed for this panel
    Methods in this class: gather_data -- collect information from an existing panel
                           create_new -- create a new panel and fill in AREP information"""
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        """This method will gather information from an existing AREP panel and add the information to class properties.
        Properties created: AREP_exists -- boolean if AREP information is present
                            name -- AREP's name (string)
                            street -- the street address of the AREP - will include both lines (string)
                            city -- city of AREP's address (string)
                            state -- state abbrv code of AREP's address (string)
                            zip -- zip code of AREP's address (string)
                            disq -- boolean to determine if AREP is disqualified or not
                            months_disq -- months to disqualify AREP (string)
                            phone_one -- AREP's first phone number - format xxx-xxx-xxxx (will be None if blank)
                            ext_one -- extension of AREP's first phone number
                            phone_two -- AREP's second phone number - format xxx-xxx-xxxx (will be None if blank)
                            ext_two -- extension of AREP's second phone number
                            forms_to_AREP -- boolean for if forms should go to AREP
                            MMIS_mail_to_AREP - boolean for if MMIS mail should go to AREP

                            FS_alt_rep_exists -- boolean if Food Support Alternat Representative exists
                            FS_alt_rep_name -- FS Alternate Representative's name (string)
                            FS_alt_rep_street -- the street address of the FS Alt Rep - will include both lines (string)
                            FS_alt_rep_city -- city of FS Alt Rep's address (string)
                            FS_alt_rep_state -- state abbrv code of FS Alt Rep's address (string)
                            FS_alt_rep_zip -- zip code of FS Alt Rep's address (string)
                            FS_alt_rep_disq -- boolean to determine if FS Alt Rep is disqualified or not
                            FS_alt_rep_months_disq -- months to disqualify FS Alt Rep (string)
                            FS_alt_rep_phone_one -- FS Alt Rep's first phone number - format xxx-xxx-xxxx (will be None if blank)
                            FS_alt_rep_ext_one -- extension of FS Alt Rep's first phone number
                            FS_alt_rep_phone_two -- FS Alt Rep's second phone number - format xxx-xxx-xxxx (will be None if blank)
                            FS_alt_rep_ext_two -- extension of FS Alt Rep's second phone number"""

        # navigate to the STAT/AREP panel
        at_AREP = bzio.ReadScreen(4, 2, 53)
        if at_AREP != "AREP":
            FuncLib.navigate_to_MAXIS_screen(self.case, self.month, self.year, "STAT", "AREP")

        self.AREP_exists = True
        self.FS_alt_rep_exists = True

        # reading the information from the top of the panel and assigning it to properties - AREP
        self.name = bzio.ReadScreen(37, 4, 32).replace("_", "")
        if self.name is "":
            self.AREP_exists = False
        self.street = "%s %s" % (bzio.ReadScreen(22, 5, 32).replace("_", ""), bzio.ReadScreen(22, 6, 32).replace("_", ""))   # reads both lines and concantenate
        self.street = self.street.strip()           # removing space from the property
        self.city = bzio.ReadScreen(15, 7, 32).replace("_", "")
        self.state = bzio.ReadScreen(2, 7, 55)
        self.zip = bzio.ReadScreen(5, 7, 64)

        self.phone_one = "%s-%s-%s" % (bzio.ReadScreen(3, 8, 34), bzio.ReadScreen(3, 8, 40), bzio.ReadScreen(4, 8, 44))     # formatting the phone number
        if self.phone_one == "___-___-____":                                                                                # set to none if blank
            self.phone_one = None
        self.ext_one = bzio.ReadScreen(3, 8, 55).replace("_", "")

        self.phone_two = "%s-%s-%s" % (bzio.ReadScreen(3, 9, 34), bzio.ReadScreen(3, 9, 40), bzio.ReadScreen(4, 9, 44))     # formatting the phone number
        if self.phone_two == "___-___-____":                                                                                # set to none if blank
            self.phone_two = None
        self.ext_two = bzio.ReadScreen(3, 9, 55).replace("_", "")

        if bzio.ReadScreen(1, 5, 77) == "Y":                        # If disqualify is 'Y' then this AREP is disqualified - set to true
            self.disq = True
        else:
            self.disq = False
        self.months_disq = bzio.ReadScreen(2, 6, 77).replace("_", "")

        self.forms_to_AREP = False                          # setting this to false as default
        if bzio.ReadScreen(1, 10, 45) == "Y":               # if 'Y' code found - this will change the boolean to True
            self.forms_to_AREP = True

        self.MMIS_mail_to_AREP = False                      # setting this to false as default
        if bzio.ReadScreen(1, 10, 77) == "Y":               # if 'Y' code found - this will change the boolean to True
            self.MMIS_mail_to_AREP = True

        # reading the information from the bottom of the panel and assigning it to properties - FS Alt Rep
        self.FS_alt_rep_name = bzio.ReadScreen(37, 13, 32).replace("_", "")
        if self.FS_alt_rep_name is "":
            self.FS_alt_rep_exists = False
        # reads both lines and concantenates
        self.FS_alt_rep_street = "%s %s" % (bzio.ReadScreen(22, 14, 32).replace("_", ""), bzio.ReadScreen(22, 15, 32).replace("_", ""))
        self.FS_alt_rep_street = self.FS_alt_rep_street.strip()           # removing space from the property
        self.FS_alt_rep_city = bzio.ReadScreen(15, 16, 32).replace("_", "")
        self.FS_alt_rep_state = bzio.ReadScreen(2, 16, 55)
        self.FS_alt_rep_zip = bzio.ReadScreen(5, 16, 64)

        # formatting the phone number
        self.FS_alt_rep_phone_one = "%s-%s-%s" % (bzio.ReadScreen(3, 17, 34), bzio.ReadScreen(3, 17, 40), bzio.ReadScreen(4, 17, 44))
        if self.FS_alt_rep_phone_one == "___-___-____":             # set to none if blank
            self.FS_alt_rep_phone_one = None
        self.FS_alt_rep_ext_one = bzio.ReadScreen(3, 17, 55).replace("_", "")

        # formatting the phone number
        self.FS_alt_rep_phone_two = "%s-%s-%s" % (bzio.ReadScreen(3, 18, 34), bzio.ReadScreen(3, 18, 40), bzio.ReadScreen(4, 18, 44))
        if self.FS_alt_rep_phone_two == "___-___-____":             # set to none if blank
            self.FS_alt_rep_phone_two = None
        self.FS_alt_rep_ext_two = bzio.ReadScreen(3, 18, 55).replace("_", "")

        if bzio.ReadScreen(1, 14, 77) == "Y":                        # If disqualify is 'Y' then this AREP is disqualified - set to true
            self.FS_alt_rep_disq = True
        else:
            self.FS_alt_rep_disq = False
        self.FS_alt_rep_months_disq = bzio.ReadScreen(2, 15, 77).replace("_", "")

    def update_auth_rep(self, name, street, city, state, zip, disq="N", forms_to_AREP="Y", MMIS_mail_to_AREP="Y",
                        phone_one=None, ext_one=None, phone_two=None, ext_two=None, months_of_disq=None):
        """Method to add or change an Authorized Representative.
        If panel exists, method will simply update, if no panel exists, one will be created.
        Arguments: name -- name of AREP
                   street/city/state/zip -- address of AREP
                   disq -- if AREP is disqualified as an AREP - default to N
                   forms_to_AREP -- if MAXIS mail goes to AREP - defaulted to Y
                   MMIS_mail_to_AREP -- if MMIS mail goies to AREP - defaulted to Y
            Optional Arguments:
                   phone_one -- AREP phone number (xxx-xxx-xxxx format)
                   ext_one -- AREP phone one extension
                   phone_two -- AREP phone number (xxx-xxx-xxxx format)
                   ext_two -- AREP phone one extension
                   months_of_disq -- number of months of disq - needed if disq is set to Y"""

        # navigate to the STAT/AREP panel
        FuncLib.navigate_to_MAXIS_screen(self.case, self.month, self.year, "STAT", "AREP")

        # putting the panel in edit mode
        if bzio.ReadScreen(1, 2, 73) == "0":    # if no panel exists - create a new one
            bzio.WriteScreen("NN", 20, 79)
            FuncLib.transmit()
        else:                                   # if a panel does exists - put in edit mode
            FuncLib.PF9()

        # FIXME add function to be sure AREP panel is in edit mode.

        # each of these args needs spaces added to the end in case we are replacing data instead of creating a new entry
        spaces_to_add = 37 - len(name)              # determine how many spaces
        name = name + (" " * spaces_to_add)         # add the spaces to the end of the word
        bzio.WriteScreen(name, 4, 32)               # write the word to the panel

        bzio.WriteScreen(" " * 22, 5, 32)           # blanking out the address spaces before entering new data since writing here is more complex
        bzio.WriteScreen(" " * 22, 6, 32)

        if len(street) <= 22:                       # addresses may be on more than one line
            bzio.WriteScreen(street, 5, 32)         # maximum length of line is 22, if the address is smaller, one line is suficient
        else:
            row = 5
            col = 32
            word_list = street.split()              # split the address into a list of words
            for word in word_list:                  # each word will be written seperately
                if col + len(word) >= 53:           # evaluates location, to ensure the line break happens at the right place
                    if row == 6:                   # if we have already reached the end of the second line - the loop will end - some words may be missed
                        break
                    row = 6
                    col = 32
                word = word + " "                   # add 1 space to the end of the word
                bzio.WriteScreen(word, row, col)
                col += len(word)                    # move to the next word location

        spaces_to_add = 15 - len(city)              # determine how many spaces
        city = city + (" " * spaces_to_add)         # add the spaces to the end of the word
        bzio.WriteScreen(city, 7, 32)

        # these don't need spaces as they are fixed lengths
        bzio.WriteScreen(state, 7, 55)
        bzio.WriteScreen(zip, 7, 64)

        if phone_one:                               # if a phone number is entered
            phone_list = phone_one.split("-")           # seperating phone number in to individual elements for entry
            bzio.WriteScreen(phone_list[0], 8, 34)     # each element is written to the panel
            bzio.WriteScreen(phone_list[1], 8, 40)
            bzio.WriteScreen(phone_list[2], 8, 44)

            if ext_one:                             # extension only makes sense if a phone is entered
                bzio.WriteScreen(ext_one, 8, 55)
        else:                                       # if no phone information provided - blanking out the field in case old data is here
            bzio.WriteScreen("   ", 8, 34)
            bzio.WriteScreen("   ", 8, 40)
            bzio.WriteScreen("    ", 8, 44)

        if phone_two:                               # if a phone number is entered
            phone_list = phone_two.split("-")           # seperating phone number in to individual elements for entry
            bzio.WriteScreen(phone_list[0], 9, 34)     # each element is written to the panel
            bzio.WriteScreen(phone_list[1], 9, 40)
            bzio.WriteScreen(phone_list[2], 9, 44)

            if ext_two:                             # extension only makes sense if a phone is entered
                bzio.WriteScreen(ext_one, 9, 55)
        else:                                       # if no phone information provided - blanking out the field in case old data is here
            bzio.WriteScreen("   ", 9, 34)
            bzio.WriteScreen("   ", 9, 40)
            bzio.WriteScreen("    ", 9, 44)

        # writing in the disq and mail options
        bzio.WriteScreen(disq, 5, 77)
        bzio.WriteScreen(forms_to_AREP, 10, 45)
        bzio.WriteScreen(MMIS_mail_to_AREP, 10, 77)

        if months_of_disq:                          # if months of disq are indicated - write to the panel.
            bzio.WriteScreen(months_of_disq, 6, 77)

        submition_check = ""
        while submition_check != "ENTER A":
            FuncLib.transmit()                              # once all information is added to the panel - transmit to save
            submition_check = bzio.ReadScreen(7, 24, 2)     # reading to see if panel information has been saved
        self.gather_data()                                  # filling all the class properties with the new information

    def update_fs_alt_rep(self, name, street, city, state, zip, disq="N", phone_one=None, ext_one=None, phone_two=None, ext_two=None, months_of_disq=None):
        """Method to add or change a Food Support Alternate Representative.
        If panel exists, method will simply update, if no panel exists, one will be created.
        Note that this method will send the case through background to correctly update MONY/DISB
        Arguments: name -- name of AltRep
                   street/city/state/zip -- address of AltRep
                   disq -- if AltRep is disqualified as an AltRep - default to N
            Optional Arguments:
                   phone_one -- AltRep phone number (xxx-xxx-xxxx format)
                   ext_one -- AltRep phone one extension
                   phone_two -- AltRep phone number (xxx-xxx-xxxx format)
                   ext_two -- AltRep phone one extension
                   months_of_disq -- number of months of disq - needed if disq is set to Y"""

        # navigate to the STAT/AREP panel
        FuncLib.navigate_to_MAXIS_screen(self.case, self.month, self.year, "STAT", "AREP")

        # putting the panel in edit mode
        if bzio.ReadScreen(1, 2, 73) == "0":    # if no panel exists - create a new one
            bzio.WriteScreen("NN", 20, 79)
            FuncLib.transmit()
        else:                                   # if a panel does exists - put in edit mode
            FuncLib.PF9()

        # FIXME add function to be sure AREP panel is in edit mode.

        # each of these args needs spaces added to the end in case we are replacing data instead of creating a new entry
        spaces_to_add = 37 - len(name)              # determine how many spaces
        name = name + (" " * spaces_to_add)         # add the spaces to the end of the word
        bzio.WriteScreen(name, 13, 32)               # write the word to the panel

        bzio.WriteScreen(" " * 22, 14, 32)           # blanking out the address spaces before entering new data since writing here is more complex
        bzio.WriteScreen(" " * 22, 15, 32)

        if len(street) <= 22:                       # addresses may be on more than one line
            bzio.WriteScreen(street, 14, 32)         # maximum length of line is 22, if the address is smaller, one line is suficient
        else:
            row = 14
            col = 32
            word_list = street.split()              # split the address into a list of words
            for word in word_list:                  # each word will be written seperately
                if col + len(word) >= 53:           # evaluates location, to ensure the line break happens at the right place
                    if row == 15:                   # if we have already reached the end of the second line - the loop will end - some words may be missed
                        break
                    row = 15
                    col = 32
                word = word + " "                   # add 1 space to the end of the word
                bzio.WriteScreen(word, row, col)
                col += len(word)                    # move to the next word location

        spaces_to_add = 15 - len(city)              # determine how many spaces
        city = city + (" " * spaces_to_add)         # add the spaces to the end of the word
        bzio.WriteScreen(city, 16, 32)

        # these don't need spaces as they are fixed lengths
        bzio.WriteScreen(state, 16, 55)
        bzio.WriteScreen(zip, 16, 64)

        if phone_one:                               # if a phone number is entered
            phone_list = phone_one.split("-")           # seperating phone number in to individual elements for entry
            bzio.WriteScreen(phone_list[0], 17, 34)     # each element is written to the panel
            bzio.WriteScreen(phone_list[1], 17, 40)
            bzio.WriteScreen(phone_list[2], 17, 44)

            if ext_one:                             # extension only makes sense if a phone is entered
                bzio.WriteScreen(ext_one, 17, 55)
        else:                                       # if no phone information provided - blanking out the field in case old data is here
            bzio.WriteScreen("   ", 17, 34)
            bzio.WriteScreen("   ", 17, 40)
            bzio.WriteScreen("    ", 17, 44)

        if phone_two:                               # if a phone number is entered
            phone_list = phone_two.split("-")           # seperating phone number in to individual elements for entry
            bzio.WriteScreen(phone_list[0], 18, 34)     # each element is written to the panel
            bzio.WriteScreen(phone_list[1], 18, 40)
            bzio.WriteScreen(phone_list[2], 18, 44)

            if ext_two:                             # extension only makes sense if a phone is entered
                bzio.WriteScreen(ext_one, 18, 55)
        else:                                       # if no phone information provided - blanking out the field in case old data is here
            bzio.WriteScreen("   ", 18, 34)
            bzio.WriteScreen("   ", 18, 40)
            bzio.WriteScreen("    ", 18, 44)

        # writing in the disq and mail options
        bzio.WriteScreen(disq, 14, 77)

        if months_of_disq:                          # if months of disq are indicated - write to the panel.
            bzio.WriteScreen(months_of_disq, 15, 77)

        submition_check = ""
        while submition_check != "ENTER A":
            FuncLib.transmit()                              # once all information is added to the panel - transmit to save
            submition_check = bzio.ReadScreen(7, 24, 2)     # reading to see if panel information has been saved
            empty_panel = bzio.ReadScreen(15, 24, 2)
            if empty_panel == "NAME IS MISSING":
                bzio.WriteScreen("DEL", 20, 71)

        FuncLib.PF3()                                       # command to get to MONY/DISB after a change to AREP for FS Alt Rep
        check_for_DISB = bzio.ReadScreen(4, 2, 51)          # If Alt Rep is changed, MAXIS will open MONY/DISB upon sending through background
        while check_for_DISB != "DISB":                     # looking to get to DISB
            FuncLib.PF3()
            check_for_DISB = bzio.ReadScreen(4, 2, 51)
            SELF_check = bzio.ReadScreen(4, 2, 50)          # Escape from the loop in case MONY/DISB does not come up
            if SELF_check is "SELF":
                break

        # entering the EBT Additional Adult code on MONY DISB and navigating out of the case
        if name.strip() is "":                              # need to strip the name because there are a lot of spaces added
            bzio.WriteScreen("  ", 13, 35)                  # if no name is on ALt Rep - the code should be blanked out
        else:
            bzio.WriteScreen("55", 13, 35)                  # if a name is on Alt Rep - the code is always 55

        check_for_WRAP = ""                                 # after entering the additional adult code, MAXIS goes to STAT/WRAP
        while check_for_WRAP != "WRAP":
            FuncLib.transmit()
            check_for_WRAP = bzio.ReadScreen(4, 2, 46)

        bzio.WriteScreen("AREP", 20, 71)                    # navigating manually back to AREP manually for gather_data
        FuncLib.transmit()

        self.gather_data()                                  # filling all the class properties with the new information

        FuncLib.PF3()                                       # going back to SELF as STAT behaves oddly with MONY/DISB until gone through background
        # entering the EBT Additional Adult code on MONY DISB - because it shows up again
        if name.strip() is "":                              # need to strip the name because there are a lot of spaces added
            bzio.WriteScreen("  ", 13, 35)                  # if no name is on ALt Rep - the code should be blanked out
        else:
            bzio.WriteScreen("55", 13, 35)                  # if a name is on Alt Rep - the code is always 55

        FuncLib.PF3()                                       # going back to self - must do this when changing Alt Rep to ensure MONY/DISB
        FuncLib.PF3()                                       # doesn't mess with future navigation code.


class STAT_BILS_panel:
    """This class references the BILS panel.
    There are NO member or instance parameters for this panel as only one exists for each case.
    Methods in this class: gather_data -- reads the BILS panel and fills class properties
                           create_new -- creates a new panel for the case
                           add_bill -- adds one bill to the BILS panel - panel must exist"""
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    global bill_services
    bill_services = {"01": "Health Professional",
                     "03": "Surgery",
                     "04": "Chiropractic",
                     "05": "Maternity & Reproductive",
                     "07": "Hearing",
                     "08": "Vision",
                     "09": "Hospital",
                     "11": "Hospice",
                     "13": "SNF",
                     "14": "Dental",
                     "15": "Rx Drug/Non-Durable Supply",
                     "16": "Home Health",
                     "17": "Diagnostic",
                     "18": "Mental Health",
                     "19": "Rehabilitation Habilitation",
                     "21": "Durable Medical Equipment/Supplies",
                     "22": "Medical Transportation",
                     "24": "Waivered Services",
                     "25": "Medicare Premium",
                     "26": "Dental or Health Premium",
                     "27": "Remedial Care",
                     "28": "Non-FFP MCRE Service",
                     "30": "Alternative Care",
                     "31": "MCSHN",
                     "32": "Insurance Extension Program",
                     "34": "CW-TCM",
                     "37": "Pay-In Spenddown",
                     "42": "Access Services",
                     "43": "Chemical Dependency",
                     "44": "Nutrition Service",
                     "45": "Organ/tissue Transplant",
                     "46": "Out-of-Area Services",
                     "47": "Copayment/Deductible",
                     "49": "Preventative Care",
                     "99": "Other"}

    global bill_verifications
    bill_verifications = {"01": "Billing Statement",
                          "02": "Explanation of Benefits",
                          "03": "Client Statement - Medical Transport Only",
                          "04": "Credit/Loan Statement",
                          "05": "Provider Statement",
                          "06": "Other",
                          "NO": "No Verification Provided"}

    global all_expense_types
    all_expense_types = {"H": "Health Insurance, Other Premium",
                         "P": "Not Covered, Non-Reimbursed",
                         "M": "Old, Unpaid Medical Bills",
                         "R": "Reimburseable"}

    def gather_data(self):
        """Method will gather all the information from BILS
        Properties generated: self.bills_exist -- boolean to identify if any bills are listed on the panel
                              self.all_bills -- this returns a list of all the bills
                                                each item in the list is a list of all the details of the bill
                                                each individual list is set up as follows:
                                                INDEX -- ELEMENT
                                                0     -- Reference Number of HH Member who incurred expense
                                                1     -- Date of bill
                                                2     -- Service bill is for - SEE DICTIONARY - bill_services
                                                3     -- Gross bill ($ amount before any third party payment)
                                                4     -- Third Party Payments made on bill
                                                5     -- Verification of bill - SEE DICTIONARY - bill_verifications
                                                6     -- Expense Type - SEE DICTIONARY - all_expense_types
                                                7     -- OLD PRI - set the order in which old bills are applied
                                                8     -- Dependent indicator - boolean - True if bill is for a dependedn NOT in the HH
                                                9     -- PAGE of panel the bill is on
                                                10    -- ROW the bill is listed on in panel"""

        # navigate to BILS panel in MAXIS
        at_BILS = bzio.ReadScreen(4, 2, 54)
        if at_BILS != "BILS":
            FuncLib.navigate_to_MAXIS_screen(self.case, self.month, self.year, "STAT", "BILS")

        while bzio.ReadScreen(10, 24, 14) != "FIRST PAGE":      # ensuring we are starting from page 1
            FuncLib.PF19()

        if bzio.ReadScreen(2, 6, 26) != "__":   # checking to be sure that a bill exists on the panel
            self.bills_exist = True             # sets the variable to if a bill exists
        else:
            self.bills_exist = False

        self.all_bills = []                     # defining the property as a list
        row = 6                                 # setting the start of variables
        page = 1

        # this will loop until all the bills are read on each page of the BILS panel
        # each bill entry will be added to a list as a list of all the details
        next_bill = bzio.ReadScreen(2, row, 26)
        while next_bill != "__":

            # reading each line of the BILS panel
            ref_nbr = bzio.ReadScreen(2, row, 26)
            bill_date = "%s/%s/%s" % (bzio.ReadScreen(2, row, 30), bzio.ReadScreen(2, row, 33), bzio.ReadScreen(2, row, 36))    # format as a date
            serv_code = bzio.ReadScreen(2, row, 40)
            grs_amt = float(bzio.ReadScreen(9, row, 45).strip())        # formating as a number for maths
            pymts = bzio.ReadScreen(9, row, 57).strip()                 # reading the third payments field and trimming
            if pymts == "_________":                                    # this may be blank - handling for reading blank as 0
                pymts = 0.0
            else:
                pymts = float(pymts)                                    # if not blank - converiting to a number for maths
            ver_code = bzio.ReadScreen(2, row, 67)
            exp_typ = bzio.ReadScreen(1, row, 71)
            old_pri = bzio.ReadScreen(2, row, 75).replace("_", "")      # this may be blank - taking out the underlines if so
            dpd_ind = bzio.ReadScreen(1, row, 79)                       # reading the code then redefining as a boolean
            if dpd_ind == "Y":
                dpd_ind = True
            else:
                dpd_ind = False

            # all of the found information will be added to the list
            self.all_bills.append([ref_nbr,                         # INDEX - 0 -- Refernce number of the HH Member who incurred the bill
                                   bill_date,                       # INDEX - 1 -- date of service of the bill
                                   bill_services[serv_code],        # INDEX - 2 -- type of service of the bill - detail is filled from dictionary bill_servies
                                   grs_amt,                         # INDEX - 3 -- Gross amount of bill - as a float
                                   pymts,                           # INDEX - 4 -- amount of any third party payments on bill - as a float
                                   bill_verifications[ver_code],    # INDEX - 5 -- verification -   detail from dictionary bill_verifications
                                   all_expense_types[exp_typ],      # INDEX - 6 -- Type of Expense - detail from dictionary all_expense_types
                                   old_pri,                         # INDEX - 7 -- Change priority - may be blank
                                   dpd_ind,                         # INDEX - 8 -- Boolean of if bill is for a dependent not in HH
                                   page,                            # INDEX - 9 -- page that the bill can be found in the panel
                                   row])                            # INDEX - 10 -- row that the bill can be found on the panel

            row += 1               # advancing the row
            if row == 18:          # this is the end of the page
                FuncLib.PF20()  # goes to the next page
                if bzio.ReadScreen(9, 24, 14) == "LAST PAGE":       # if there are no more pages, the loop will stop
                    break
                page += 1       # if we went to a next page, then increasing the page number and resets the row number
                row = 6

            next_bill = bzio.ReadScreen(2, row, 26)                 # reads the next ref_nbr to see if we should loop again

    def add_bill(self, ref_number, date_of_bill, service, gross_amt, payment_amt, verif, expense_type, old_priority=None, depdnt_indc=False):
        """Method to add bill to BILS panel.
        If no panel exists, one will be created.
        Argument requirements: ref_number -- reference number of HH member who incurred the bill
                               date_of_bill -- date of medical service
                               service -- type of medical service - use code from dictionary bill_services
                               gross_amt -- ross amount of the original bill
                               payment_amt -- amount to already paid by third party
                               verif -- verification of bill, use codes from dictionary bill_verifications
                               expense type -- type of bill - use codes from dictionary all_expense_types
                               old_priority -- use this to reset priority - default to None
                               depdnt_indc -- boolean for if bill is for a dependent who is not in the household - default to False"""

        # navigate to BILS panel in MAXIS
        at_BILS = bzio.ReadScreen(4, 2, 54)
        if at_BILS != "BILS":
            FuncLib.navigate_to_MAXIS_screen(self.case, self.month, self.year, "STAT", "BILS")

        while bzio.ReadScreen(10, 24, 14) != "FIRST PAGE":      # ensuring we are starting from page 1
            FuncLib.PF19()

        # putting the panel in edit mode
        if bzio.ReadScreen(1, 2, 73) == "0":    # if no panel exists - create a new one
            bzio.WriteScreen("NN", 20, 79)
            FuncLib.transmit()
        else:                                   # if a panel does exists - put in edit mode
            FuncLib.PF9()

        # a bill can be entered to last line on the page and MAXIS will rearage according to the sort (defaulted to DATE)
        # reading the last line to make sure it is blank
        while bzio.ReadScreen(2, 17, 26) != "__":
            FuncLib.PF20()

        # now all the arguments will be written to the blank line
        bzio.WriteScreen(ref_number, 17, 26)                # writing the reference number
        FuncLib.write_mainframe_date(date_of_bill, "XX XX XX", [17, 30], [17, 33], [17, 36])    # writing the date in the each space
        bzio.WriteScreen(service, 17, 40)                   # writing the service code
        bzio.WriteScreen(gross_amt, 17, 45)                 # write the gross amount of bill
        if payment_amt == 0:                                # resetting this to a blank if set to 0 because BILS doesn't like 0
            payment_amt = ""
        bzio.WriteScreen(payment_amt, 17, 57)               # writing any payment amount
        bzio.WriteScreen(verif, 17, 67)                     # writing in the verification code
        bzio.WriteScreen(expense_type, 17, 71)              # writing in the expense type code
        if old_priority:                                    # if this exists - writing in old priority
            bzio.WriteScreen(old_priority, 17, 75)
        if depdnt_indc:                                     # if dependent indicator is tru, a Y code will be entered
            bzio.WriteScreen("Y", 17, 79)

        FuncLib.transmit()          # transmit once to take the panel out of edit mode
        FuncLib.transmit()          # second transmit resolves the sort for all the bills

        self.gather_data()          # now all of the data will be gathered and stored in class properties


class STAT_BUDG_panel:
    """Class references STAT/BUDG panel.
    NO instance or member parameter required as only one panel per case.
    Methods in this class: gather_data -- get all information from the panel and save to class properties
                           change_budget -- will update the budget period"""
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    global budget_src_codes
    budget_src_codes = {"M": "MAXIS",
                        "W": "Worker",
                        "C": "Converted"}

    def gather_data(self):
        """This method will pull data from STAT/BUDG
        Properties generated: self.hc_app_date -- date of hc application - format mm/dd/yy
                              self.current_budg_start -- Month and year of current budget period start month - format MM/YY
                              self.current_budg_end -- Month and year of current budget period last month - format MM/YY
                              self.current_budg_src -- source of budget generation
                              self.past_budgets -- list of all past budgets"""

        # navigate to BUDG panel in MAXIS
        at_BILS = bzio.ReadScreen(4, 2, 52)
        if at_BILS != "BUDG":
            FuncLib.navigate_to_MAXIS_screen(self.case, self.month, self.year, "STAT", "BUDG")

        # reading information from the panel and assigning to Properties
        # also formatting dates
        self.hc_app_date = "%s/%s/%s" % (bzio.ReadScreen(2, 4, 64), bzio.ReadScreen(2, 4, 67), bzio.ReadScreen(2, 4, 70))
        self.current_budg_start = "%s/%s" % (bzio.ReadScreen(2, 10, 35), bzio.ReadScreen(2, 10, 38))
        self.current_budg_end = "%s/%s" % (bzio.ReadScreen(2, 10, 46), bzio.ReadScreen(2, 10, 49))
        source = bzio.ReadScreen(1, 10, 58)
        self.current_budg_src = budget_src_codes[source]                # filling detail about source from dictionary

        self.past_budgets = []          # setting this property as a list
        row = 11                        # setting the row

        # setting the variable for a loop
        next_budget = bzio.ReadScreen(2, row, 35)       # next will loop to get each line of past budget period details
        while next_budget != "  ":
            begin_dt = "%s/%s" % (bzio.ReadScreen(2, row, 35), bzio.ReadScreen(2, row, 38))     # reading the begin date and formatting
            end_dt = "%s/%s" % (bzio.ReadScreen(2, row, 46), bzio.ReadScreen(2, row, 49))       # readint the end date and formatting
            source = bzio.ReadScreen(1, row, 58)

            self.past_budgets.append([begin_dt,                  # INDEX - 0 -- begining of budg pd - format MM/YY
                                     end_dt,                    # INDEX - 1 -- ending of budg pd - format MM/YY
                                     budget_src_codes[source],  # INDEX - 2 -- detail about source of the budget
                                     row])                       # INDEX - 3 -- saving the row of this budget

            row += 1            # incrementing the row for the next line
            next_budget = bzio.ReadScreen(2, row, 35)

    def change_budget(self, budget_begin_month):
        """This method will update the 'Override Budget Period'
        Only the begin month in format MM/YY - method will determine the end month
        THIS METHOD WILL SEND THE CASE THROUGH BACKGROUND"""

        # navigate to BUDG panel in MAXIS
        at_BILS = bzio.ReadScreen(4, 2, 52)
        if at_BILS != "BUDG":
            FuncLib.navigate_to_MAXIS_screen(self.case, self.month, self.year, "STAT", "BUDG")

        # setting the panel to edit mode
        FuncLib.PF9()

        # spliting the month and year for entry to the panel
        begin_month = budget_begin_month[:2]
        begin_year = budget_begin_month[3:]

        month_number = int(begin_month)         # changing the month to an integer for maths
        year_number = int(begin_year)
        last_month_number = month_number + 5    # last month is five months after the first
        if last_month_number > 12:              # there are only 12 months
            last_month_number -= 12             # this will go to the next year
            year_number += 1

        end_month = str(last_month_number)      # setting these as strings
        if len(end_month) is 1:                 # adding the leading 0 to the month if needed
            end_month = "0" + end_month
        end_year = str(year_number)

        # writing the new budget to the panel
        bzio.WriteScreen(begin_month, 5, 64)
        bzio.WriteScreen(begin_year, 5, 67)
        bzio.WriteScreen(end_month, 5, 72)
        bzio.WriteScreen(end_year, 5, 75)

        FuncLib.transmit()      # saving the information to the panel
        FuncLib.PF3()           # exiting STAT
        FuncLib.PF3()

        self.gather_data()


class STAT_BUSI_panel:
    """Class references STAT/BUSI panel.
    This panel requires MEMBER and INSTANCE parameters
    Methods in this class: gather_data -- reading the panel and assigning information to class properties
                           create_new -- create a new BUSI panel
                           update_amount -- update the income information for one program"""
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year
        self.member = member
        self.instance = instance

    global busi_income_types
    busi_income_types = {"01": "Farming",
                         "02": "Real Estate",
                         "03": "Home Product Sales",
                         "04": "Other Sales",
                         "05": "Personal Services",
                         "06": "Paper Route",
                         "07": "In Home Daycare",
                         "08": "Rental Income",
                         "09": "Other"}

    global busi_verifications
    busi_verifications = {"1": "Income Tax Returns",
                          "2": "Receipts of Sales/Purchases",
                          "3": "Client Business Records/Ledger",
                          "4": "Pending Out State Verification",
                          "6": "Other Document",
                          "N": "No Verification Provided",
                          "_": "Blank"}

    def gather_data(self):
        """Method to read panel and generate class properties.
        Properties created: business_type -- detail of income type code (string)
                            income_start -- date of income start (mm/dd/yy format)
                            income_end -- date of income end (mm/dd/yy format) - may be None if not filled
                            for cash and snap
                            _retro_net -- amount from main panel for retro net amount (float)
                            _prosp_net -- amount from main panel for prospective net amount (float)
                            _retro_gross -- amount from income calctulation pop-up (float)
                            _prosp_gross -- amount from income calctulation pop-up (float)
                            _retro_exp -- counted expense amount from income calctulation pop-up (float)
                            _prosp_exp -- counted expense amount from income calctulation pop-up (float)
                            _inc_verif -- full detail of the income verification (string)
                            _exp_verif -- full detail of the expense verification (string)

                            for ive, hc_methA, and hc_methB  (these do not have retro information)
                            _net -- amount from main panel for net amount (float)
                            _gross -- amount from income calculation pop-up (float)
                            _expense -- counted expense amount from income calculation pop-up (float)
                            _inc_verif -- full detail of the income verification (string)
                            _exp_verif -- full detail of the expense verification (string)

                            retro_rept_hrs -- reported hours for the retro month
                            prosp_rept_hrs -- reported hours for the prospective month
                            min_wage_hrs_retro -- calculated minimum wage hours for the retro month
                            min_wage_hrs_prosp -- calculated minimum wage hours for the prosp month
                            self_emp_method -- full detail of the self employment method chosen (string)
                            method_date -- date self employment method was chosen (mm/dd/yy format)

                            inc_est_A_total -- amount from income estimate pop up - Method A total
                            inc_est_B_total -- amount from income estimate pop up - Method B total
                            inc_est_A_exp -- amount of expenses from income estimate pop up - Method A total
                            inc_est_B_exp -- amount of expenses from income estimate pop up - Method B total
                            inc_est_A_gross -- sum amount from income estimate pop up - Method A total
                            inc_est_B_gross -- sum amount from income estimate pop up - Method B total
                            """

        # navigate to BUSI panel in MAXIS
        at_BILS = bzio.ReadScreen(4, 2, 51)
        if at_BILS != "BUSI":
            FuncLib.navigate_to_MAXIS_screen(self.case, self.month, self.year, "STAT", "BUSI")
        bzio.WriteScreen(self.member, 20, 76)           # navigating to the correct member and instance of the panel
        bzio.WriteScreen(self.instance, 20, 79)
        FuncLib.transmit()

        # TODO create and insert method to verify BUSI panel exists before trying to read

        # reading all infromation from panel
        income_type_code = bzio.ReadScreen(2, 5, 37)                    # income code - for key value for dictionary
        self.business_type = busi_income_types[income_type_code]        # assigning property with full detail from dictionary busi_income_types
        self.income_start = "%s/%s/%s" % (bzio.ReadScreen(2, 5, 55), bzio.ReadScreen(2, 5, 58), bzio.ReadScreen(2, 5, 61))  # reading and formating start date
        self.income_end = "%s/%s/%s" % (bzio.ReadScreen(2, 5, 72), bzio.ReadScreen(2, 5, 75), bzio.ReadScreen(2, 5, 78))    # reading and formating end end date
        if self.income_end == "__/__/__":
            self.income_end = None

        # reads each number from the panel and converts it to a float for maths
        self.cash_retro_net = FuncLib.read_float_from_BZ(8, 8, 55)     # CASH retro NET - from main panel
        self.cash_prosp_net = FuncLib.read_float_from_BZ(8, 8, 69)     # CASH prosp NET - from main panel

        self.snap_retro_net = FuncLib.read_float_from_BZ(8, 10, 55)     # SNAP retro NET - from main panel
        self.snap_prosp_net = FuncLib.read_float_from_BZ(8, 10, 69)     # SNAP prosp NET - from main panel

        self.ive_prosp_net = FuncLib.read_float_from_BZ(8, 9, 69)     # IV-E prosp NET - from main panel

        self.hc_methA_prosp_net = FuncLib.read_float_from_BZ(8, 11, 69)     # HC Method A prosp NET - from main panel

        self.hc_methB_prosp_net = FuncLib.read_float_from_BZ(8, 12, 69)     # HC Method B prosp NET - from main panel

        # reading the hours from the main page
        self.retro_rept_hrs = FuncLib.read_float_from_BZ(3, 13, 60)        # retro reported hours
        self.prosp_rept_hrs = FuncLib.read_float_from_BZ(3, 13, 74)        # prospective reported horus
        self.min_wage_hrs_retro = FuncLib.read_float_from_BZ(3, 14, 69)    # retro minimum wage hours
        self.min_wage_hrs_prosp = FuncLib.read_float_from_BZ(3, 14, 74)    # prospective minimum wage hours

        # reading information about the self employment method
        self_emp_code = bzio.ReadScreen(2, 16, 53)              # reads the code from the panel
        if self_emp_code == "01":                               # assigns the detail of the code
            self.self_emp_method = "50'%' Gross Income"
        elif self_emp_code == "02":
            self.self_emp_method = "Tax Forms"
        else:
            self.self_emp_method = None
        self.method_date = "%s/%s/%s" % (bzio.ReadScreen(2, 16, 63), bzio.ReadScreen(2, 16, 66), bzio.ReadScreen(2, 16, 69))

        # selects the Gross Income Calculation Pop-up and opens it
        bzio.WriteScreen("X", 6, 26)
        FuncLib.transmit()

        # reading all the infromation from the pop up and assigning to properties
        self.cash_retro_gross = FuncLib.read_float_from_BZ(8, 9, 43)               # CASH prog information - formatted by function to make FLOAT
        self.cash_prosp_gross = FuncLib.read_float_from_BZ(8, 9, 59)
        self.cash_inc_verif = busi_verifications[bzio.ReadScreen(1, 9, 73)]     # assigning full deatil from PF1 menu instead of just the code
        self.cash_retro_exp = FuncLib.read_float_from_BZ(8, 15, 43)
        self.cash_prosp_exp = FuncLib.read_float_from_BZ(8, 15, 59)
        self.cash_exp_verif = busi_verifications[bzio.ReadScreen(1, 15, 73)]    # assigning full deatil from PF1 menu instead of just the code

        self.snap_retro_gross = FuncLib.read_float_from_BZ(8, 11, 43)              # SNAP prog information - formatted by function to make FLOAT
        self.snap_prosp_gross = FuncLib.read_float_from_BZ(8, 11, 59)
        self.snap_inc_verif = busi_verifications[bzio.ReadScreen(1, 11, 73)]    # assigning full deatil from PF1 menu instead of just the code
        self.snap_retro_exp = FuncLib.read_float_from_BZ(8, 17, 43)
        self.snap_prosp_exp = FuncLib.read_float_from_BZ(8, 17, 59)
        self.snap_exp_verif = busi_verifications[bzio.ReadScreen(1, 17, 73)]    # assigning full deatil from PF1 menu instead of just the code

        self.ive_prosp_gross = FuncLib.read_float_from_BZ(8, 10, 59)               # IV-E prog information - formatted by function to make FLOAT
        self.ive_inc_verif = busi_verifications[bzio.ReadScreen(1, 10, 73)]     # assigning full deatil from PF1 menu instead of just the code
        self.ive_prosp_exp = FuncLib.read_float_from_BZ(8, 16, 59)
        self.ive_exp_verif = busi_verifications[bzio.ReadScreen(1, 16, 73)]     # assigning full deatil from PF1 menu instead of just the code

        self.hc_methA_prosp_gross = FuncLib.read_float_from_BZ(8, 12, 59)               # HC Method A prog information - formatted by function to make FLOAT
        self.hc_methA_inc_verif = busi_verifications[bzio.ReadScreen(1, 12, 73)]     # assigning full deatil from PF1 menu instead of just the code
        self.hc_methA_prosp_exp = FuncLib.read_float_from_BZ(8, 18, 59)
        self.hc_methA_exp_verif = busi_verifications[bzio.ReadScreen(1, 18, 73)]     # assigning full deatil from PF1 menu instead of just the code

        self.hc_methB_prosp_gross = FuncLib.read_float_from_BZ(8, 13, 59)               # HC Method B prog information - formatted by function to make FLOAT
        self.hc_methB_inc_verif = busi_verifications[bzio.ReadScreen(1, 13, 73)]     # assigning full deatil from PF1 menu instead of just the code
        self.hc_methB_prosp_exp = FuncLib.read_float_from_BZ(8, 19, 59)
        self.hc_methB_exp_verif = busi_verifications[bzio.ReadScreen(1, 19, 73)]     # assigning full deatil from PF1 menu instead of just the code

        FuncLib.PF3()           # exiting the pop-up to go back to the main panel

        # Opening the HC Income Estimate Pop-Up
        bzio.WriteScreen("X", 17, 27)
        FuncLib.transmit()

        # reading all values from the pop-up and assigning to class properties
        self.inc_est_A_total = FuncLib.read_float_from_BZ(8, 7, 54)
        self.inc_est_B_total = FuncLib.read_float_from_BZ(8, 8, 54)
        self.inc_est_A_exp = FuncLib.read_float_from_BZ(8, 11, 54)
        self.inc_est_B_exp = FuncLib.read_float_from_BZ(8, 12, 54)
        self.inc_est_A_gross = FuncLib.read_float_from_BZ(8, 15, 54)
        self.inc_est_B_gross = FuncLib.read_float_from_BZ(8, 16, 54)
        self.inc_est_hrs = FuncLib.read_float_from_BZ(3, 18, 58)

        FuncLib.PF3()       # closing the pop-up window

    def create_new(self, start_date, income_type, program, prosp_gross, income_verif,
                   prosp_expense, expense_verif, prosp_hours, method, date_selection,
                   retro_gross=None, retro_expense=None, retro_hours=None):
        """Method will create a new BUSI panel and enter income detail for 1 program
        Argument requirements: start_date -- Start date of income
                               income_type -- code for type of self employment income
                               program -- which program is income information provided for (cash, iv-e, snap, hcA, hcB)
                               prosp_gross -- amount of total gross income for prospective
                               income_verif -- verif code for the income amount
                               prosp_expense -- amount of expenses to count for prospective
                               expense_verif -- verif code for the expense amount
                               prosp_hours -- reported prospective hours
                               method -- self employment budget method code (01 or 02)
                               date_selection -- the date that the self employment method was selected
                    Optional arguments:
                               retro_gross -- amount of total gross income
                               retro_expense -- amount of retro counted expenses
                               retro_hours -- reported retro hours"""
        # navigate to BUSI panel in MAXIS
        at_BILS = bzio.ReadScreen(4, 2, 51)
        if at_BILS != "BUSI":
            FuncLib.navigate_to_MAXIS_screen(self.case, self.month, self.year, "STAT", "BUSI")
        bzio.WriteScreen(self.member, 20, 76)           # navigating to the correct member and instance of the panel
        bzio.WriteScreen("NN", 20, 79)
        FuncLib.transmit()

        instance = bzio.ReadScreen(2, 2, 72).strip()    # assigning the instance to class variable
        if len(instance) == 1:
            instance = "0" + instance
        self.instance = instance

        # writing the information to the panel
        bzio.WriteScreen(income_type, 5, 37)                                                # income type code
        FuncLib.write_mainframe_date(start_date, "XX XX XX", [5, 55], [5, 58], [5, 61])     # start date of income
        bzio.WriteScreen(prosp_hours, 13, 74)                                               # prospective hours
        if retro_hours:                                                                     # retro hours if provided
            bzio.WriteScreen(retro_hours, 13, 60)
        bzio.WriteScreen(method, 16, 53)                                                    # self employment method and date
        FuncLib.write_mainframe_date(date_selection, "XX XX XX", [16, 63], [16, 66], [16, 69])

        program = program.upper()           # converting the program variable to upper case for comparing
        bzio.MsgBox(program)
        if program == "CASH":               # defining the row to write information to based on the program provided
            inc_row = 9
            exp_row = 15
        elif program is "IV-E":
            inc_row = 10
            exp_row = 16
        elif program is "SNAP":
            inc_row = 11
            exp_row = 17
        elif program is "HCA":
            inc_row = 12
            exp_row = 18
        elif program is "HCB":
            inc_row = 13
            exp_row = 19

        # selects the Gross Income Calculation Pop-up and opens it
        bzio.WriteScreen("X", 6, 26)
        FuncLib.transmit()

        bzio.WriteScreen(prosp_gross, inc_row, 59)          # wrting the gross amount to the pop-up panel
        bzio.WriteScreen(income_verif, inc_row, 73)         # writing the verif
        if retro_gross:                                     # if a retro amount was provided - writing it in
            bzio.WriteScreen(retro_gross, inc_row, 43)

        bzio.WriteScreen(prosp_expense, exp_row, 59)        # writing the expense amount to the pop-up panel
        bzio.WriteScreen(expense_verif, exp_row, 73)        # writing the verif
        if retro_expense:                                   # if a retro expense was provdied - writing it in
            bzio.WriteScreen(retro_expense, exp_row, 43)

        FuncLib.PF3()           # going back to the main panel.

        FuncLib.transmit()      # submitting the panel and taking out of edit mode

        self.gather_data()      # filling all class properties

    def update_amount(self, program, prosp_gross, income_verif,
                   prosp_expense, expense_verif, prosp_hours=None,
                   retro_gross=None, retro_expense=None, retro_hours=None):
        """Method will update the gross amount, expense, verification, reported hours for one program
        Argument requirements: program -- which program is income information provided for (cash, iv-e, snap, hcA, hcB)
                               prosp_gross -- amount of total gross income for prospective
                               income_verif -- verif code for the income amount
                               prosp_expense -- amount of expenses to count for prospective
                               expense_verif -- verif code for the expense amount
                    Optional arguments:
                               prosp_hours -- reported prospective hours
                               retro_gross -- amount of total gross income
                               retro_expense -- amount of retro counted expenses
                               retro_hours -- reported retro hours"""

        # navigate to BUSI panel in MAXIS
        at_BUSI = bzio.ReadScreen(4, 2, 51)
        if at_BUSI != "BUSI":
            FuncLib.navigate_to_MAXIS_screen(self.case, self.month, self.year, "STAT", "BUSI")
        bzio.WriteScreen(self.member, 20, 76)           # navigating to the correct member and instance of the panel
        bzio.WriteScreen(self.instance, 20, 79)
        FuncLib.transmit()

        FuncLib.PF9()       # putting panel in edit mode

        # TODO create and insert method to verify BUSI panel is in edit mode

        if prosp_hours:                                 # prospective hours if provided
            prosp_hours = str(prosp_hours)          # adding spaces to the end of the information to be sure to overwrite old data
            spaces_to_add = 3 - len(prosp_hours)
            prosp_hours = prosp_hours + (" " * spaces_to_add)
            bzio.WriteScreen(prosp_hours, 13, 74)
        if retro_hours:                                 # retro hours if provided
            retro_hours = str(retro_hours)          # adding spaces to the end of the information to be sure to overwrite old data
            spaces_to_add = 3 - len(retro_hours)
            retro_hours = retro_hours + (" " * spaces_to_add)
            bzio.WriteScreen(retro_hours, 13, 60)

        program = program.upper()           # converting the program variable to upper case for comparing
        if program is "CASH":               # defining the row to write information to based on the program provided
            inc_row = 9
            exp_row = 15
        elif program is "IV-E":
            inc_row = 10
            exp_row = 16
        elif program is "SNAP":
            inc_row = 11
            exp_row = 17
        elif program is "HCA":
            inc_row = 12
            exp_row = 18
        elif program is "HCB":
            inc_row = 13
            exp_row = 19

        # selects the Gross Income Calculation Pop-up and opens it
        bzio.WriteScreen("X", 6, 26)
        FuncLib.transmit()

        prosp_gross = str(prosp_gross)          # adding spaces to the end of the information to be sure to overwrite old data
        spaces_to_add = 8 - len(prosp_gross)
        prosp_gross = prosp_gross + (" " * spaces_to_add)

        bzio.WriteScreen(prosp_gross, inc_row, 59)          # wrting the gross amount to the pop-up panel
        bzio.WriteScreen(income_verif, inc_row, 73)         # writing the verif
        if retro_gross:                                     # if a retro amount was provided - writing it in
            retro_gross = str(retro_gross)          # adding spaces to the end of the information to be sure to overwrite old data
            spaces_to_add = 8 - len(retro_gross)
            retro_gross = retro_gross + (" " * spaces_to_add)

            bzio.WriteScreen(retro_gross, inc_row, 43)

        prosp_expense = str(prosp_expense)          # adding spaces to the end of the information to be sure to overwrite old data
        spaces_to_add = 8 - len(prosp_expense)
        prosp_expense = prosp_expense + (" " * spaces_to_add)

        bzio.WriteScreen(prosp_expense, exp_row, 59)        # writing the expense amount to the pop-up panel
        bzio.WriteScreen(expense_verif, exp_row, 73)        # writing the verif
        if retro_expense:                                   # if a retro expense was provdied - writing it in
            retro_expense = str(retro_expense)          # adding spaces to the end of the information to be sure to overwrite old data
            spaces_to_add = 8 - len(retro_expense)
            retro_expense = retro_expense + (" " * spaces_to_add)

            bzio.WriteScreen(retro_expense, exp_row, 43)

        FuncLib.PF3()           # going back to the main panel.

        FuncLib.transmit()      # submitting the panel and taking out of edit mode

        self.gather_data()      # filling all class properties


class STAT_CARS_panel:
    """Class refernces the STAT/CARS panel.
    This class requires MEMBER and INSTANCE parameters.
    Methods in this class: gather_data -- collect all information from an existing panel and generate all class properties
                           create_new -- create a new CARS panel
                           update_value -- change the value of a vehicle
                           update_verif -- change or add a verification type
                           update_amount_owed -- change or add an amount owed"""
    def __init__(self, case_number, footer_month, footer_year, member, instance):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year
        self.member = member
        self.instance = instance

    global vehicle_types
    vehicle_types = {"1": "Car",
                     "2": "Truck",
                     "3": "Van",
                     "4": "Camper",
                     "5": "Motorcycle",
                     "6": "Trailer",
                     "7": "Other"}

    global value_sources
    value_sources = {"1": "NADA",
                     "2": "Appraisal Val",
                     "3": "Client Stmt",
                     "4": "Other Document"}

    global ownership_verifications
    ownership_verifications = {"1": "Title",
                               "2": "License Registration",
                               "3": "DMV",
                               "4": "Purchase Agreement",
                               "5": "Other Document",
                               "N": "No Verification Provided",
                               "_": "Blank"}

    global loan_bal_verifications
    loan_bal_verifications = {"1": "Bank/Lending Institution Statement",
                              "2": "Private Lender Statement",
                              "3": "Other Document",
                              "4": "Pending Out of State Verification",
                              "N": "No Verification Provided",
                              "_": "Blank"}

    global vehicle_uses
    vehicle_uses = {"1": "Primary Vehicle",
                    "2": "Employment/Training Transportation/Search",
                    "3": "Disabled Transport",
                    "4": "Income Producing",
                    "5": "Used as Home",
                    "7": "Unlicensed",
                    "8": "Other Countable",
                    "9": "Unavailable",
                    "0": "Long Distance Employment Travel",
                    "A": "Carry Heating Fuel or Water"}

    def gather_data(self):
        """Method to read panel and generate class properties
        Properties generated: type -- kind of vehicle panel is for - full string from dictionary
                              year -- year of vehicle - string
                              make -- make of vehicle - string
                              model -- Model of vehicle
                              trade_in_value -- Trade-In value of vehicle - float
                              loan_value -- Loan Value of vehicle - float
                              value_source -- source of value identity - full string from dictionary
                              ownership_verif -- verification detail - full string from dictionary
                              amount_owed -- value that is still owed on vehicle - float
                              verif_owed -- verification of the amount still owed - full string from dictionary
                              owed_date -- date the amount owed was established - string
                              use -- details of vehicle use - full string from dictionary
                              hc_clt_benefit -- if vehicle is for MA client - boolean
                              joint_owner -- if vehicle is jointly owned - boolean
                              share_ratio -- the ratio that the vehicle is shared at - string"""
        # navigate to CARS panel in MAXIS
        at_CARS = bzio.ReadScreen(4, 2, 44)
        if at_CARS != "CARS":
            FuncLib.navigate_to_MAXIS_screen(self.case, self.month, self.year, "STAT", "CARS")
        bzio.WriteScreen(self.member, 20, 76)           # navigating to the correct member and instance of the panel
        bzio.WriteScreen(self.instance, 20, 79)
        FuncLib.transmit()

        # TODO create and insert method to verify CARS panel exists before trying to read

        self.type = vehicle_types[bzio.ReadScreen(1, 6, 43)]        # readung the type code and filling property with detail from dictionary vehicle_types
        self.year = bzio.ReadScreen(4, 8, 31)                       # reading the year and blanking out if the field is empty
        self.year = self.year.replace("_", "")
        self.make = bzio.ReadScreen(15, 8, 43)                      # reading the make, then formatting the property
        self.make = self.make.strip()
        self.make = self.make.replace("_", "")
        self.model = bzio.ReadScreen(15, 8, 66)                     # reading the model, then formatting the property
        self.model = self.model.strip()
        self.model = self.model.replace("_", "")
        self.trade_in_value = FuncLib.read_float_from_BZ(8, 9, 45)  # reading trade in value as a float
        self.loan_value = FuncLib.read_float_from_BZ(8, 9, 62)      # reading the load value as a float
        self.value_source = value_sources[bzio.ReadScreen(1, 9, 80)]                # reading source code and filling detail from value_sources dictionary
        self.ownership_verif = ownership_verifications[bzio.ReadScreen(1, 10, 60)]  # reading ownership verif and filling detail from dictionary
        self.amount_owed = FuncLib.read_float_from_BZ(8, 12, 45)                    # reading amount owed as a float
        self.verif_owed = loan_bal_verifications[bzio.ReadScreen(1, 12, 60)]        # reading owed amnount verif and filling detail from dictionary
        # reading received date and formatting it as mm/dd/yy
        self.owed_date = "%s/%s/%s" % (bzio.ReadScreen(2, 13, 43), bzio.ReadScreen(2, 13, 46), bzio.ReadScreen(2, 13, 49))
        self.use = vehicle_uses[bzio.ReadScreen(1, 15, 43)]         # readung use code and filling detail from vehicle_used dictionary

        if bzio.ReadScreen(1, 15, 76) == "Y":       # reading HC Clt Benefit and saving as boolean
            self.hc_clt_benefit = True
        else:
            self.hc_clt_benefit = False

        if bzio.ReadScreen(1, 16, 43) == "Y":       # reading joint owner code and formatting as boolean
            self.joint_owner = True
        else:
            self.joint_owner = False

        # reading the share ratio and formatting it as x/y
        self.share_ratio = "%s/%s" % (bzio.ReadScreen(1, 16, 76), bzio.ReadScreen(1, 16, 80))

    def create_new(self, type, year, make, model, trade_in, value_source, use, HC_client, owner_verif="N", share_ratio="1/1"):
        """Method to create a new CARS panel.
        Argument requirements: type -- type code - options - 1, 2, 3, 4, 5, 6, 7
                               year -- vehicle year
                               make -- vehicle make
                               model -- vehicle model
                               trade_in -- trade-in value - as a float
                               value_source -- source code - options - 1, 2, 3, 4
                               use -- use code - options - 1, 2, 3, 4, 5, 7, 8, 9, 0, A
                               HC_client -- Y or N
                               owner_verif -- ownership verificatio - default to 'N' - options - 1, 2, 3, 4, 5, N
                               share_ratio -- ratio of 1/1 defaulted - can be changed - should be in x/y format - joint owner determined by this"""
        # navigate to CARS panel in MAXIS
        at_CARS = bzio.ReadScreen(4, 2, 44)
        if at_CARS != "CARS":
            FuncLib.navigate_to_MAXIS_screen(self.case, self.month, self.year, "STAT", "CARS")
        bzio.WriteScreen(self.member, 20, 76)           # navigating to the correct member and instance of the panel
        bzio.WriteScreen("NN", 20, 79)
        FuncLib.transmit()

        instance = bzio.ReadScreen(2, 2, 72).strip()    # assigning the instance to class variable
        if len(instance) == 1:
            instance = "0" + instance
        self.instance = instance

        bzio.WriteScreen(type, 6, 43)           # writing type code to the new panel
        bzio.WriteScreen(year, 8, 31)           # writing the year, make, model to the panel
        bzio.WriteScreen(make, 8, 43)
        bzio.WriteScreen(model, 8, 66)
        bzio.WriteScreen(trade_in, 9, 45)       # writing the trade-in value
        loan_val = trade_in * .9                # calculating the loan value from trade in value
        loan_val = (25.0 * round(loan_val / 25.0))  # formatting the number to be a multiple of 25
        bzio.WriteScreen(loan_val, 9, 62)       # writing in the loan value
        bzio.WriteScreen(value_source, 9, 80)   # writing in the value source
        bzio.WriteScreen(use, 15, 43)           # writing in the use code
        bzio.WriteScreen(HC_client, 15, 76)     # writing in the HC Client Y/N code
        bzio.WriteScreen(owner_verif, 10, 60)   # writing in the verif of ownership
        if share_ratio == "1/1":                # writing the share ratio and joint owner code
            bzio.WriteScreen("N", 16, 43)       # joint owner code is determined by the share ratio provided
            bzio.WriteScreen("1", 16, 76)
            bzio.WriteScreen("1", 16, 80)
        else:
            bzio.WriteScreen("Y", 16, 43)
            bzio.WriteScreen(share_ratio[0], 16, 76)
            bzio.WriteScreen(share_ratio[2], 16, 80)

        self.gather_data()      # filling all the class properties

    def update_value(self, trade_in, value_source):
        """Method to update only the trade-in and loan value and source code
        Argument requirements: trade_in -- trade-in value - as a float
                               value_source -- source code - options - 1, 2, 3, 4 """
        # navigate to CARS panel in MAXIS
        at_CARS = bzio.ReadScreen(4, 2, 44)
        if at_CARS != "CARS":
            FuncLib.navigate_to_MAXIS_screen(self.case, self.month, self.year, "STAT", "CARS")
        bzio.WriteScreen(self.member, 20, 76)           # navigating to the correct member and instance of the panel
        bzio.WriteScreen(self.instance, 20, 79)
        FuncLib.transmit()

        FuncLib.PF9()       # puts panel in edit mode

        # TODO create and insert method to verify CARS panel is in edit mode

        bzio.WriteScreen("        ", 9, 45)     # blanking out previous entry
        bzio.WriteScreen("        ", 9, 62)
        bzio.WriteScreen(trade_in, 9, 45)       # writing the trade-in value
        loan_val = trade_in * .9                # calculating the loan value from trade in value
        loan_val = (25.0 * round(loan_val / 25.0))  # formatting the number to be a multiple of 25
        bzio.WriteScreen(loan_val, 9, 62)       # writing in the loan value
        bzio.WriteScreen(value_source, 9, 80)   # writing in the value source

        self.gather_data()      # filling all the class properties

    def update_verif(self, owner_verif):
        """Method to update the ownershiup verification code
        owner_verif -- ownership verificatio - options - 1, 2, 3, 4, 5, N"""
        # navigate to CARS panel in MAXIS
        at_CARS = bzio.ReadScreen(4, 2, 44)
        if at_CARS != "CARS":
            FuncLib.navigate_to_MAXIS_screen(self.case, self.month, self.year, "STAT", "CARS")
        bzio.WriteScreen(self.member, 20, 76)           # navigating to the correct member and instance of the panel
        bzio.WriteScreen(self.instance, 20, 79)
        FuncLib.transmit()

        FuncLib.PF9()       # puts panel in edit mode

        # TODO create and insert method to verify CARS panel is in edit mode

        bzio.WriteScreen(owner_verif, 10, 60)   # writing in the verif of ownership

        self.gather_data()      # filling all the class properties

    def update_amount_owed(self, amount, owed_date, owed_verif):
        """Method to update the amount, verif, date of a loan balance
        Arguments: amount -- value of the loan balance
                   owed_date -- date of the loan balance - mm/dd/yy format
                   owed_verif -- verif code of the loan balance - options: 1, 2, 3, 4, N"""
        # navigate to CARS panel in MAXIS
        at_CARS = bzio.ReadScreen(4, 2, 44)
        if at_CARS != "CARS":
            FuncLib.navigate_to_MAXIS_screen(self.case, self.month, self.year, "STAT", "CARS")
        bzio.WriteScreen(self.member, 20, 76)           # navigating to the correct member and instance of the panel
        bzio.WriteScreen(self.instance, 20, 79)
        FuncLib.transmit()

        FuncLib.PF9()       # puts panel in edit mode

        # TODO create and insert method to verify CARS panel is in edit mode

        bzio.WriteScreen("        ", 12, 45)    # blanking the field first so leftovers are not changing the amount
        bzio.WriteScreen(amount, 12, 45)    # writing the amount of loan balance to panel
        bzio.WriteScreen(owed_verif, 12, 60)    # writing the verif code of loan balance
        FuncLib.write_mainframe_date(owed_date, "XX XX XX", [13, 43], [13, 46], [13, 49])   # writing the date to the panel using function

        self.gather_data()      # filling all the class properties


class STAT_CASH_panel:
    """Class to reference STAT/CASH penel.
    Methods in this class: gather_data -- get information from the panel
                           update_cash -- add new panel or change value."""
    def __init__(self, case_number, footer_month, footer_year, member):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year
        self.member

    def gather_data(self):
        """Method to gather information from the panel.
        Properties created: amount -- value of cash indicated - float"""
        # navigate to the STAT/CASH panel
        at_CASH = bzio.ReadScreen(4, 2, 42)
        if at_CASH != "CASH":
            # navigate to the STAT/CASH panel
            FuncLib.navigate_to_MAXIS_screen(self.case, self.month, self.year, "STAT", "CASH")
        bzio.WriteScreen(self.member, 20, 76)       # going to the panel for the correct member
        FuncLib.transmit()

        self.amount = FuncLib.read_float_from_BZ(8, 8, 39)  # reading the value as a float for maths

    def update_cash(self, amount):
        # navigate to the STAT/CASH panel
        at_CASH = bzio.ReadScreen(4, 2, 42)
        if at_CASH != "CASH":
            # navigate to the STAT/CASH panel
            FuncLib.navigate_to_MAXIS_screen(self.case, self.month, self.year, "STAT", "CASH")
        bzio.WriteScreen(self.member, 20, 76)       # going to the panel for the correct member
        FuncLib.transmit()

        # putting the panel in edit mode
        if bzio.ReadScreen(1, 2, 73) == "0":    # if no panel exists - create a new one
            bzio.WriteScreen("NN", 20, 79)
            FuncLib.transmit()
        else:                                   # if a panel does exists - put in edit mode
            FuncLib.PF9()

        # FIXME add function to be sure CASH panel is in edit mode.

        if amount is 0:                         # if the amount is 0 - the cleanest way is to delete the panel
            bzio.WriteScreen("DEL", 20, 71)     # this goes in the command line
        else:                                       # if a value actually exists then it will be writen to the panel
            bzio.WriteScreen("        ", 8, 39)     # blanking the line out so that we don't get jumbled values
            bzio.WriteScreen(amount, 8, 39)         # writing the value in to the panel

        FuncLib.transmit()                      # submitting the panel - saving the value or deleting the panel


class STAT_COEX_panel:
    """Class references the STAT/COEX panel.
    Methods in this class: gather_data -- collecting all information from the panels and assigning it properties
                           update_support -- add or update amount of support order
                           update_alimony -- add or update amount of alimony order
                           update_tax_dep -- add pr update amount for tax dependents
                           update_other -- add or update amount of other expense order"""
    def __init__(self, case_number, footer_month, footer_year, member):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year
        self.member

    def gather_data(self):
        """Method will collect all the information from the panel and assign it to class properties.
        Propertis created: support_retro --
                           support_prosp --
                           support_verif --
                           support_hc_est --
                           alimony_retro --
                           alimony_prosp --
                           alimony_verif --
                           alimony_hc_est --
                           tax_dep_retro --
                           tax_dep_prosp --
                           tax_del_verif --
                           tax_dep_hc_est --
                           other_retro --
                           other_prosp --
                           other_verif --
                           other_hc_est --
                           total_retro --
                           total_prosp --
                           change_in_fin_circ --"""
        pass


class STAT_DCEX_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_DFLN_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_DIET_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_DISA_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_DISQ_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_DSTT_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_EATS_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_EMMA_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_EMPS_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_FACI_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_FCFC_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_FCPL_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_FMED_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_HCMI_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_HCRE_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_HEST_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_IMIG_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_INSA_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_JOBS_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_LUMP_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_MEDI_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_MEMB_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_MEMI_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_MISC_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_MMSA_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_MSUR_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_OTHR_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_PACT_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_PARE_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_PBEN_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_PDED_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_PREG_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_PROG_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_RBIC_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_REMO_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_RESI_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_REST_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_REVW_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_SANC_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_SCHL_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_SECU_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_SHEL_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_SIBL_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_SPON_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_STEC_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_STIN_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_STRK_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_STWK_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_SWKR_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_TIME_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_TRAC_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_TRAN_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_TYPE_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_UNEA_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_WKEX_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass


class STAT_WREG_panel:
    def __init__(self, case_number, footer_month, footer_year):
        self.case = case_number
        self.month = footer_month
        self.year = footer_year

    def gather_data(self):
        pass
