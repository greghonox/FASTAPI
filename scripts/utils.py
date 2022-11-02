from time import sleep
from random import choice

def choices() -> bool:
    ops = [True, False]
    print('INICIANDO ESCOLHA')
    sleep(5)
    choic = choice(ops)
    print(f'ESCOLHA FEITA {choic}')
    return choic
    