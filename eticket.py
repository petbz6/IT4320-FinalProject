# Generates a unique e-ticket number
# The first name of the passenger is combined with the string "IT4320" alternating every other character
def generate_e_ticket_number(first_name):
    INFOTC4320_string = "INFOTC4320"
    combined_string = ""
    
    for i in range(max(len(first_name), len(INFOTC4320_string))):
        if i < len(first_name):
            combined_string += first_name[i]
        if i < len(INFOTC4320_string):
            combined_string += INFOTC4320_string[i]
    return combined_string
