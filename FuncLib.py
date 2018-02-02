"""Temporary FUNCLib"""

import bzio


global MAXIS_case_number


def mainframe_date(date, format):
    date_split = date.split("/")
    format = format.upper()
    if len(date_split[0]) == 1:
        date_split[0] = "0" + date_split[0]
    if len(date_split[1]) == 1:
        date_split[1] = "0" + date_split[1]
    if format == "XX XX XX" or "XX XX":
        if len(date_split[2]) == 4:
            date_split[2] = date_split[2][2:]
    elif format == "XX XX XXXX":
        if len(date_split[2]) == 2:
            date_split[2] = "20" + date_split[2]

    if format == "XX XX":
        del date_split[1]

    return date_split


def find_variable(opening_string, length_of_variable):
    search_result = bzio.Search(opening_string)
    row = search_result[1]
    col = search_result[2]
    if row != 0:
        return bzio.ReadScreen(length_of_variable, row, col + len(opening_string))


# FuncLib fucntions created
def MAXIS_case_number_finder():
    SELF_check = bzio.ReadScreen(4, 2, 50)
    if SELF_check == "SELF":
        variable_for_MAXIS_case_number = bzio.ReadScreen(8, 18, 43)
        variable_for_MAXIS_case_number = variable_for_MAXIS_case_number.replace("_", "")
        variable_for_MAXIS_case_number = variable_for_MAXIS_case_number.lstrip()
        variable_for_MAXIS_case_number = variable_for_MAXIS_case_number.rstrip()
    else:
        # row = 1
        # col = 1
        title_loc = bzio.Search("Case Nbr:")
        row = title_loc[1]
        col = title_loc[2]

        if row != 0:
            variable_for_MAXIS_case_number = bzio.ReadScreen(8, row, col + 10)
            variable_for_MAXIS_case_number = variable_for_MAXIS_case_number.replace("_", "")
            variable_for_MAXIS_case_number = variable_for_MAXIS_case_number.lstrip()
            variable_for_MAXIS_case_number = variable_for_MAXIS_case_number.rstrip()
    return variable_for_MAXIS_case_number


def MAXIS_footer_finder():
    SELF_check = bzio.ReadScreen(4, 2, 50)
    if SELF_check == "SELF":
        MAXIS_footer_month = bzio.ReadScreen(2, 20, 43)
        MAXIS_footer_year = bzio.ReadScreen(2, 20, 46)
    else:
        MEMO_check = bzio.ReadScreen(4, 2, 47)
        if MEMO_check == "MEMO":
            MAXIS_footer_month = bzio.ReadScreen(2, 19, 54)
            MAXIS_footer_year = bzio.ReadScreen(2, 49, 57)
        else:
            MAXIS_footer = find_variable("Month: ", 5)
            MAXIS_footer_month = MAXIS_footer[:2]
            MAXIS_footer_year = MAXIS_footer[3:]
    return [MAXIS_footer_month, MAXIS_footer_year]


def transmit():
    bzio.SendKey("<enter>")
    bzio.WaitReady(0, 0)


def check_for_MAXIS(end_script):
    MAXIS_check = ""
    while MAXIS_check != "MAXIS" or MAXIS_check != "AXIS ":
        transmit()
        MAXIS_check = bzio.ReadScreen(5, 1, 39)
        print(MAXIS_check)
        if MAXIS_check != "MAXIS" and MAXIS_check != "AXIS ":
            if end_script:
                bzio.MsgBox("You do not appear to be in AMXIS. You may be passworded out. Please check your MAXIS screen and thry again.")
                quit()
            else:
                bzio.MsgBox("You do not appear to be in MAXIS.\
                            You may be passworded out. Please check you MAXIS screen and they again, or press CANCEL to exit the script.")
        else:
            break


def PF3():
    bzio.SendKey("<PF3>")
    print("sent")
    bzio.WaitReady(0, 0)


def PF7():
    bzio.SendKey("<PF8>")
    bzio.WaitReady(0, 0)


def PF8():
    bzio.SendKey("<PF8>")
    bzio.WaitReady(0, 0)


def ShiftPF8():
    bzio.SendKey("<PF8>", "<shift>")
    bzio.WaitReady(0, 0)


def PF9():
    bzio.SendKey("<PF9>")
    bzio.WaitReady(0, 0)


def navigate_to_MAXIS_screen(case_number, footer_month, footer_year, function_to_go_to, command_to_go_to):
    transmit()
    MAXIS_check = bzio.ReadScreen(5, 1, 39)
    function_to_go_to = function_to_go_to.upper()
    command_to_go_to = command_to_go_to.upper()

    if MAXIS_check == "MAXIS" or MAXIS_check == "AXIS ":
        locked_panel = bzio.ReadScreen(23, 2, 30)
        if locked_panel == "Program History Display":
            PF3()

        find_function = bzio.Search("Function: ")
        row = find_function[1]
        col = find_function[2]

        if row != 0:
            MAXIS_function = bzio.ReadScreen(4, row, col + 10)
            STAT_note_check = bzio.ReadScreen(4, 2, 45)

            find_case_nbr = bzio.Search("Case Nbr: ")
            row = find_case_nbr[1]
            col = find_case_nbr[2]
            if row != 0:
                current_case_number = bzio.ReadScreen(8, row, col + 10)
                current_case_number = current_case_number.replace("_", "")
                current_case_number = current_case_number.lstrip()
                current_case_number = current_case_number.rstrip()
            else:
                current_case_number = ""

        if current_case_number == case_number and MAXIS_function == function_to_go_to and STAT_note_check != "NOTE":
            find_command = bzio.Search("Command: ")
            row = find_command[1]
            col = find_command[2]

            bzio.WriteScreen(command_to_go_to, row, col + 9)
            transmit()
        else:
            SELF_check = ""
            while SELF_check != "SELF":
                PF3()
                SELF_check = bzio.ReadScreen(4, 2, 50)

            bzio.WriteScreen(function_to_go_to, 16, 43)
            bzio.WriteScreen("________", 18, 43)
            bzio.WriteScreen(case_number, 18, 43)
            bzio.WriteScreen(footer_month, 20, 43)
            bzio.WriteScreen(footer_year, 20, 46)
            bzio.WriteScreen(command_to_go_to, 21, 70)
            transmit()

            abended_check = bzio.ReadScreen(7, 9, 27)
            if abended_check == "abended":
                transmit()

            ERRR_check = bzio.ReadScreen(4, 2, 52)
            if ERRR_check == "ERRR":
                transmit()


def start_a_blank_case_note():
    navigate_to_MAXIS_screen("CASE", "NOTE")
    mode_check = ""
    while mode_check != "A" and mode_check != "E":
        PF9()
        case_note_check = bzio.ReadScreen(17, 2, 33)
        mode_check = bzio.ReadScreen(1, 20, 9)
        if case_note_check != "Case Notes (NOTE)" or mode_check != "A":
            bzio.MsgBox("The script can't open a case note. Reasons may include:\n \n \
                        * You may be in inquiry \n \
                        * You may not have authorization to case note this case (e.g.: out-of-county case)\n \n \
                        Check MAXIS and/or navigate to CASE/NOTE, and try again. You can press the STOP SCRIPT button on the power pad to stop the script.")


def write_bullet_and_variable_in_CASE_NOTE(bullet, variable):
    variable.rstrip()
    variable.lstrip()
    if variable != "":
        noting_row = bzio.CursorRow()			# Needs to get the row and col to start. Doesn't need to get it in the array function because that uses WriteScreen.
        noting_col = bzio.CursorCol()
        noting_col = 3							# The noting col should always be 3 at this point, because it is the beginning. But, this will be dynamically recreated each time.
        # The following figures out if we need a new page, or if we need a new case note entirely.
        character_test = ""
        while character_test != " ":
            character_test = bzio.ReadScreen(1, noting_row, noting_col)
            # Reads a single character at the noting row/col. If there's a character there, it needs to go down a row, and look again until there's nothing.
            # It also needs to trigger these events if it's at or above row 18 (which means we're beyond case note range).
            if character_test != " " or noting_row >= 18:
                noting_row += 1

                # If we get to row 18 (which can't be read here), it will go to the next panel (PF8).
                if noting_row >= 18:
                    PF8()

                    # Checks to see if we've reached the end of available case notes. If we are, it will get us to a new case note.
                    end_of_case_note_check = bzio.ReadScreen(1, 24, 2)
                    if end_of_case_note_check == "A":
                        PF3()
                        PF9()
                        bzio.WriteScreen("~~~continued from previous note~~~", 4, 3)		# Enters a header
                        bzio.SetCursor(5, 3)												# Sets cursor in a good place to start noting.
                        noting_row = 5														# Resets this variable to work in the new Locale
                    else:
                        noting_row = 4														# Resets this variable to 4 if we did not need a brand new note.

        # Looks at the length of the bullet. This determines the indent for the rest of the info. Going with a maximum indent of 18.
        if len(bullet) >= 14:
            indent_length = 18		# It's four ore than the bullet text to account for the asterisk, the colon, and the space.
        else:
            indent_length = len(bullet) + 4		# It's four more for the reason explained above.

        # Writes the bullet
        bzio.WriteScreen("* %s: " % (bullet), noting_row, noting_col)

        # Determines new noting_col based on Length of the bullet length (bullet + 4 to account for asterisk, colon, and spaces).
        noting_col = noting_col + (len(bullet) + 4)

        # Splits the contents of the variable into an array of words
        variable_array = variable.split()

        for word in variable_array:
            # If the length of the word would go past col 80 (you can't write to col 80), it will kick to the next line and indent the length of the bullet
            if len(word) + noting_col > 80:
                noting_row += 1
                noting_col = 3

            # If the next line is row 18 (you can't write to row 18), it will PF8 to get to the next page
            if noting_row >= 18:
                PF8()

                # Checks to see if we've reached the end of available case notes. If we are, it will get us to a new case note.
                end_of_case_note_check = bzio.ReadScreen(1, 24, 2)
                if end_of_case_note_check == "A":
                    PF3()
                    PF9()
                    bzio.WriteScreen("~~~continued from previous note~~~", 4, 3)    # enters a header
                    bzio.SetCursor(5, 3)												# Sets cursor in a good place to start noting.
                    noting_row = 5														# Resets this variable to work in the new Locale
                else:
                    noting_row = 4														# Resets this variable to 4 if we did not need a brand new note.

            # Adds spaces (indent) if we're on col 3 since it's the beginning of a line. We also ahve to increase the noting col in these instances
            # (so it does not overwrite the indent).
            if noting_col == 3:
                word = word.rjust(indent_length)

            # Writes the word and a space using bzio.WriteScreen
            bzio.WriteScreen(word.replace(";", "") + " ", noting_row, noting_col)

            # If a semicolon is seen (we use this to mean "go down a row") it will kick the noting row down by one and add more indent again.
            if word.endswith(";"):
                noting_row += 1
                noting_col = 3

            # Increases noting_col the length of the word + 1 (for the space)
            noting_col = noting_col + (len(word) + 1)

        bzio.SetCursor(noting_row + 1, 3)


def write_variable_in_CASE_NOTE(variable):
    variable.lstrip()
    variable.rstrip()
    if variable != "":
        noting_row = bzio.CursorRow()        # Needs to get the row and col to start. Doesn't need to get it in the array function because that uses WriteScreen
        noting_col = 3         # The noting col should always be 3 at this point, because it's the beginning. But, this will be dynamically recreated each time.
        # The following figures out if we need a new page, or if we need a new case note entirely as well.
        character_test = ""
        while character_test != " ":
            # Reads a single character at the noting row/col. If there's a character there, it needs to go down a row, and look again until there's nothing.
            # It also needs to trigger these events if it's at or above row 18 (which means we're beyond case note range).
            character_test = bzio.ReadScreen(1, noting_row, noting_col)
            if character_test != " " or noting_row >= 18:
                noting_row += 1

                # If we get to row 18 (which can't be read here), it will go to the next panel (PF8).
                if noting_row >= 18:
                    PF8()

                    # Checks to see if we've reached the end of available case notes. If we are, it will get us to a new case note.
                    end_of_case_note_check = bzio.ReadScreen(1, 24, 2)
                    if end_of_case_note_check == "A":
                        PF3()
                        PF9()
                        bzio.WriteScreen("~~~continued from previous note~~~", 4, 3)		# Enters a header
                        bzio.SetCursor(5, 3)												# Sets cursor in a good place to start noting.
                        noting_row = 5														# Resets this variable to work in the new Locale
                    else:
                        noting_row = 4														# Resets this variable to 4 if we did not need a brand new note.

        # Splits the contents of the variable into an array of words
        variable_array = variable.split()

        for word in variable_array:
            # If the length of the word would go past col 80 (you can't write to col 80), it will kick to the next line and indent the length of the bullet
            if len(word) + noting_col > 80:
                noting_row += 1
                noting_col = 3

            # If the next line is row 18 (you can't write to row 18), it will PF8 to get to the next page
            if noting_row >= 18:
                PF8()

                # Checks to see if we've reached the end of available case notes. If we are, it will get us to a new case note.
                end_of_case_note_check = bzio.ReadScreen(1, 24, 2)
                if end_of_case_note_check == "A":
                    PF3()
                    PF9()
                    bzio.WriteScreen("~~~continued from previous note~~~", 4, 3)    # enters a header
                    bzio.SetCursor(5, 3)												# Sets cursor in a good place to start noting.
                    noting_row = 5														# Resets this variable to work in the new Locale
                else:
                    noting_row = 4														# Resets this variable to 4 if we did not need a brand new note.

            # Writes the word and a space using bzio.WriteScreen
            bzio.WriteScreen(word.replace(";", "") + " ", noting_row, noting_col)

            # If a semicolon is seen (we use this to mean "go down a row") it will kick the noting row down by one and add more indent again.
            if word.endswith(";"):
                noting_row += 1
                noting_col = 3

            # Increases noting_col the length of the word + 1 (for the space)
            noting_col = noting_col + (len(word) + 1)

        bzio.SetCursor(noting_row + 1, 3)
