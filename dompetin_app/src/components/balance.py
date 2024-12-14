import flet as ft
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List
import json
import random

@dataclass
class Balance:
    amount: float


class BalanceController:
    def __init__(self, page: ft.Page):
        self.page = page
        # Load balance dari client storage
        self.balance = self._load_balance()

    def _load_balance(self) -> Balance:
        """Load balance dari client storage."""
        balance_data = self.page.client_storage.get("balance")
        if balance_data:
            balance_data = json.loads(balance_data)
            return Balance(**balance_data)
        return Balance(0.0)

    def _save_balance(self):
        """Simpan balance ke client storage."""
        self.page.client_storage.set(
            "balance",
            json.dumps(asdict(self.balance))
        )

    def get_balance(self) -> float:
        return self.balance.amount

    
    def decrease_balance(self, amount:float):
        current = self.get_balance()
        self.balance.amount = current - amount
        self._save_balance()
    
    def increase_balance(self, amount:float):
        current = self.get_balance()
        self.balance.amount = current + amount
        self._save_balance()

    def display_balance(self):
        balance = self.get_balance()
        return ft.Text(f"Rp. {'{:,.2f}'.format(balance).replace(',', 'X').replace('.', ',').replace('X', '.')}",size=20)
    
    def set_balance(self, amount: float):
        self.balance.amount = amount
        self._save_balance()
    
    def edit_balance(self, amount: float):
        self.balance.amount = amount
        self._save_balance()
