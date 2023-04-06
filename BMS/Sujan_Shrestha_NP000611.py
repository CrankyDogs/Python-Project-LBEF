#Sujan Shrestha
#NP000611

from stdiomask import *
import stdiomask
import sys
import datetime
import re
import calendar
from uuid import uuid4
import tabulate


#------------------------------------------------for Admin Log--------------------------------------------------------------------------------------
def admin():
    while True:
        name_admin = input("Enter your admin username: ")
        password_admin = getpass("Please enter your password: ", mask='*') #stdiomask to show user inputed password in * symbol.
        admins = open('admin.txt','r')
        temp = 0
        for line in admins:  #checking if the admin provided credentials are valied or not in text file named admin

            if name_admin in line and password_admin in line:
                temp = 1
        if temp:
            print("\n Admin Logged In Successfully")
            admin_functions()#provides access for admin function when logged in
        else:
            print("\n Error!!!! Please check the credentials you've entered")



#--------------------------------------Admin access and menu to be performed by admin only---------------------------------------------------------

def admin_functions():
    print(""" \n
    **********************************ADMIN MENU*****************************************
           1. Verify Loan Requests from Customers (Press 1 to choose this option)
           2. Check for Request of New Customers  (Press 2 to choose this option)
           3. View Transactios                    (Press 3 to choose this option)
           4. Retrun to Main Menu                 (Press 4 to choose this option)
    \n """ )
    try:
        ch = int(input("Select The Activity You Want To Perform(1-4)"))#asking admin for input for next step
    except:
        print("\nOnly Number Inputs Are Acceptable")
        admin_functions()
    else:
        if ch == 1:
            loan_req_verify()
        elif ch == 2:
            customer_req_verify()
        elif ch == 3:
            view_transactions_menu()
        else:
            main_menu()

#----------------------------------------------------------------Loan Request Verify-----------------------------------------------------------------------------------

def loan_req_verify():
                place_loan_id_in_file()
                view_unverified_loan()#calling function that prints all unverified loans
                loan_verify = input("\nDo you want to verify any user loans (y/n) ?")
                while loan_verify == 'y':
                    loan_id = input("Enter Loan ID provided above to verify loan of any ID: ")

                    if verify_user_loan_id(loan_id): # calling function that verify requested user id and write in a file
                        if placing_installment_date(loan_id): # calling function that place installment data in a file
                            if calculates_loan_emi(loan_id): # calling function that writes loan calculation details in a file
                                    print(f"\n Loan ID '{loan_id}' has been verified...\n")
                            loan_req_verify()
                admin_functions()

#---------------------------------------------------------------Customer Request Verify-----------------------------------------------------------------------------------
def customer_req_verify():

                view_unverified_requests()#calling function that prints all unverified loans
                req_verify =  input("\nDo you want to verify any user request (y/n) ?  ")
                while req_verify == 'y':
                     username = input("Enter username whose request you want to verify: ")
                     if verify_customers(username):
                        
                        print(f"\n{username} has been verified...\n")
                        customer_req_verify()
                admin_functions()

#----------------------------------------------------------------View Transaction Menu-----------------------------------------------------------------------------------

def view_transactions_menu():    # view transactions menu
    print("""
****************************** Transactions Menu ****************************\n    
    1. View transactio of Specific Customers  (Press 1 to select this option)
    2. View transaction of Specific Loan Type (Press 2 to select this option)
    3. View transaction of all customer       (Press 3 to select this option)
    4. View transaction of all types Loan     (Press 4 to select this option)
    5. Go to Admin Menu                       (Press 5 to select this option)
    """)
    ch = int(input("\nPlease select the option you want to perform(1-5):"))
    if ch == 1:
        view_trans_of_specific_user()
    elif ch == 2:
        view_of_transaction_of_specific_loan_type()
    elif ch == 3:
        view_all_customers()
    elif ch == 4:
        view_transactions_of_all_types_loan()
    else:
        admin_functions()

#------------------------------------------------------------------return_to_transaction_menu---------------------------------------------------------------------------------

def return_to_transaction_menu():  # go back to trans menu
    inp_user = input("\nDo you want to go back to previous menu (y/n)?")
    if inp_user == 'y':
        view_transactions_menu()
    else: 
        sys.exit()
        
    
#------------------------------------------------------------------View transaction for specific user----------------------------------------------------------------------

def view_trans_of_specific_user(): #to view transaction of specific customer
    name_user = input("Enter username of the customer: ")  
    detail_of_loan = read_file_data('all_loan_data.txt','r')# reading txt file to get info about transaction of entered user
    table_data = []
    for loan_data in detail_of_loan:#checking data of txt file
        if loan_data[2] == name_user: 

            titled_data = loan_data[1],loan_data[2],loan_data[4],loan_data[5],loan_data[6]+' years',loan_data[7] +' %',loan_data[8],loan_data[9]
            table_data.append(titled_data)
    title = ['Loan Id','Username','Loan Types','Applied Loan Amt','Loan Tenure','Loan Rate','Installment Amt','Due Amt']
    print(tabulate.tabulate(table_data, headers=title,tablefmt="github"))#tabulate module to print data in table in output
    return_to_transaction_menu()


#------------------------------------------------------------------View transaction for specific loan----------------------------------------------------------------------

def view_of_transaction_of_specific_loan_type(): # view transactions of specific loan type
    loan_type = input("""\nPlease type full name of loan type:
    Car Loan
    Education Loan    
    Home Loan
    Personal Loan
    """)
    loan_details = read_file_data('all_loan_data.txt','r') # calling read_file_data 
    table_data = []
    for loan_data in loan_details:
        if loan_type in loan_data:   # checking userid and if it finds, functions other task on the vary line
            t_data = loan_data[1],loan_data[2],loan_data[4],loan_data[5],loan_data[6]+' years',loan_data[7] +' %',loan_data[8],loan_data[9]
            table_data.append(t_data)
    title = ['Loan Id','Username','Loan Types','Applied Loan Amt','Loan Tenure','Loan Rate','Installment Amt','Due Amt']
    print(tabulate.tabulate([t_data], headers=title,tablefmt="github")) #tabulate module to print data in table in output
    return_to_transaction_menu()

#------------------------------------------------------------------View loan of all customer----------------------------------------------------------------------

def view_all_customers():    # view transactions of all customers
    loan_details = read_file_data('all_loan_data.txt','r')
    table_data = []
    for loan_data in loan_details:
        if loan_data[-1] == 'Verified':
            titled_data = loan_data[1],loan_data[2],loan_data[4],loan_data[5],loan_data[6]+' years',loan_data[7] +' %',loan_data[8],loan_data[9]
            table_data.append(titled_data)
            title = ['Loan Id','Username','Loan Types','Applied Loan Amt','Loan Tenure','Loan Rate','Installment Amt','Due Amt']
            print(tabulate.tabulate([titled_data], headers=title,tablefmt="github"))    # using tabulate module to make table
            print('\n')  
    return_to_transaction_menu()

#------------------------------------------------------------------View transaction for all loan types----------------------------------------------------------------------

def view_transactions_of_all_types_loan():
    view_all_customers()# calls all customer function as same thing has to done to view all loans
    return_to_transaction_menu()

#---------------------------------------------------------------Verify customer request---------------------------------------------------------------------

def verify_customers(username): # verify requested userID
    with open('details.txt','r+') as file: 

        customer_details = file.readlines()#checkig data in details.txt
        
        for elem in range(len(customer_details)):#to check in txt file
            if username in customer_details[elem]: # checking if username available in txt file
                user_data = customer_details[elem].split(',')
                user_data[-1] = user_data[-1].replace(user_data[-1][:5],'Verified') # changing unverified to verified of the searched user

                str_ud = ','.join([str(e) for e in user_data]) # converting user data into string
                customer_details[elem] = customer_details[elem].replace(str(customer_details[elem]),str_ud)
        file.seek(0)
        file.writelines(customer_details)
    return True

#------------------------------------------------------------------View unverified requests----------------------------------------------------------------------

def view_unverified_requests():
    a_list = read_file_data('details.txt','r')#opening and reading datails.txt
    pending_users = []#creating list for pending users
    for ab in a_list:
        if ab[-1] == "False":
            pending_users.append(ab)
    title= ["Name", "Address", "E-mail", "Contact No.", "Gender", "DOB", "Username","Password","Is Admin", "User Status"]
    print(tabulate.tabulate(pending_users,title,tablefmt="github"))#tabulate module to print data in table in output

#------------------------------------------------------------------Generate loan ID----------------------------------------------------------------------

def generate_loan_id(): # function to generate unique loan id for new loans
    unique_loan_id = str(uuid4())
    splt_loan_id = unique_loan_id.split('-')
    loan_id = 'LiD-'+''.join(splt_loan_id[4]) 
    return loan_id

#------------------------------------------------------------------place loan id----------------------------------------------------------------------

def place_loan_id_in_file(): # placing user loan id in the file
    with open('all_loan_data.txt','r+') as file:#opening and reading all_loan_data.txt
        loan_details = file.readlines()
        for elem in range(len(loan_details)):
            loan_data = loan_details[elem].split(',')
            if len(loan_data) <7:   # total element with loanid in one line of loan_details.txt is 7  so if more it does not give unique id
                loan_data.insert(1,generate_loan_id()) # inserting called unique loan id
            str_loan_data = ','.join([str(e) for e in loan_data]) # converting user data into comma separated string
            loan_details[elem] = loan_details[elem].replace(str(loan_details[elem]),str_loan_data) # replacing the whole data
        file.seek(0)
        file.writelines(loan_details)

#------------------------------------------------------------------Placing installment date----------------------------------------------------------------------

def placing_installment_date(loan_id): # verify user loan id
    with open('all_loan_data.txt','r+') as file:#opening and reading all_loan_data.txt

        loan_details = file.readlines()
        
        for elem in range(len(loan_details)):
            if loan_id in loan_details[elem]:   # checking userid available or not in file
                
                #  finding installment date
                loan_data = loan_details[elem].split(',')
                loan_data[0] = loan_data[0].split('-')
                loan_data[0] = ','.join(loan_data[0])
                loan_data[0].replace(',','-')
                joined_date = datetime.datetime.strptime(loan_data[0],"%Y,%m,%d")
                days_in_month = calendar.monthrange(joined_date.year, joined_date.month)[1]
                installment_date = str(joined_date + datetime.timedelta(days=days_in_month)).split(' ')[0]
                loan_data[0] = loan_data[0].replace(str(loan_data[0]),str(joined_date).split(' ')[0])
                loan_data.insert(3,installment_date) # inserting installment date in file
                str_loan_data = ','.join([str(e) for e in loan_data]) # converting user data into string
                loan_details[elem] = loan_details[elem].replace(str(loan_details[elem]),str_loan_data)
        file.seek(0)
        file.writelines(loan_details)  
    return True

#------------------------------------------------------------------Calculate loan EMI----------------------------------------------------------------------

def calculates_loan_emi(loan_id): # verify user loan id
    with open('all_loan_data.txt','r+') as file:

        loan_details = file.readlines()
        
        for elem in range(len(loan_details)):
            if loan_id in loan_details[elem]:
                loan_data = loan_details[elem].split(',')
                proposed_loan_amt = float(loan_data[5])    # loan amt from file
                loan_tenure = int(loan_data[6]) # laon tenure from file
                loan_types = loan_data[4] # loan_types from file

                if loan_types == 'Car Loan':
                    if loan_tenure <=5:
                        loan_rate = 15
                    elif loan_tenure <=10:
                        loan_rate = 17
                    else:
                        print("Loan period is out of range !!!") 

                elif loan_types == 'Education Loan':
                    if loan_tenure <=5:
                        loan_rate = 12
                    elif loan_tenure <=10:
                        loan_rate = 14
                    else:
                        print("Loan period is out of range !!!")
                
                elif loan_types == 'Home Loan':
                    if loan_tenure <=5:
                        loan_rate = 10
                    elif loan_tenure <=10:
                        loan_rate = 14
                    elif loan_tenure > 10:
                        loan_rate = 18
                
                elif loan_types == 'Personal Loan':
                    if loan_tenure <=5:
                        loan_rate = 14
                    elif loan_tenure <=10:
                        loan_rate = 15
                    else:
                        print("Loan period is out of range !!!")
                    
                num_of_months = loan_tenure *12
                r = loan_rate/(12*100)  # calculates interest rate per month    
                emi = proposed_loan_amt * r * ((1+r)**num_of_months)/((1+r)**num_of_months - 1) # calculates Equated Monthly Installment (EMI)
                total_loan_amt = emi * num_of_months

                loan_data.insert(7,loan_rate)
                loan_data.insert(8,round(emi,3))
                loan_data.insert(9,round(total_loan_amt,3))
                                
                str_loan_data = ','.join([str(e) for e in loan_data]) # converting user data into string
                loan_details[elem] = loan_details[elem].replace(str(loan_details[elem]),str_loan_data)
        file.seek(0)
        file.writelines(loan_details)  
    return True

#------------------------------------------------------------------Calculate installment date----------------------------------------------------------------------

def get_installment_date():  # Finding next month installment date
    c_list = read_file_data('all_loan_data.txt','r')

    for loaned_date in c_list:
        loaned_date[0] = str(loaned_date[0]).split('-')
        loaned_date[0] = ','.join(loaned_date[0])
    
    loaned_date[0]=loaned_date[0].replace(',','-')
    loan_borrowed_date = datetime.datetime.strptime(loaned_date[0],"%Y,%m,%d")
    days_in_month = calendar.monthrange(loan_borrowed_date.year, loan_borrowed_date.month)[1]
    installment_date = str(loan_borrowed_date + datetime.timedelta(days=days_in_month)).split(' ')[0]
    return installment_date

#------------------------------------------------------------------view unverified loan----------------------------------------------------------------------

def view_unverified_loan(): # verify unverified loans
    place_loan_id_in_file()      # calling generated loan id to write in file
    loan_list = read_file_data('all_loan_data.txt','r')
    pending_loans  = []
    for ele in loan_list:
        if ele[-1] == "False":
            pending_loans.append(ele)
    title = ["Applied Date","Loan ID","Username","Loan Type","Loan Amount","Loan Tenure","Loan Status"]
    print(tabulate.tabulate(pending_loans,title,tablefmt="github"))

#------------------------------------------------------------------Verify user loan requestss----------------------------------------------------------------------

def verify_user_loan_id(loan_id): # verify user loan id
    with open('all_loan_data.txt','r+') as file:

        loan_details = file.readlines()
        
        for elem in range(len(loan_details)):
            if loan_id in loan_details[elem]: # checking userid in all_loan_data.txt
                loan_data = loan_details[elem].split(',')
                loan_data[-1] = loan_data[-1].replace(loan_data[-1][:5],'Verified') # changing unverified to verified of the searched user
                str_loan_data = ','.join([str(e) for e in loan_data]) # converting user data into string
                loan_details[elem] = loan_details[elem].replace(str(loan_details[elem]),str_loan_data)
        file.seek(0)
        file.writelines(loan_details)
    return True

#------------------------------------------------------------------New Customer Menu----------------------------------------------------------------------

#Customer Functions Starts Here
def newcustomer():
    while True:
        try:
            print("""
            ******************New Customer's Menu**************\n
                1. Check Loan Details       (press 1 to select this option)
                2. For Loan Calculator      (press 2 to select this option)
                3. Register new Account     (press 3 to select this option)
                4. Go to Main Menu          (press 4 to select this option)
            """)
            new_customer = int(input("\nSelect your option (1-4):"))
        except ValueError:
            print("Number Input are only acceptable !!!")
        else:
            if new_customer == 1: # Check loan Details
                show_loan_details()
            elif new_customer == 2: # Loan Calculator
                loan_interest_calc()
            elif new_customer == 3: # Register new Account
                new_account_registration()

            elif new_customer == 4: # main menu
                main_menu()


def new_customer_menu():
    inp_user = input("\nDo you want to go back to previous menu (y/n)?")
    if inp_user == 'y':
        newcustomer()
    else: 
        sys.exit()
#------------------------------------------------------------------Age eligibility calculation----------------------------------------------------------------------

def calculate_age():
    while True:
        try:
            dob = datetime.datetime.strptime(input("Date of birth (yyyy/mm/dd): "), "%Y/%m/%d")
        except ValueError:
            print("\nDate is not in correct format !!!\n")
        else:
            today = datetime.datetime.today()
            age = today.year - dob.year
            
            if age > 18:
                dob = str(dob).split(' ')[0] # splitting date and time
                return dob
                break
                
            else:
                print("Invalid!!!!! Minimum age limit for loan is 18 years !!!\n")

#------------------------------------------------------------------Check username----------------------------------------------------------------------

def check_username():#function to check if username is already taken
    while True:
        user_name = input("Username: ")

        with open('details.txt','r') as fo:

            customer_list = fo.read()
            customer_list = list(filter(None,customer_list.split('\n'))) # splitting by new line and removing empty strings from list 
            temp = 0
            try:
                for ele in customer_list:
                    ele = ele.split(',')
                    if user_name == ele[6]: #checking if username is in the index 9 of file
                        temp = 1
            except:
                return user_name
                break
            else:
                if not temp:
                    return user_name # return new user name
                    break
                else:
                    print("\nUsername is already available.. Tryout next username !!!\n")
                # return True

#------------------------------------------------------------------Check user entered password----------------------------------------------------------------------

def check_user_password(): #to check password is eligible
    
    pswd_pattern = '(?=.*[A-Z]+)(?=.*\d+)(?=.*[!@#$%^.&*]+)(?!.*\s)' # password only includes upper case letters, digits, specific symbols and ignore whitespace
    while 1:
        usr_pswd = input("Enter password: ")
        if len(usr_pswd)<8:
            print("\nYour password must be 8-16 characters long !!!\n")
        elif not re.search(pswd_pattern, usr_pswd): # check password and password pattern are satified or not
            print("\nPassword must contain uppercase, number and special symbols !!!\n")
        else:
            usr_confirm_pswd = input("Enter Confirm Password: ")

            if usr_pswd == usr_confirm_pswd:
                return usr_confirm_pswd
                break

            else:
                print("\nPassword and confirm password is not same.\n")

#------------------------------------------------------------------New account registration----------------------------------------------------------------------

def new_account_registration():
    # reading file and also checking if it exist already If not, file will be created.
        try:
            fp = open('details.txt','r')
        except FileNotFoundError:
            fp = open('details.txt','w')
        else:
            if fp:
                fp.close()
                fp = open("details.txt", "a")
            
        print("Please enter the following requirements to become our new customer: \n ")
        full_name = input("Name: ")
        address = input("Address: ")
        email_ad = input ("E-mail: ")
        contact_no = int (input("Contact no.: "))
        gender = input("Gender: ") 
        date_of_birth = calculate_age() # calling a function that checks if the age is eligibke to apply for loan
        user_name = check_username() # calls a function that checks if user name is already taken or not        
        user_password = check_user_password()#calls a function that checks if the password is eligible
        is_admin = False
        active_user = False
        user_info = f"{full_name.title()},{address.title()},{email_ad},{contact_no},{gender.title()},{date_of_birth},{user_name},{user_password},{is_admin},{active_user}\n"
        print(f"\n{full_name.title()}, Thank you for creating an account ...\n")
        fp.write(user_info)
        fp.close()
        new_customer_menu()

#------------------------------------------------------------------Loan Interest Calculation----------------------------------------------------------------------

def loan_interest_calc(): # loan interest calculator functions
    loan_amt = float(input("Enter amount of Loan: "))
    loan_rate = float(input("Enter Annual Interest Rate (%): "))
    num_of_months = int(input("Enter number of months: " ))
    r = loan_rate/(12*100)  # calculates interest rate per month    
    emi = loan_amt * r * ((1+r)**num_of_months)/((1+r)**num_of_months - 1) # calculates Equated Monthly Installment (EMI)

    print("EMI = %.2f" %emi)
    new_customer_menu()


#**********************************************Registered Customer log in page*********************************************
def reg_customer_login(): # Registered customer login page
    while True:
        usr_name = input("Enter your Username: ")
        usr_psd = getpass("Please enter your password: ", mask='*') #stdiomask to show user inputed password in * symbol.
        fh = open('details.txt','r')
        for line in fh:
            if usr_name in line and usr_psd in line:
                if ('Verified' not in line): # checking if username is verified
                    print(f"\nUsername {usr_name} has not been verified yet !!!\n")
                    break
                print("\nYou have logged in successfully.\n")
                reg_customer_menu(usr_name)
                break            
        
        print("The credentials you've entered are wrong")  
                    
#-----------------------------------------------------------------registered customer menu---------------------------------------------------------------------


def reg_customer_menu(usr_name): # registered customer menu
    while 1:
        print("""
    *****************************Registered Customer Menu********************************\n
              1. View Loan Details and Apply    (Press 1 to choose this option)
              2. Pay Loan Installment           (Press 2 to choose this option)
    **********Choose th below option if you have verified loan transaction****************\n
              3. View Transaction               (Press 3 to choose this option)
              4. Status of Loan                 (Press 4 to choose this option)
              5. Back to Main menu              (Press 5 to choose this option)\n\n""")
        try:
            registered_customer_func = int(input("Select what you want to do (1-5):"))
        except ValueError:
            print("\nNumber inputs are only acceptable !!!\n")
        else:
            if registered_customer_func == 1:
                if show_loan_details():
                    apply_for_loan(usr_name)
                    # reg_customer_menu(usr_name)

            elif registered_customer_func == 2:
                installment_loan_pay(usr_name)

            elif registered_customer_func == 3:
                view_transactions(usr_name)
                    
            elif registered_customer_func == 4:
                    status_of_loan(usr_name)
        
            elif registered_customer_func == 5:
                main_menu()
            
#------------------------------------------------------------------View transaction----------------------------------------------------------------------

def view_transactions(usr_name):
    with open('all_loan_data.txt','r+') as file:#opening and reading all_loan_data.txt
        loan_details = file.readlines()
        table_data = []
        for elem in range(len(loan_details)):
            if usr_name in loan_details[elem]:   # checking userid and if it finds, functions other task on the vary line
                loan_data = loan_details[elem].split(',')
                titled_data = loan_data[10],loan_data[1],loan_data[2],loan_data[8],loan_data[9]
                table_data.append(titled_data)
        title = ['Payment Date','Loan Id', 'User', 'Paid Amount', 'Due Amount']
        print(tabulate.tabulate(table_data,headers=title,tablefmt="github"))#using tabulate module to print data in
        goto_customer_menu(usr_name)

#------------------------------------------------------------------Loan details----------------------------------------------------------------------


def show_loan_details():#loan details
    title = "Loan Details"
    print(title.center(78,"-")) # center "Loan Details" inside - appearance on both sides
    print()
    loans = [['Education Loan (HL)','15%', '17%','-'],
            ['Car Loan (CL)','12%', '14%','-'],
            ['Home Loan (HL)', '10%', '14%', '18%'],
            ['Personal Loan (PL)','14%','15%','-']]
    title= ['Loan Types','Upto 5 years','Upto 10 years','Above 10 years']
    print(tabulate.tabulate(loans, headers=title,tablefmt="github")) 
    return True
    
#------------------------------------------------------------------apply for loan----------------------------------------------------------------------

def apply_for_loan(usr_name):   # function that asks user details for loans
    try:
        fp = open('all_loan_data.txt','r')
    except FileNotFoundError:
        fp = open("all_loan_data.txt","w")
    else:
        if fp:
            fp.close()
            fp = open("all_loan_data.txt", "a") 

    print("\nFill the required fields to apply for loan !\n")
    is_verified = False
    pick_loan_types = available_loan_types()
    proposed_loan = float(input("Enter your proposed Loan Amount: "))
    loan_tenure = int(input ("Tenure of Loans (in years): "))
    loan_applied_date = str(datetime.datetime.today()).split(' ')[0]
    apply_loan = f"{loan_applied_date},{usr_name},{pick_loan_types},{proposed_loan},{loan_tenure},{is_verified}\n"
    
    print("Your loan request has been sent successfully...\n")
    fp.write(apply_loan)
    fp.close()
    goto_customer_menu(usr_name)    # return to previous menu


#------------------------------------------------------------------ASk for type of loan----------------------------------------------------------------------

def available_loan_types(): # shows avalilable loans and asks users to choose loans
    print("\nChoose types of Loan:\n")
    loan_lst = ["1. Press 1 for Education Loan ","2. Press 2 for Car Loan ","3. Press 3 for Home Loan","4. Press 4 for Personal Loan"]
    for types in loan_lst:
        print(f'  {types}')
    while True:
        try:
            ch = int(input("\n>>> "))
        except ValueError:
            print("Number input are only acceptable !!!")
            available_loan_types()      
        else:
            if ch == 1:
                return 'Education Loan'              
            elif ch == 2:
                return 'Car Loan'
            elif ch == 3:
                return 'Home Loan'
            elif ch == 4:
                return 'Personal Loan'
#------------------------------------------------------------------View transaction for customer----------------------------------------------------------------------


def customer_view_their_loan(usr_name):
    loan_details = read_file_data('all_loan_data.txt','r+')
    title = ['Loan Id','Username','Loan Types','Applied Loan Amt','Loan Tenure','Loan Rate','Installment Amount','Due Amount']
    table_data = []
    for loan_data in loan_details:
        if usr_name == loan_data[2]:
            titled_data = loan_data[1],loan_data[2],loan_data[4],loan_data[5],loan_data[6]+' years',loan_data[7] +' %',loan_data[8],loan_data[9]
            table_data.append(titled_data)
    print(tabulate.tabulate(table_data, headers=title,tablefmt="github"))   # printing loan details of the user in table with tabulate module

#------------------------------------------------------------------Pay loan installment----------------------------------------------------------------------

def installment_loan_pay(usr_name): # loan installment payment
    customer_view_their_loan(usr_name)
    loan_details = read_file_data('all_loan_data.txt','r')
    for loan_data in loan_details:
        if usr_name == loan_data[2]:
            loan_id = input("\nEnter loan id: ")
            if loan_id == loan_data[1]:
                pay_installment = input(f"\nDo you want to pay montly installment of {loan_data[4]} (y/n) ?")
        
                if pay_installment == 'y':
                    total_loan_amt_to_pay = str(float(loan_data[9]) - float(loan_data[8]))
                    loan_data[9] = total_loan_amt_to_pay
                    print(f"{usr_name}, Rs.{loan_data[8]} installment amount has been paid successfully...")
                else:
                    reg_customer_menu(usr_name)
            break

    with open('all_loan_data.txt','w') as file:
        for ele in loan_details:
            ele = ','.join(ele)
            file.write(ele+'\n') 
    goto_customer_menu(usr_name)
#------------------------------------------------------------------Status of loan----------------------------------------------------------------------

def status_of_loan(usr_name):
    loan_details = read_file_data('all_loan_data.txt','r') # calling read_file_data
    for loan_data in loan_details:
        if usr_name in loan_data:   # checking userid and if it finds, functions other task on the vary line
            print(f"\n-----------Loan Details-------------\n")
            print(f"Username : {loan_data[2]}")
            print(f"Loan ID : {loan_data[1]}")
            print(f"Types of Loan: {loan_data[4]}")
            print(f"Applied Loan Amount : Rs.{loan_data[5]}")
            print(f"Rate for Loan Amount : {loan_data[7]}%")
            print(f"Loan Tenure: {loan_data[6]} years")
            print(f"Date of Loan Applied : {loan_data[0]}")
            print(f"Installment Date : {loan_data[3]}")
            print(f"Total loan amount to pay: Rs.{loan_data[9]}")
            print(f"Monthly Installment Amount : Rs.{loan_data[8]}\n")
            goto_customer_menu(usr_name)

def goto_customer_menu(usr_name):
    inp_user = input("\nDo you want to go back to previous menu (y/n)?")
    if inp_user == 'y':
        reg_customer_menu(usr_name)
    else: 
        sys.exit()
#------------------------------------------------------------------Reading file data function----------------------------------------------------------------------

def read_file_data(filename, mode):
    #taking filename and mode both as a parameter in function 
    with open(filename, mode) as r:
        content = r.read()
        content = content.split('\n')  #split the data of file by \n
        datalist = []

        for data in content:
            data = data.split(',') #splittig content by ,
            datalist.append(data)
        datalist.pop(-1)#removing empty list
    return datalist 
#------------------------------------------------------------------Main Menu----------------------------------------------------------------------

def main_menu():
    print("\n           *******************Welcome To***************************")
    print("\n            Malaysia Bank Online Loan Management System (MBOLMS) \n")
    while True:
        try:
            print("""
      ******************************Main Menu**************************************\n  
                1. Admin                    (Press 1 to select this option)
                2. New Customer             (Press 2 to select this option)
                3. Registered Customer      (Press 3 to select this option)        
                4. Exit                     (Press 4 to select this option)
            """)
            system_users = int(input("Select your login method from the following (Press 1-4): "))
            print()

            if system_users == 1: # Admin
                admin()

            elif system_users == 2: # New customer
                newcustomer()
                
            elif system_users == 3: # registered customer
                reg_customer_login()

            elif system_users == 4: 
                print("Progarm has been closed successfully.\n")
                sys.exit()
                
            else:
                print("You made the wrong choice. Please select the choice between 1-3 !!!\n\n")

        except ValueError:
            print("\nNumber input are only acceptable !!!\n")
main_menu()