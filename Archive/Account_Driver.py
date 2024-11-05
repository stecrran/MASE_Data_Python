from AccountObj import Account
from SavingsAccountObj import SavingsAccount

def main():
    account1 = Account("Harry Potter", 1000)
    account1.deposit(500)
    account1.withdraw(200)
    print("Account check-------------------")
    account1.account_info()

    print("\n")
    account2 = SavingsAccount("Herm Granger", 500, 2.5)
    account2.deposit(250)
    account2.calculate_interest()
    print("Account check-------------------")
    account2.account_info()

if __name__ == "__main__":
    main()