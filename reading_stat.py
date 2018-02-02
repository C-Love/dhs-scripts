"""Testing Script for these classes"""

import bzio
import wx
import wx.xrc
import FuncLib
import MAXIS_panels
# Importing these modules is critical
# the bzio, FuncLib, and MAXIS_panels are modules based off of scripts in the same directory.
# MAXIS_panels is the module with all the code to read and create panels in MAXIS.

""" The intention here is that we can save on lines of code and have cleaner code if our functionality is in classes with properties and methods.
This way we do not have to code reading pannels into seperate scripts - it can happen just by calling a class and its method.
This also makes any MAXIS changes easier to resolve as we only have to change coordinates in one place."""

bzio.Connect("")
bzio.Focus()

# QUESTION Can we make this global to modules so we don't have to pass it through as a parameter?
global MAXIS_case_number

# defining case number and footer month and year
# I ran this on a training case as it DOES UPDATE Panels
# the training case has ADDR, ABPS, and 1 ACCT panel for MEMB 01
MAXIS_case_number = FuncLib.MAXIS_case_number_finder()
MAXIS_case_number = str(MAXIS_case_number)
footer_mo_yr = FuncLib.MAXIS_footer_finder()
MAXIS_footer_month = footer_mo_yr[0]
MAXIS_footer_year = footer_mo_yr[1]

# creates an object and sets that to an ADDR Panel class
ADDR = MAXIS_panels.STAT_ADDR_panel(MAXIS_case_number, MAXIS_footer_month, MAXIS_footer_year)
ADDR.gather_data()      # using the method of the ADDR Panel class to get all information from the panel

# creates an object and sets it to an ABPS Panel class
# this class needs an instance parameter
ABPS_01 = MAXIS_panels.STAT_ABPS_panel(MAXIS_case_number, MAXIS_footer_month, MAXIS_footer_year, "01")
ABPS_01.gather_data()   # using the method from ABPS to get all information - this LOOKs like the same method as above but it is specific to this panel

# creates an oject and sets it to the ACCT Panel class
# this class requires member and instance parameter
ACCT_01_01 = MAXIS_panels.STAT_ACCT_panel(MAXIS_case_number, MAXIS_footer_month, MAXIS_footer_year, "01", "01")
ACCT_01_01.gather_data()  # getting all information from ACCT 01 01 panel

# creating an object and setting it to ACCT Panel class - this is the same class as above BUT a different object with different property assignments
# note that this panel does not exist yet - but the object is defined in the script
ACCT_01_02 = MAXIS_panels.STAT_ACCT_panel(MAXIS_case_number, MAXIS_footer_month, MAXIS_footer_year, "01", "02")
ACCT_01_02.create_new("SV", "434", "6", "12/30/2017", "", "Wells Fargo")    # using method defined in the class to create a brand new panel

# this outputs the code from above so we can see it worked.
print(ADDR.case)
print(ADDR.resi1)
print(ADDR.resi_city)
print(ADDR.resi_verif)
print(ADDR.phone_list)
print(ADDR.effective_date)

print("Absent parent is %s and is the parent of %s" % (ABPS_01.full_name, ABPS_01.children))
print("")
print("Account is at " + ACCT_01_01.location)
print("Account number: " + ACCT_01_01.number)
print("Balance is " + ACCT_01_01.balance)
print("Verification is " + ACCT_01_01.balance_verif)
print("New account instance: " + ACCT_01_02.instance)
