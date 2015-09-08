#!/usr/bin/env python

"""Code from github for python global alignment with affine gap penalties. Code is from:
https://github.com/dnase/affine-gap-sequence-alignment/blob/master/alignment.py"""

from matrices import Blosum62

global S
global E
global match
global mismatch
global MIN
S = -11
E = -1
#match = 1
#mismatch = -4
MIN = -float("inf")

#return match or mismatch score
def _match(s, t, i, j):
    #if t[i-1] == s[j-1]:
    return Blosum62(t[i-1],s[j-1]).sub_score()
    #else:
        #return mismatch

#initializers for matrices
def _init_x(i, j):
    if i > 0 and j == 0:
        return MIN
    else:
        if j > 0:
            return -10 + (-0.5 * j)
        else:
            return 0

def _init_y(i, j):
    if j > 0 and i == 0:
        return MIN
    else:
        if i > 0:
            return -10 + (-0.5 * i)
        else:
            return 0

def _init_m(i, j):
    if j == 0 and i == 0:
        return 0
    else:
        if j == 0 or i == 0:
            return MIN
        else:
            return 0

def _format_tuple(inlist, i, j):
    return 0

def distance_matrix(s, t):
    dim_i = len(t) + 1
    dim_j = len(s) + 1
    #abuse list comprehension to create matrices
    X = [[_init_x(i, j) for j in range(0, dim_j)] for i in range(0, dim_i)]
    Y = [[_init_y(i, j) for j in range(0, dim_j)] for i in range(0, dim_i)]
    M = [[_init_m(i, j) for j in range(0, dim_j)] for i in range(0, dim_i)]

    for j in range(1, dim_j):
        for i in range(1, dim_i):
            X[i][j] = max((S + E + M[i][j-1]), (E + X[i][j-1]), (S + E + Y[i][j-1]))
            Y[i][j] = max((S + E + M[i-1][j]), (S + E + X[i-1][j]), (E + Y[i-1][j]))
            M[i][j] = max(_match(s, t, i, j) + M[i-1][j-1], X[i][j], Y[i][j])
    return [X, Y, M]

def backtrace(s, t, X, Y, M):
    sequ1 = ''
    sequ2 = ''
    i = len(t)
    j = len(s)
    while (i>0 or j>0):
        if (i>0 and j>0 and M[i][j] == M[i-1][j-1] + _match(s, t, i, j)):
            sequ1 += s[j-1]
            sequ2 += t[i-1]
            i -= 1
            j -= 1
        elif (i>0 and M[i][j] == Y[i][j]):
            sequ1 += '-'
            sequ2 += t[i-1]
            i -= 1
        elif (j>0 and M[i][j] == X[i][j]):
            sequ1 += s[j-1]
            sequ2 += '-'
            j -= 1

    print sequ1
    print sequ2
    sequ1r = ' '.join([sequ1[j] for j in range(-1, -(len(sequ1) + 1), -1)])
    sequ2r = ' '.join([sequ2[i] for i in range(-1, -(len(sequ2) + 1), -1)])

    return [sequ1r, sequ2r]


if __name__ == '__main__':
    import sys
    seq1 = sys.argv[1]
    seq2 = sys.argv[2]
    print seq1
    print seq2
    X,Y,M = distance_matrix(seq1,seq2)
    s1,s2 = backtrace(seq1,seq2,X,Y,M)
    print s1
    print s2
