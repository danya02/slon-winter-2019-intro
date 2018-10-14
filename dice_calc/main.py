#!/usr/bin/python3
import random
import re
import time

pedantic = True # disable to be able to use any expression with d-notation
verbose = True

def printv(*args):
    if verbose:
        print(*args)


def printvn(*args):
    if verbose:
        print(*args, end='')


def roll_dice(num: int, sides: int, from_zero: bool = False) -> int:
    n = 0
    for i in range(num):
        printvn('\t\tDie number {} rolled '.format(i + 1))
        v = random.randint(1, sides)
        if from_zero:
            v -= 1
        printv(str(v))
        n += v
    printv('\t\tTotal: ' + str(n))
    return n


def eval_d_notation(expr: str) -> float:
    nexpr = expr.lower()
    printv('While evaluating expression `{}`, the following dice were used:'.format(expr))
    d = False
    for i in re.findall(r'\d+d\d+', nexpr):
        d = True
        printvn('\t`{}`, which means "roll '.format(i))
        if i[0] == 'd':
            i = '1' + i
        if i[-1] == 'd':
            i = i + '6'
        isp = [int(j) for j in i.split('d')]
        printv('{} dice, each of {} sides".'.format(*isp))
        nexpr = nexpr.replace(i, str(roll_dice(*isp)))
    for i in re.findall(r'\d+d', nexpr):
        printvn('\t`{}`, which means "roll '.format(i))
        d = True
        ni = i
        if i[0] == 'd':
            ni = '1' + i
        if i[-1] == 'd':
            ni = ni + '6'
        isp = [int(j) for j in ni.split('d')]
        printv('{} dice, each of {} sides".'.format(*isp))
        nexpr = nexpr.replace(i, str(roll_dice(*isp)))
    for i in re.findall(r'd\d+', nexpr):
        printvn('\t`{}`, which means "roll '.format(i))
        d = True
        ni = i
        if i[0] == 'd':
            ni = '1' + i
        if i[-1] == 'd':
            ni = ni + '6'
        isp = [int(j) for j in ni.split('d')]
        printv('{} dice, each of {} sides".'.format(*isp))
        nexpr = nexpr.replace(i, str(roll_dice(*isp)))
    for i in re.findall(r'd', nexpr):
        printvn('\t`{}`, which means "roll '.format(i))
        d = True
        ni = i
        if i[0] == 'd':
            ni = '1' + i
        if i[-1] == 'd':
            ni = ni + '6'
        isp = [int(j) for j in ni.split('d')]
        printv('{} dice, each of {} sides".'.format(*isp))
        nexpr = nexpr.replace(i, str(roll_dice(*isp)))
    if not d:
        printv('\tNo dice were used.')
    return eval(nexpr)

if __name__=='__main__':
    counter=0
    while 1:
        counter+=1
        try:
            expr=input(('Expression for run ' if verbose else '')+f'{counter}:')
        except KeyboardInterrupt:
            exit(0)
        except EOFError:
            exit(0)
        if re.match('([0-9]+)*([Dd])([0-9]+)*(\+[0-9]+)*',expr) or not pedantic:
            ts=time.time()
            try:
                print(f'{counter} ->', eval_d_notation(expr))
            except KeyboardInterrupt:
                te=time.time()
                print(f'Oh, did I really take {te-ts} seconds to calculate "{expr}"? I\'m super sorry! I\'ll try to be faster next time!' if verbose else f'{counter} -> T>{te-ts}s')
            except:
                print(f'There was a problem parsing the expression "{expr}" in run {counter}. Please enter a valid expression.' if verbose else f'{counter} -> WTF')
        else:
            print(f'I\'m sorry, but your expression "{expr}" doesn\'t look right to the regex. If you actually need to calculate this, please set the "pedantic" flag to False in the source code.' if verbose else f'{counter} -> FAILTEST')
