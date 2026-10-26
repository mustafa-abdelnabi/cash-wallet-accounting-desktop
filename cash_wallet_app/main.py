import tkinter as tk

from cash_wallet_app.app import CashWalletApp


def main() -> None:
    root = tk.Tk()
    CashWalletApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
