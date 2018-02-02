"""Testing Script for these classes"""

import bzio
import wx
import wx.xrc
import FuncLib
import MAXIS_panels

bzio.Connect("")
bzio.Focus()

global MAXIS_case_number

MAXIS_case_number = FuncLib.MAXIS_case_number_finder()
MAXIS_case_number = str(MAXIS_case_number)
footer_mo_yr = FuncLib.MAXIS_footer_finder()
MAXIS_footer_month = footer_mo_yr[0]
MAXIS_footer_year = footer_mo_yr[1]

ADDR = MAXIS_panels.STAT_ADDR_panel(MAXIS_case_number, MAXIS_footer_month, MAXIS_footer_year)
ADDR.gather_data()

ABPS_01 = MAXIS_panels.STAT_ABPS_panel(MAXIS_case_number, MAXIS_footer_month, MAXIS_footer_year, "01")
ABPS_01.gather_data()

ACCT_01_01 = MAXIS_panels.STAT_ACCT_panel(MAXIS_case_number, MAXIS_footer_month, MAXIS_footer_year, "01", "01")
ACCT_01_01.gather_data()

ACCT_01_02 = MAXIS_panels.STAT_ACCT_panel(MAXIS_case_number, MAXIS_footer_month, MAXIS_footer_year, "01", "02")
ACCT_01_02.create_new("SV", "434", "6", "12/30/2017", "", "Wells Fargo")

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
