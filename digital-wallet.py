import uuid
import datetime

class Transaction:
    """Represents a single financial activity inside a wallet."""
    
    def __init__(self, action_type, amount, note=""):
        self.tx_id = str(uuid.uuid4())[:8]
        self.action = action_type   # deposit, withdrawal, send, receive
        self.amount = amount
        self.note = note
        self.time = datetime.datetime.now()

    def __str__(self):
        return (f"[{self.time}] {self.action.upper()} | "
                f"Amount: {self.amount} | {self.note} | TX-ID: {self.tx_id}")


class Wallet:
    """Digital wallet for a user with balance tracking and history."""
    
    def __init__(self, owner_name):
        self.owner = owner_name
        self.balance = 0.0
        self.history = []

    def deposit(self, amount):
        if amount <= 0:
            print(" Invalid amount. Please enter a positive value.")
            return
        self.balance += amount
        self.history.append(Transaction("deposit", amount))
        print(f" ${amount:.2f} added to {self.owner}'s wallet.")

    def withdraw(self, amount):
        if amount <= 0:
            print(" Invalid amount. Please enter a positive value.")
            return
        if amount > self.balance:
            print(" Withdrawal failed. Not enough funds.")
            return
        self.balance -= amount
        self.history.append(Transaction("withdrawal", amount))
        print(f" ${amount:.2f} withdrawn from {self.owner}'s wallet.")

    def transfer(self, amount, receiver):
        if amount <= 0:
            print(" Transfer amount must be positive.")
            return
        if amount > self.balance:
            print(" Transfer failed. Insufficient balance.")
            return

        # Reduce amount from sender
        self.balance -= amount
        self.history.append(Transaction("send", amount, f"Sent to {receiver.owner}"))

        # Add to receiver
        receiver.balance += amount
        receiver.history.append(Transaction("receive", amount, f"Received from {self.owner}"))

        print(f" ${amount:.2f} successfully sent to {receiver.owner}.")

    def show_balance(self):
        print(f"\n {self.owner}'s Current Balance: ${self.balance:.2f}\n")

    def show_history(self):
        print(f"\n Transaction Log for {self.owner}:")
        if not self.history:
            print("   No transactions yet.")
        for entry in self.history:
            print(" -", entry)
        print()


# ---------------------------------------------------------
# Command Line Interface
# ---------------------------------------------------------

def main():
    print("===== DIGITAL WALLET SYSTEM =====")

    # Create user wallets
    name1 = input("Enter name for first wallet: ")
    name2 = input("Enter name for second wallet: ")

    wallet1 = Wallet(name1)
    wallet2 = Wallet(name2)

    wallets = {"1": wallet1, "2": wallet2}

    while True:
        print("""
Select an option:
1 - Add Money
2 - Withdraw Money
3 - Send Money
4 - View Balance
5 - View Transaction History
6 - Exit
        """)

        choice = input("Your choice: ")

        if choice == "1":
            w = wallets.get(input("Choose wallet (1 or 2): "))
            amount = float(input("Enter deposit amount: "))
            w.deposit(amount)

        elif choice == "2":
            w = wallets.get(input("Choose wallet (1 or 2): "))
            amount = float(input("Enter withdrawal amount: "))
            w.withdraw(amount)

        elif choice == "3":
            sender = wallets.get(input("Sender wallet (1 or 2): "))
            receiver = wallets.get(input("Receiver wallet (1 or 2): "))
            amount = float(input("Enter transfer amount: "))
            sender.transfer(amount, receiver)

        elif choice == "4":
            w = wallets.get(input("Choose wallet (1 or 2): "))
            w.show_balance()

        elif choice == "5":
            w = wallets.get(input("Choose wallet (1 or 2): "))
            w.show_history()

        elif choice == "6":
            print(" Exiting program. Have a great day!")
            break

        else:
            print(" Invalid selection. Please try again.")


if __name__ == "__main__":
    main()
