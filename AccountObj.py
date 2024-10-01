class Account:
    def __init__(self, name, balance):
        self._name = name
        self._balance = balance
        print("Account was successfully created.")
        print("Name: {0}\tBalance: {1}".format(name, balance))
        #account_info()


    def account_info(self):
        print("Name: {0}".format(self._name))
        print("Balance: {0:.2f}".format(self._balance))


    def get_acc_name(self):
        return self._name


    def get_acc_balance(self):
        return self._balance


    def set_balance(self, new_balance):
        self._balance = new_balance

    def deposit(self, amt):
        self._balance += amt
        print("You have deposited €{0}".format(amt))
        print("New balance is €{0:.2f}".format(self.get_acc_balance()))

    def withdraw(self, amt):
        if self._balance <= 0 or amt >= self._balance:
            print("You have insufficient funds. Your balance is {0:.2f}".format(self.get_acc_balance()))
        else:
            self._balance -= amt
            print("€{0} - Withdrawn, your new balance is €{1:.2f}".format(amt, self.get_acc_balance()))



