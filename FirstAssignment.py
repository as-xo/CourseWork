def clean_up():
    f = 'text_to_clean.txt'
    sf = 'student_names.txt'
    cleaned = ""
    with open('text_to_clean.txt', 'r') as f: # open txt file and read into function
        text = f.read()
        for line in text.split('\n'):
            clean_line = ''
            for char in line:
                x = ord(char)
                if 65 <= x <= 90 or 97 <= x <= 122 or x == 46 or x == 32:
                    clean_line = clean_line + char
            cleaned = cleaned + clean_line + '\n'
    with open('student_names.txt', 'w') as g:  
        g.write(cleaned)
    return cleaned

def build_id():
    id_list = []
    with open('student_names.txt', 'r') as build: # open txt file to read into function
        for eachPass in build:
            name = eachPass.split() # assign the list to the variable name
            name_list = ""
             
            if len(name) == 3: # for names with 3 parts, splice first char of each name
                 for initial in name:
                     name_list += initial[0].lower()
                     
            elif len(name) == 2: # for names with two parts, splice first char of each name, but add x for missing middle name initial
                name_list += name[0][0].lower() 
                name_list += 'x'
                name_list += name[1][0].lower()
                                  
            id_list.append(name_list)
    return id_list

def validate_password(password):
    with open('password.txt', 'r') as val:
        illegal_password = []
        alph_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_0123456789"
         
        if len(password) < 8:
            illegal_password.append("TOO SHORT")
        if len(password) > 12:
            illegal_password.append("TOO LONG") 
        for char in password:
            if char not in alph_chars:
                illegal_password.append("WRONG CHARACTERS")
        if password == password.lower() or password == password.upper():
            illegal_password.append("NOT MIXED CASE")
        if password[0].isdigit():
            illegal_password.append("LEADING DIGIT")
        if password in val.read():
            illegal_password.append("CANNOT MAKE USE OF THIS PASSWORD")
    return illegal_password

def create_unique(id_list):
    final_list = []
    unique_id_counts = {}
     

    with open('create_emails.txt', 'w') as create_emails_file:
      with open('unique_ids.txt', 'w') as unique_ids_file:
    
        for current_id in id_list: # increment count by 1 in each loop if found in unique_id else 0
            if current_id in unique_id_counts:
               count = unique_id_counts[current_id]
               unique_id_counts[current_id] += 1 
            else:
                unique_id_counts[current_id] = 0     # no increment
                
            character_count = str(unique_id_counts[current_id])
            zeros_count = 4 - len(character_count)
            total_count = ""
            for x in range(zeros_count):
                total_count += "0"
            total_count += character_count

            U_id = f"{current_id}{total_count}"
    
            email = f"{U_id}@student.bham.ac.uk" 
            create_emails_file.write(email + '\n')
            unique_ids_file.write(U_id + '\n')

            final_list.append(U_id)        
    return final_list

def create_short_address():
    f = "addresses.txt"
    split_addrs = []
    
    with open('addresses.txt', 'r') as addy:
        for eachPass in addy:
            loc = eachPass.split(', ')
            if len(loc) >= 4:
                loc_list = [loc[0], loc[3][:-1]]
                split_addrs.append(loc_list)
    return split_addrs

def validate_pcode(split_addrs):
    validate_pcode = []
    valid_character = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    valid_digit = "0123456789"
    count = 0

    for i in split_addrs:
        post_c = i[1]
        validate_pcode.append(count) 
        
        if len(i[1]) != 6: # verify len of char == 6
            validate_pcode.append("False")
            post_c = "$$$$$$"
        else:
            validate_pcode.append("True")

        if post_c[0] in valid_character: # if first char is valid upper 
            validate_pcode.append("True")
        else:
            validate_pcode.append("False")   
            
        if post_c[1] in valid_digit and post_c[2] in valid_digit and post_c[3] in valid_digit: # if 2nd 3rd 4th char is number
            validate_pcode.append("True")
        else:
            validate_pcode.append("False")

        if post_c[-2] in valid_character and post_c[-1] in valid_character: # last two chars is valid upper
            validate_pcode.append("True")
        else:
            validate_pcode.append("False")
        count += 1

    return validate_pcode

def ids_addrs(short_addr):
    f = open("unique_ids.txt", 'r')
    ids = f.read()
    combo = {}
    
    count = 0
    unique_ids = ids.split('\n')

    for id in range(len(unique_ids) -1):
        combo[unique_ids[id]] = short_addr[id]
        count += 1
    f.close()
    return combo

def main():
    id_list = []
    while True:
        print("\nStudent File Menu:")
        print("1. Perform clean up operation")
        print("2. Create ID's")
        print("3. Validate a Password")
        print("4. Create unique ID's")
        print("5. Reduce addresses")
        print("6. Validate postcode")
        print("7. Create ID with short address")
        print("8. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            clean_up()
        elif choice == '2':
            id_list = build_id()
        elif choice == '3':
            validate_password("1abcDE%")
        elif choice == '4':
            create_unique(id_list)
        elif choice == '5':
            short_addr = create_short_address()
        elif choice == '6':
            validate_pcode(short_addr)
        elif choice == '7':
            ids_addrs(short_addr)
        elif choice == '8':
            break
        else:
            print("Invalid choice! Please choose again.")

if __name__ == "__main__":
    main()

"""
    Adhere to the instructions in question 4 to determine a unique id for each student
    Write the content of the unique ids to the file unique_ids.txt - open / close the file correctly
    Write the content of the emails created to the file create_emails.txt - - open / close the file correctly
    :param id_list: the id_list that was returned in build_id() is used here to create the unique ids
    :return: final_list is returned and this list contains all of the unique student ids
    """