from AccountObj import Account

class SavingsAccount(Account):
    def __init__(self, name, balance, interest_rate):
        super().__init__(name, balance)
        self._interest_rate = interest_rate

    def calculate_interest(self):
        return self._interest_rate

    def deposit(self, amt):
        self._balance += amt
        print("You have deposited €{0}".format(amt))
        print("New balance is €{0:.2f}".format(self.get_acc_balance()))
        interest = self.get_acc_balance() * self.calculate_interest()/100
        print("Interest earned: {0:.2f}".format(interest))
        super().deposit(interest)



