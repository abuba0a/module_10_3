import threading
from threading import Thread, Lock
import time
from random import randint


class Bank:

    def __init__(self):
        self.lock = Lock()
        self.balance = 0

    def deposit(self):
        for i in range(100):
            replenish = randint(50, 500)
            self.balance += replenish
            print(f'Пополнение: {replenish}. Баланс: {self.balance}.')
            time.sleep(.001)
            if self.balance >= 500 and self.lock.locked():
                self.lock.release()
            time.sleep(.001)

    def take(self):
        for i in range(100):
            reduce = randint(50, 500)
            print(f'Запрос на {reduce}')
            time.sleep(.001)
            if reduce <= self.balance:
                self.balance -= reduce
                print(f'Снятие: {reduce}. Баланс: {self.balance}')

            else:
                print(f'Запрос отклонён, недостаточно средств')
                self.lock.acquire()
            time.sleep(.001)


bk = Bank()

th1 = threading.Thread(target=Bank.deposit, args=(bk,))
th2 = threading.Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()
th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')
