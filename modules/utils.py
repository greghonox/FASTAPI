from time import sleep
from random import choice

TEMP = 1

def choices() -> bool:
    ops = [True, False]
    print('INICIANDO ESCOLHA')
    sleep(TEMP)
    choic = choice(ops)
    print(f'ESCOLHA FEITA {choic}')
    return choic