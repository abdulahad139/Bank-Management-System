# importing all necessary modules and libraries
import pandas as pd
import random
from datetime import date
import os
from abc import abstractmethod, ABC
import glob

class CreateAccount:  # To create a new bank account
    def getCustomerInfo(self):
        self.customer_details_dict = {}  # collecting the information of the customer
        self.name = input("Enter your full name: ")
        self.address = input("Enter your Home Address: ")
        self.nationality = input("Enter your Nationality: ")
        print("Which Type of Account you want to open?\n1. Savings Account\n2. Checking Account\n3. Loan Account")
        type_ask = input("Your choice: ")
        if type_ask == "1":
            self.acc_type = "Saving"
        elif type_ask == "2":
            self.acc_type = "Checking"
        else:
            self.acc_type = "Loan"
        self.balance = 0  # initially setting balance to zero

    def customerDetails(self):
        self.gen_acc_number = random.randint(1000000, 9999999)  # generating account number
        if (self.acc_type == "Saving") or (self.acc_type == "Checking"):
            self.customer_details_dict = {"Account Holder":[self.name],"AccountType":[self.acc_type],
                                      "Balance":[self.balance], "Password":[self.password],"Phone Number":[self.phone],
                                       "CNIC":[int(self.cnic)],"Address":[self.address],"Nationality":[self.nationality]}
            df = pd.DataFrame(data=self.customer_details_dict)  # converting the data into data frame
            cr_acc_f = df.to_csv(f"{self.gen_acc_number}.csv",index=False)  # creating account file and saving data
        elif self.acc_type == "Loan":   # if customer is making loan account
            self.customer_details_dict = {"Account Holder": [self.name], "AccountType": [self.acc_type],
                                          "Balance": [self.balance],"Loan Duration":[0],"Remaining Interest":[0],"Password": [self.password],
                                          "Phone Number": [self.phone],
                                          "CNIC": [self.cnic], "Address": [self.address],
                                          "Nationality": [self.nationality]}
            df = pd.DataFrame(data=self.customer_details_dict)  # converting the data into data frame
            cr_acc_f = df.to_csv(f"{self.gen_acc_number}.csv", index=False)  # creating account file and saving data

    def register(self):  # register an account
        while True:
            self.cnic = input("Enter your 13 Digits CNIC number: ")
            if len(self.cnic) == 13:
                self.phone = input("Enter your Phone Number without initial zero :")
                self.password = input("Create a strong password greater than 7 characters: ")
                if len(self.phone) == 10:   # length of phone number
                    if len(self.password) > 7:  # length of password
                        self.customerDetails()
                        print("Account Created Successfully")
                        print(f'Your Account Number is {self.gen_acc_number}')
                        print("-------------------------------------------------")
                        break
                    else:
                        print("Password must be greater than 7 characters!")
                else:
                    print("Invalid phone number! Please enter 10 digit number")
            else:
                print("Please Enter valid CNIC number.")


class Account(ABC):  # class for main account and it is abstract class
    def __init__(self, acc_no, password, balance):
        self.balance = balance
        self.acc_no = acc_no
        self.password = password

    @staticmethod
    def updateBalance(account_no, newbalance):  # to update the balance in account
        file_r = pd.read_csv(f"{account_no}.csv",index_col=False)   # reading the csv data file
        file_r.loc[0,"Balance"] = int(newbalance)    # updating new balance
        file_r.to_csv(f"{account_no}.csv",index=False)  # writing the csv data file

    @staticmethod
    def Transaction(acc_no, trans_type, amount):  # saving transaction in account
        gen_trans_ID = random.randint(100, 999)    # generating transaction ID
        data2 = {"Date": [f'{date.today()}'], "Transaction Type": [trans_type],
                 "Amount": [amount], "Transaction ID": [gen_trans_ID]}
        df2 = pd.DataFrame(data2)   # making data frame of transaction
        cr = df2.to_csv(f'{acc_no}.csv', mode="a", header=True, index=False)   # saving information to file


    def transactionHistory(self):
        print("--------------------------------------------------")
        print("     -------Transaction History------")
        while True:
            try:
                if os.path.exists(f"{self.acc_no}.csv"):  # checking if file exist
                    condition = True
                else:
                    condition = False

                if condition == True:
                    # Set the display option to show all rows
                    pd.set_option('display.max_rows', None)
                    df = pd.read_csv(f"{self.acc_no}.csv", index_col=False, header=None)

                    # Check if the DataFrame has any rows from the second row onwards
                    if len(df) > 1 and len(df.iloc[2:]) > 0:
                        # If the DataFrame has rows from the second row onwards, print them
                        df.dropna(how='any', axis="columns", inplace=True)  # to remove columns containing null values
                        print(df.iloc[2:])
                    else:
                        # If the DataFrame is empty or has no rows from the second row onwards, print a message
                        print("This file has no transaction history.")
                    break

                else:
                    print("     You haven't made any Transactions.")
                    print("-----------------------------------------------")
            except Exception as e:
                print("Invalid Input :((", e)

    @abstractmethod
    def deposit(self):  # deposit amount in account
        pass    # implemented in subclass

    @abstractmethod
    def withDraw(self):  # to withdraw amount in account
        pass    # implemented in subclass


    def balanceEnquiry(self):  # to check the current balance in account
        print(f'Current Balance: {self.balance}')


class CheckingAccount(Account):
    def __init__(self, acc_no, password, balance):
        super().__init__(acc_no,password,balance)
        self.overdraft_fee = 500  # Overdraft fee
        self.credit_limit = 50000

    def deposit(self):  # deposit amount in account, implementation of abstractmethod
        while True:
            try:
                deposit_amount = int(input("Enter the amount you want to deposit: "))
                if deposit_amount > 0:
                    self.balance += deposit_amount
                    Account.updateBalance(self.acc_no, self.balance)  # updating the balance
                    Account.Transaction(self.acc_no, "Deposit", deposit_amount)  # updating the transaction history
                    print(f"Deposited {deposit_amount}Rs. New balance is {self.balance}Rs.")
                    print("Your Amount has been Deposited!")
                    break
                else:
                    print("please deposit some amount")
                    continue
            except ValueError:
                print("Invalid Input :((")
                continue

    def withDraw(self):     # withdraw amount from account, implementation of abstractmethod
        withdraw_amount = int(input("Enter withdraw amount: "))
        if self.balance < withdraw_amount:
            print("You dont have enough money in your account.")
            over_input = input("Do you want an overdraft amount (y/n): ").lower()
            if over_input == "y":
                if 0>self.balance>-50000 :  # if balance is in negative
                    amount = 50000-abs(self.balance)
                    print(f"You can withdraw amount till {amount}Rs and overdraft fee will be {self.overdraft_fee}Rs")
                    over_input_2 = input("Are you sure to withdraw (y/n): ").lower()
                    if over_input_2 == 'y':
                        if withdraw_amount <= amount:
                            self.balance = self.balance - withdraw_amount - self.overdraft_fee
                            Account.updateBalance(self.acc_no, self.balance)  # updating the balance
                            Account.Transaction(self.acc_no, "Withdraw",withdraw_amount)  # updating the transaction history
                            print("Overdraft  Amount Successfully.")
                            print(f"Withdraw {withdraw_amount}Rs. New balance is {self.balance}Rs.")
                            print("---------------------------------------------------------------")
                        else:
                            print(f"You have exceeded the withdraw limit, The withdraw amount should not be greater than {amount}Rs")
                            print("--------------------------------------------------------------------------------------------------")
                    else:
                        print("You haven't overdraft amount.")
                        print("------------------------------------")
                elif self.balance >0:
                    print(f"You can withdraw amount till 50000Rs and overdraft fee will be {self.overdraft_fee}Rs")
                    if withdraw_amount <= 50000:
                        self.balance = self.balance - withdraw_amount - self.overdraft_fee
                        Account.updateBalance(self.acc_no, self.balance)  # updating the balance
                        Account.Transaction(self.acc_no, "Withdraw", withdraw_amount)  # updating the transaction history
                        print(f"Withdraw {withdraw_amount}Rs. New balance is {self.balance}Rs.")
                    else:
                        print("You have exceeded the withdraw limit, The withdraw amount should not be greater than 50000Rs")
                        print("----------------------------------------------------------------------------------------------")
                else:
                    print("You are not eligible for overdraft. Plz clear your dues first")
                    print("---------------------------------------------------------------")

            elif over_input == "n":
                print("You haven't overdraft the amount.")
        else:
            self.balance -= withdraw_amount
            Account.updateBalance(self.acc_no, self.balance)  # updating the balance
            Account.Transaction(self.acc_no, "Withdraw", withdraw_amount)  # updating the transaction history
            print(f"Withdraw {withdraw_amount}Rs. New balance is {self.balance}Rs.")

    def sendMoney(self):
        while True:
            ask_acc_num = input("Enter Account number of Beneficiary: ")  # taking account number
            if os.path.exists(f"{ask_acc_num}.csv"):    # checking if file exist
                condition = True
            else:
                condition = False

            if condition == True:
                account2 = pd.read_csv(f'{ask_acc_num}.csv', index_col=False)  # reading the account file
                if account2.loc[0, "AccountType"] == "Checking":    # if its checking account
                    acc2Balance = int(account2.loc[0,"Balance"])
                    send_amount = int(input("Enter the amount You want to Transfer: "))
                    if self.balance > 0:
                        if send_amount <=self.balance:
                            self.balance -= send_amount
                            acc2Balance += send_amount
                            self.updateBalance(self.acc_no,self.balance)
                            self.Transaction(self.acc_no,"Money Transfer",send_amount)
                            self.updateBalance(ask_acc_num,acc2Balance)
                            self.Transaction(ask_acc_num,"Money Transfer",send_amount)
                            print("Transaction Successfull.")
                            print(f'Your remaining balance is now {self.balance}Rs')
                            print("_________________________________________________")
                            break
                        else:
                            print("You have insufficient balance to make this transaction.")
                            print("----------------------------------------------------------")
                    elif self.balance <= 0:
                        print("Your Balance is Zero. You cannot make this transaction.")
                        print("_________________________________________________________")
                        break

                else:
                    print("The account is not checking.You can Transfer only to other Checking Accounts.")
                    print("--------------------------------------------------------------------------------")
            else:
                print("No Account found on this account number.")
                print("-------------------------------------------")


    def balanceEnquiry(self):   # overriding method from account class
        print(f'Total Balance: {self.balance}Rs')

class SavingAccount(Account):
    def __init__(self, acc_no, password, balance):
        super().__init__(acc_no,password,balance)
        self.interest_rate = 0.1  # 10 %
        
    # To add Interest in Saving Accounts
    def add_interest(self):
        try:
            for file in glob.glob("*.csv"):  # Search for all CSV files in the current directory
                try:
                    with open(file, "r") as f:
                        if "Saving" in f.read():  # if its Saving Account File
                            df = pd.read_csv(file,index_col=False)
                            balance = int(df.loc[0,"Balance"])
                            interestamount = int(balance * self.interest_rate)
                            balance += interestamount
                            df.loc[0,"Balance"] = balance
                            df.to_csv(file,index=False)
                except:
                    continue
            
        except Exception as e:
            print("An error occurred:", e)

    def deposit(self):  # deposit amount in account, implementation of abstractmethod
        while True:
            try:
                deposit_amount = int(input("Enter the amount you want to deposit: "))
                if deposit_amount > 0:
                    self.balance += deposit_amount
                    self.updateBalance(self.acc_no, self.balance)   # updating the balance
                    self.Transaction(self.acc_no, "Deposit", deposit_amount)    # updating the transaction history
                    print(f"Deposited {deposit_amount}Rs. \nNew balance is {self.balance}Rs.")
                    break
                else:
                    print("please deposit some amount")
            except ValueError:
                print("Invalid input :((")

    def withDraw(self):  # to withdraw amount in account, implementation of abstractmethod
        withdraw_amount = int(input("Enter the amount you want to withdraw: "))
        if self.balance >= withdraw_amount: # if withdraw is less than balance
            self.balance -= withdraw_amount
            self.updateBalance(self.acc_no, self.balance)   # updating the balance
            self.Transaction(self.acc_no, "Withdraw", withdraw_amount)  # updating the transaction history
            print(f"Withdraw {withdraw_amount}Rs.\nNew balance is {self.balance}Rs.")
        else:
            print("Insufficient balance.")

    def balanceEnquiry(self):   # overriding method from account class
        print(f"Account : balance={self.balance}Rs, interest_rate={self.interest_rate}%")



class LoanAccount(Account):
    def __init__(self,acc_no,password,balance,duration,remaininginterest):
        super().__init__(acc_no,password,balance)
        self.interestRate = 0.09   # 9% annual interest rate
        self.loanDuration = duration    # initializing the loan duration
        self.principal_amount = 0   # initializing the principal amount
        self.remaining_interest = remaininginterest
    @staticmethod
    def updateDuration(accountnumber,duration):
        file_r = pd.read_csv(f"{accountnumber}.csv",index_col=False)   # reading the csv data file
        file_r.loc[0,"Loan Duration"] = int(duration)
        file_r.to_csv(f"{accountnumber}.csv",index=False)

    @staticmethod
    def updateTotalInterest(accountnumber, interestpay):    # to update remaining interest
        file_r = pd.read_csv(f"{accountnumber}.csv", index_col=False)  # reading the csv data file
        file_r.loc[0, "Remaining Interest"] = int(interestpay)
        file_r.to_csv(f"{accountnumber}.csv", index=False)

    def totalInterest(self,amount): # calculate total interest on principal amount
        self.total_interest = amount * self.interestRate
        return self.total_interest

    def calculateMonthlyInterest(self,duration):   # calculate monthly interest on total interest
        self.monthly_interest = self.total_interest / duration
        return self.monthly_interest

    def withDraw(self):
        if self.balance == 0:
            print('You are eligible for Loan')
            user = input("Do you want take loan (y/n): ")
            if user == "y":
                print("We have 3 types of loan\nThe Business loan____ a\nThe House loan____ b\nThe Car loan_____ c")
                user_0 = input("Enter your choice: ").lower()
                if user_0 == "a":
                    self.principal_amount = 1000000    # 10 lac
                    self.loanDuration = 20
                    self.totalinterest_payment = self.totalInterest(self.principal_amount)  # total interest on principal amount
                    self.totalmonthly_payment = self.calculateMonthlyInterest(self.loanDuration)    # total interest on monthly payment
                    self.total_1 = 50000 + int(self.totalmonthly_payment)
                    print(f"The Business loan we are providing is {self.principal_amount}Rs for Duration {self.loanDuration} months.")
                    print(f"The monthly payment will be {50000} + {self.totalmonthly_payment} = {self.total_1}")
                    user_1 = input("Are You sure to take loan(y/n): ").lower()
                    if user_1 == "y":
                        self.balance += 1000000
                        Account.updateBalance(self.acc_no, self.balance)  # updating the balance
                        LoanAccount.updateDuration(self.acc_no,self.loanDuration)   # updating the loan duration
                        Account.Transaction(self.acc_no, "Loan Taken", self.balance)  # updating the transaction history
                        LoanAccount.updateTotalInterest(self.acc_no,self.totalinterest_payment) # updating the remaining interest
                        print("You have Taken the Loan Successfully!!")
                        print("-----------------------------------------")
                    else:
                        print("You haven't Taken Business Loan!!")
                        print("-----------------------------------")
                elif user_0 == "b":
                    self.principal_amount= 2000000     # 20 lac
                    self.loanDuration = 40
                    self.totalinterest_payment = self.totalInterest(self.principal_amount)  # total interest on principal amount
                    self.totalmonthly_payment = self.calculateMonthlyInterest(self.loanDuration)  # total interest on monthly payment
                    self.total_2 = 50000 + int(self.totalmonthly_payment)
                    print(f"The House loan we are providing is {self.principal_amount}Rs for Duration {self.loanDuration}months.")
                    print(f"The monthly payment will be {50000} + {self.totalmonthly_payment} = {self.total_2}")
                    user_2 = input("Are You sure to take loan(y/n): ").lower()
                    if user_2 == "y":
                        self.balance += 2000000
                        Account.updateBalance(self.acc_no, self.balance)  # updating the balance
                        LoanAccount.updateDuration(self.acc_no, self.loanDuration)  # updating the loan duration
                        Account.Transaction(self.acc_no, "Loan Taken", self.balance)  # updating the transaction history
                        LoanAccount.updateTotalInterest(self.acc_no,self.totalinterest_payment)  # updating the remaining interest
                        print("You have Taken the Loan Successfully!!")
                        print("-----------------------------------------")
                    else:
                        print("You haven't Taken House Loan!!")
                        print("-----------------------------------")

                elif user_0 == "c":
                    self.principal_amount = 500000  # 5 lac
                    self.loanDuration = 10
                    self.totalinterest_payment = self.totalInterest(self.principal_amount)  # total interest on principal amount
                    self.totalmonthly_payment = self.calculateMonthlyInterest(self.loanDuration)  # total interest on monthly payment
                    self.total_3 = 50000 + int(self.totalmonthly_payment)
                    print(f"The Car loan we are providing is {self.principal_amount}Rs for Duration {self.loanDuration}months.")
                    print(f"The monthly payment will be {50000} + {self.totalmonthly_payment} = {self.total_3}")
                    user_3 = input("Are You sure to take loan(y/n): ").lower()
                    if user_3 == "y":
                        self.balance += 500000
                        Account.updateBalance(self.acc_no, self.balance)  # updating the balance
                        LoanAccount.updateDuration(self.acc_no, self.loanDuration)  # updating the loan duration
                        Account.Transaction(self.acc_no, "Loan Taken", self.balance)  # updating the transaction history
                        LoanAccount.updateTotalInterest(self.acc_no,self.totalinterest_payment)  # updating the remaining interest
                        print("You have Taken the Loan Successfully!!")
                        print("-----------------------------------------")
                    else:
                        print("You haven't Taken CarLoan!!")
                        print("-----------------------------------")
        elif self.balance > 0:  # if there is some loan left to be paid off
            print("You have already taken loan. First pay off the previous loan.")
            print("________________________________________________________________")

    def deposit(self):
        if self.balance > 0:
            print("Which Type of Loan have You taken?\nThe Business Loan___a\nThe House Loan___b\nThe Car Loan___c")
            user = input("Enter which loan you have taken (a/b/c): ").lower()
            if user == "a":
                while True:
                    print("You had taken Business Loan!!")
                    print(f"First You have to pay Rs 4,500 as Interest Amount")
                    interest_amount = int(input("Enter interest Amount in Numbers: "))
                    if interest_amount == 4500:
                        print("Pay Your Fixed Monthly Amount of Fifty Thousand Rupees Only")
                        user_0 = int(input("Enter amount in numbers: "))
                        if user_0 == 50000:
                            self.balance -= 50000
                            self.loanDuration -= 1
                            self.remaining_interest -= interest_amount
                            Account.updateBalance(self.acc_no, self.balance)  # updating the balance
                            Account.Transaction(self.acc_no, "Loan paid back", self.balance)  # updating the transaction history
                            LoanAccount.updateDuration(self.acc_no, self.loanDuration)  # updating the loan duration
                            LoanAccount.updateTotalInterest(self.acc_no,self.remaining_interest)  # updating the remaining interest
                            print("You have successfully paid the amount!")
                            print("----------------------------------------")
                            break
                        else:
                            print("Please provide the complete payment.")
                            print("------------------------------------------")
                            continue
                    else:
                        print("Please provide the complete payment.")
                        print("------------------------------------------")
                        continue

            elif user == "b":
                while True:
                    print("You had taken House Loan!!")
                    print(f"First You have to pay Rs 4,500 as Interest Amount")
                    interest_amount = int(input("Enter interest Amount in Numbers: "))
                    if interest_amount == 4500:
                        print("Pay Your Fixed Monthly Amount of Fifty Thousand Rupees Only")
                        user_1 = int(input("Enter amount in numbers: "))
                        if user_1 == 50000:
                            self.balance -= 50000
                            self.loanDuration -= 1
                            self.remaining_interest -= interest_amount
                            Account.updateBalance(self.acc_no, self.balance)  # updating the balance
                            Account.Transaction(self.acc_no, "Loan paid back", self.balance)  # updating the transaction history
                            LoanAccount.updateDuration(self.acc_no, self.loanDuration)  # updating the loan duration
                            LoanAccount.updateTotalInterest(self.acc_no,self.remaining_interest)  # updating the remaining interest
                            print("You have successfully paid the amount!")
                            print("----------------------------------------")
                            break
                        else:
                            print("Please provide the complete payment.")
                            print("------------------------------------------")
                            continue
                    else:
                        print("Please provide the complete payment.")
                        print("------------------------------------------")
                        continue

            elif user == "c":
                while True:
                    print("You had Car Loan!!")
                    print(f"First You have to pay Rs 4,500 as Interest Amount")
                    interest_amount = int(input("Enter interest Amount in Numbers: "))
                    if interest_amount == 4500:
                        print("Pay Your Fixed Monthly Amount of Fifty Thousand Rupees Only")
                        user_2 = int(input("Enter Amount in Numbers: "))
                        if user_2 == 50000:
                            self.balance -= 50000
                            Account.updateBalance(self.acc_no, self.balance)  # updating the balance
                            Account.Transaction(self.acc_no, "Loan paid back", self.balance)  # updating the transaction history
                            self.loanDuration -= 1
                            self.remaining_interest -= interest_amount
                            LoanAccount.updateDuration(self.acc_no, self.loanDuration)  # updating the loan duration
                            LoanAccount.updateTotalInterest(self.acc_no,self.remaining_interest)  # updating the remaining interest
                            print("You have successfully paid the amount!")
                            print("----------------------------------------")
                            break
                        else:
                            print("Please provide the complete payment.")
                            print("------------------------------------------")
                            continue
                    else:
                        print("Please provide the complete payment.")
                        print("------------------------------------------")
                        continue

        elif self.balance == 0:
            print("Your Loan Balance is zero!!")
            print("-------------------------------")



class Customer:
    def welcomeInterface(self):  # Starting interface
        print("What do you want to do ?")
        print("Create an account------------1\nLogin to existing Account----2\nPress any other key to exit Customer Interface.")

    @staticmethod
    def checkingCustomerAccounts():
        # we first check if customer already has account in the bank and how many accounts the customer has
         while True:
            try:
                cnic = input("Enter the 13 digits CNIC number: ")
                if len(cnic) == 13:
                    found_files = []

                    for file in glob.glob("*.csv"):  # Search for all CSV files in the current directory
                        try:
                            with open(file, "r") as f:
                                if cnic in f.read():   # if given cnic is present in file
                                    df = pd.read_csv(file)
                                    name = df.loc[0, "Account Holder"]
                                    account_type = df.loc[0, "AccountType"]
                                    account_number = file.split(".")[0]
                                    account_info = f"The account number is {account_number}. The account holder's name is {name} and the account type is {account_type}."
                                    found_files.append(account_info)

                        except:
                            continue

                    if found_files:
                        for accounts in found_files:
                            print(accounts)
                        break
                    else:
                        print("No account found on this CNIC")
                        print("--------------------------------")
                else:
                    print("Please enter valid CNIC.")
            except Exception as e:
                print("An error occurred:", e)

    def userLoggin(self):
        while True:
            ask_acc_num = input("Enter Account number You want to Login: ")  # taking account number
            ask_pass = input("Enter the password: ")  # taking password
            if os.path.exists(f"{ask_acc_num}.csv"):    # checking if file exist
                condition = True
            else:
                condition = False

            if condition == True:
                f = pd.read_csv(f'{ask_acc_num}.csv', index_col=False)  # reading the account file
                if f.loc[0, "Password"] == ask_pass:    # checking password
                    print("----------------------------------------")
                    print("You are successfully logged in")
                    print("-----------------------------------------")

                    if f.loc[0,"AccountType"] == "Checking":    # for current account
                        balance = int(f.loc[0, "Balance"])  # taking balance from file
                        currentObj = CheckingAccount(ask_acc_num,ask_pass,balance)   # composition of CurrentAccount class
                        while True:
                            print("Account Type: Checking Account")
                            print("1. Check Balance     2. Deposit      3. Withdraw money   4. Send Money   5. Transaction History")
                            ask_opt = input("Your Choice: ")  # taking choice of user
                            if ask_opt == "1":
                                currentObj.balanceEnquiry()  # to check current balance of account
                                print("\n1.Back To Main Menu")
                                print("2.Logout")
                                choose = input()
                                if choose == "1":
                                    continue
                                elif choose == "2":
                                    print("You have been logged out")
                                    print("___________________________")
                                    break
                                else:
                                    continue
                            elif ask_opt == "2":
                                currentObj.deposit()  # to deposit money in account
                                print("\n1.Back To Main Menu")
                                print("2.Logout")
                                choose = input()
                                if choose == "1":
                                    continue
                                elif choose == "2":
                                    print("You have been logged out")
                                    print("___________________________")
                                    break
                                else:
                                    continue
                            elif ask_opt == "3":
                                currentObj.withDraw()  # to withdraw money from account
                                print("\n1.Back To Main Menu")
                                print("2.Logout")
                                choose = input()
                                if choose == "1":
                                    continue
                                elif choose == "2":
                                    print("You have been logged out")
                                    print("___________________________")
                                    break
                                else:
                                    continue
                            elif ask_opt == "4":
                                currentObj.sendMoney()
                                print("\n1.Back To Main Menu")
                                print("2.Logout")
                                choose = input()
                                if choose == "1":
                                    continue
                                elif choose == "2":
                                    print("You have been logged out")
                                    print("___________________________")
                                    break
                                else:
                                    continue

                            elif ask_opt == "5":
                                currentObj.transactionHistory()
                                print("\n1.Back To Main Menu")
                                print("2.Logout")
                                choose = input()
                                if choose == "1":
                                    continue
                                elif choose == "2":
                                    print("You have been logged out")
                                    print("___________________________")
                                    break
                                else:
                                    continue

                    elif f.loc[0,"AccountType"] == "Saving":   # for saving account
                        balance = int(f.loc[0, "Balance"])  # taking balance from file
                        savingObj = SavingAccount(ask_acc_num,ask_pass,balance) # composition of SavingAccount class
                        

                        while True:
                            print("Account Type: Saving")
                            print("1. Check Balance     2. Deposit      3. Withdraw money     4. Transaction History")
                            ask_opt = input("Your Choice: ") # taking choice of user
                            if ask_opt == "1":
                                savingObj.balanceEnquiry()  # to check current balance of account
                                print("\n1.Back To Main Menu")
                                print("2.Logout")
                                choose = input()
                                if choose == "1":
                                    continue
                                elif choose == "2":
                                    print("You have been logged out")
                                    print("___________________________")
                                    break
                                else:
                                    continue
                            elif ask_opt == "2":
                                savingObj.deposit()  # to deposit money in account
                                print("\n1.Back To Main Menu")
                                print("2.Logout")
                                choose = input()
                                if choose == "1":
                                    continue
                                elif choose == "2":
                                    print("You have been logged out")
                                    print("___________________________")
                                    break
                                else:
                                    continue
                            elif ask_opt == "3":
                                savingObj.withDraw()  # to withdraw money from account
                                print("\n1.Back To Main Menu")
                                print("2.Logout")
                                choose = input()
                                if choose == "1":
                                    continue
                                elif choose == "2":
                                    print("You have been logged out")
                                    print("___________________________")
                                    break
                                else:
                                    continue
                            elif ask_opt == "4":
                                savingObj.transactionHistory()
                                print("\n1.Back To Main Menu")
                                print("2.Logout")
                                choose = input()
                                if choose == "1":
                                    continue
                                elif choose == "2":
                                    print("You have been logged out")
                                    print("___________________________")
                                    break
                                else:
                                    continue

                    if f.loc[0,"AccountType"] == "Loan":    # for loan account
                        balance = int(f.loc[0, "Balance"])  # taking balance from file
                        loan_duration = int(f.loc[0,"Loan Duration"]) # fetching loan duration
                        remaining_interest = int(f.loc[0,"Remaining Interest"])
                        loanObj = LoanAccount(ask_acc_num,ask_pass,balance,loan_duration,remaining_interest)   # composition of Loan Account class
                        while True:
                            print("Account Type: Loan Account")
                            print("1. Check loan Balance     2. Pay Your loan      3. Get Loan  4. Transaction History")
                            ask_opt = input("Your Choice: ")  # taking choice of user
                            if ask_opt == "1":
                                loanObj.balanceEnquiry()  # to check current balance of account
                                print("\n1.Back To Main Menu")
                                print("2.Logout")
                                choose = input()
                                if choose == "1":
                                    continue
                                elif choose == "2":
                                    print("You have been logged out")
                                    print("___________________________")
                                    break
                                else:
                                    continue
                            elif ask_opt == "2":
                                loanObj.deposit()  # to pay back loan money
                                print("\n1.Back To Main Menu")
                                print("2.Logout")
                                choose = input()
                                if choose == "1":
                                    continue
                                elif choose == "2":
                                    print("You have been logged out")
                                    print("___________________________")
                                    break
                                else:
                                    continue
                            elif ask_opt == "3":
                                loanObj.withDraw()  # to get loan from bank
                                print("\n1.Back To Main Menu")
                                print("2.Logout")
                                choose = input()
                                if choose == "1":
                                    continue
                                elif choose == "2":
                                    print("You have been logged out")
                                    print("___________________________")
                                    break
                                else:
                                    continue
                            elif ask_opt == "4":
                                loanObj.transactionHistory()
                                print("\n1.Back To Main Menu")
                                print("2.Logout")
                                choose = input()
                                if choose == "1":
                                    continue
                                elif choose == "2":
                                    print("You have been logged out")
                                    print("___________________________")
                                    break
                                else:
                                    continue

                    break
                else:
                    print("The password you enter is incorrect")
            else:
                print("the account number you entered is invalid ")

class Admin:
    @staticmethod
    def customerInformation():
        # we first check if customer already has account in the bank and how many accounts the customer has
        try:
            cnic = input("Enter the 13 digits CNIC number: ")
            if len(cnic) == 13:
                found_files = []

                for file in glob.glob("*.csv"):  # Search for all CSV files in the current directory
                    try:
                        with open(file, "r") as f:
                            if cnic in f.read():  # if given cnic is present in file
                                df = pd.read_csv(file)
                                name = df.loc[0, "Account Holder"]
                                account_type = df.loc[0, "AccountType"]
                                account_number = file.split(".")[0]
                                account_info = f"The account number is {account_number}. The account holder's name is {name} and the account type is {account_type}."
                                found_files.append(account_info)
                    except:
                        continue

                if found_files:
                    for accounts in found_files:
                        print(accounts)
                        print("_________________________________________________________________________________")
                else:
                    print("No account found on this CNIC")
                    print("_________________________________")
            else:
                print("Please Enter the valid CNIC number.")
        except Exception as e:
            print("An error occurred:", e)

    @staticmethod
    def customerDetailInfo():
        # we have to check necessary details about the account holder
        print("--------------------------------------------------")
        print("Enter Account Number Of Customer to show details")
        while True:
            try:
                ask_customeraccno = int(input("Account Number: "))
                if os.path.exists(f"{ask_customeraccno}.csv"):  # checking if file exist
                    condition = True
                else:
                    condition = False

                if condition == True:
                    f = pd.read_csv(f"{ask_customeraccno}.csv",index_col=False)
                    name = f.loc[0, "Account Holder"]
                    account_type = f.loc[0, "AccountType"]
                    balance = f.loc[0,"Balance"]
                    CNIC = f.loc[0,"CNIC"]
                    print(f"Account Holder: {name}")
                    print(f"Account Type: {account_type}")
                    print(f"Balance: {balance}")
                    print(f"CNIC: {CNIC}")
                    if account_type == "Loan":
                        loan_duration = f.loc[0,"Loan Duration"]
                        print(f"Loan Duration: {loan_duration}")
                    print("_________________________________________")
                    break
                else:
                    print("No account has Found on given Account Number")
                    print("-----------------------------------------------")
            except:
                print("Invalid Input :((")
    @staticmethod
    def seeTransaction():
        print("--------------------------------------------------")
        print("Enter Account Number Of Customer to show Transaction History.")
        while True:
            try:
                ask_customeraccno = int(input("Account Number: "))
                if os.path.exists(f"{ask_customeraccno}.csv"):  # checking if file exist
                    condition = True
                else:
                    condition = False

                if condition == True:
                    # Set the display option to show all rows
                    pd.set_option('display.max_rows', None)
                    df = pd.read_csv(f"{ask_customeraccno}.csv",index_col=False,header=None)

                    # Check if the DataFrame has any rows from the second row onwards
                    if len(df) > 1 and len(df.iloc[2:]) > 0:
                        # If the DataFrame has rows from the second row onwards, print them
                        df.dropna(how='any', axis="columns", inplace=True)  # to remove columns containing null values
                        print(df.iloc[2:])
                        print("_____________________________________________________________")
                    else:
                        # If the DataFrame is empty or has no rows from the second row onwards, print a message
                        print("This file has no transaction history.")
                        print("_____________________________________________")
                    break

                else:
                    print("No account has Found on given Account Number")
                    print("-----------------------------------------------")
            except Exception as e:
                print("Invalid Input :((",e)
    @staticmethod
    def removeAccount():
        try:
            print("Enter the Account Number to Delete the Account.")
            ask_accno = int(input("Account Number: "))
            if os.path.exists(f"{ask_accno}.csv"):  # checking if file exist
                condition = True
            else:
                condition = False

            if condition == True:
                os.remove(f"{ask_accno}.csv")
                print("Account has been Removed!!!")
                print("__________________________________")
            else:
                print("No account has Found on given Account Number")
                print("-----------------------------------------------")
        except Exception as e:
            print("Invalid Input :((",e)

    def admin(self):
        pass_file = open("AdminPassword.txt")  # opening password file
        self.password = pass_file.read()  # converting password into list
        print("This side is for Administrators. Access is restricted to authorised individuals only.")
        while True:
            print("Enter Adminitrator Password or Press 0 to Exit")
            ps = input("\nAdministrator Password: ")  # asking password from admin
            if ps == self.password:  # checking the entered password
                print("--------------------------")
                print("LOGIN SUCCESSFUL!")
                print("--------------------------")
                print("Welcome Admin")
                while True:
                    print("See Customer Accounts ---- A\n"
                        "See Account Details-------B\n"
                        "See Transaction History - C\n"
                        "Delete Account ---------- D\n"
                        "Add Interest To Saving Accounts--E\n"
                        "Exit -------------------- 0")
                    ask_admin = input("Your Choice: ").upper()
                    if ask_admin == "A":
                        print("Enter the CNIC (without dashes) of the person whose account information you would like to see!")
                        Admin.customerInformation()     # to check number of accounts a customer has
                        print("\n1.Back To Main Menu")
                        print("2.Exit From ADMIN")
                        choose = input()
                        if choose == "1":
                            continue
                        elif choose == "2":
                            print("You have been logged out")
                            print("___________________________")
                            break
                        else:
                            continue

                    elif ask_admin == "B":
                        Admin.customerDetailInfo()    # to check account details
                        print("\n1.Back To Main Menu")
                        print("2.Exit From ADMIN")
                        choose = input()
                        if choose == "1":
                            continue
                        elif choose == "2":
                            print("You have been logged out")
                            print("___________________________")
                            break
                        else:
                            continue
                    elif ask_admin == "C":
                        Admin.seeTransaction()
                        print("\n1.Back To Main Menu")
                        print("2.Exit From ADMIN")
                        choose = input()
                        if choose == "1":
                            continue
                        elif choose == "2":
                            print("You have been logged out")
                            print("___________________________")
                            break
                        else:
                            continue
                    elif ask_admin == "D":
                        Admin.removeAccount()
                        print("\n1.Back To Main Menu")
                        print("2.Exit From ADMIN")
                        choose = input()
                        if choose == "1":
                            continue
                        elif choose == "2":
                            print("You have been logged out")
                            print("___________________________")
                            break
                        else:
                            continue
                    elif ask_admin == "E":
                        objsaving = SavingAccount(000,0,0)
                        objsaving.add_interest()    # add interest to all savings accounts
                        print("Interest Has been credited to all Saving accounts")
                        print("\n1.Back To Main Menu")
                        print("2.Exit From ADMIN")
                        choose = input()
                        if choose == "1":
                            continue
                        elif choose == "2":
                            print("You have been logged out")
                            print("___________________________")
                            break
                        else:
                            continue

                    elif ask_admin == "0":
                        print("You have been Logged out!!")
                        print("___________________________")
                        quit()
            elif ps == "0": # to exit the admin interface
                print("Exited!!")
                print("___________________________")
                break
            else:
                print("Incorrect Password! Try Again or Press '0' to Exit the Program")
                print("_________________________________________________________________")
                continue

class Interface:
    def __init__(self):
        print("                                                      *********************************")
        print("                                                      * Welcome To Super Bank Limited *")
        print("                                                      *********************************")
        print()
        print()
        print()
        user = input("                                                          Enter c to continue:- ").lower()
        if user == "c":
            print()
            print()
            print( "                              **************************** SUPER BANK LIMITED ****************************")
            print()
            print("Administrator Options --- A")
            print("Customer Options -------- B")
            print("Exit -----------------Press any key")
            ask = input("Your Choice: ").upper()
            if ask == "A":
                self.admin_interface()
            elif ask == "B":
                self.customer_interface()
            else:
                quit()

    def admin_interface(self):
        adminobj = Admin()  # composition of Admin Class
        adminobj.admin()

    def customer_interface(self):
        while True:
            customerobject = Customer()   # composition of customer class because it is responsible to interact with the customer
            customerobject.welcomeInterface()   # to print options for customer
            ask_customer = int(input("Your Choice: "))
            if ask_customer == 1:
                obj_cr_acc = CreateAccount()   # composition of Create Account class
                obj_cr_acc.getCustomerInfo()
                obj_cr_acc.register()
                print("\n1.Back To Main Menu")
                print("2.Press any key To Exit")
                choose = input()
                if choose == "1":
                    continue
                else:
                    print("Exited!!!")
                    print("___________________________")
                    break
            elif ask_customer == 2:
                customerobject.checkingCustomerAccounts()
                customerobject.userLoggin()
                print("\n1.Back To Main Menu")
                print("2.Press any key To Exit")
                choose = input()
                if choose == "1":
                    continue
                else:
                    print("Exited!!!")
                    print("___________________________")
                    break
            else:
                break


obj = Interface()
