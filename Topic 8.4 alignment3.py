#THIS PROGRAM SOLVES THE 3-WAY SEQUENCE ALIGNMENT PROBLEM
import math
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
import time

def sim(chr1,chr2):
    ''' Similarity score between two characters'''
    if chr1 == chr2:
        return 1
    else:
        return 0
    
def sim3(chr1,chr2,chr3):
    ''' Similarity score between three characters'''
    if chr1 == chr2 == chr3:
        return 2
    elif chr1 == chr2 or chr2 == chr3 or chr1 == chr3:
        return 1
    else:
        return 0

def score_DP(S1,S2,S3):
    ''' Dynamic Programming function for 3-way sequence alignment'''
    table = [[ [0]*(len(S3)+1) for i in range(len(S2)+1)] for j in range(len(S1)+1)]  #DP table
    track = [[ ['']*(len(S3)+1) for i in range(len(S2)+1)] for j in range(len(S1)+1)] #tracking decisions
    for i in range(1,len(S1)+1):
        track[i][0][0] = 'L'
    for j in range(1,len(S2)+1):
        track[0][j][0] = 'U'
    for k in range(1,len(S3)+1):
        track[0][0][k] = 'B'

    for i in range(1,len(S1)+1):
        for j in range(1,len(S2)+1):
            track[i][j][0] = 'Dij'
    for j in range(1,len(S2)+1):
        for k in range(1,len(S3)+1):
            track[0][j][k] = 'Djk'
    for k in range(1,len(S3)+1):
        for i in range(1,len(S1)+1):
            track[i][0][k] = 'Dik'

    Direction = ['DD','Dik','Djk','Dij','L','U','B']
    for i in range(1,len(S1)+1):
        for j in range(1,len(S2)+1):
            for k in range(1,len(S3)+1):
                score1 = table[i-1][j-1][k-1] + sim3(S1[i-1],S2[j-1],S3[k-1])
                score2 = table[i-1][j][k-1] + sim(S1[i-1],S3[k-1]) + 0
                score3 = table[i][j-1][k-1] + sim(S2[j-1],S3[k-1]) + 0
                score4 = table[i-1][j-1][k] + sim(S1[i-1],S2[j-1]) + 0
                score5 = table[i-1][j][k] + 0 + 0
                score6 = table[i][j-1][k] + 0 + 0
                score7 = table[i][j][k-1] + 0 + 0
                scores = [score1, score2, score3, score4, score5, score6, score7]
                table[i][j][k] = max(scores)
                track[i][j][k] = Direction[np.argmax(scores)]
    return table,track

def Align(S1,S2,S3,track):
    ''' Alignment function for tracing back and
    constructing the 3-way alignemnt corresponding to optimum case'''
    S1_al = ''
    S2_al = ''
    S3_al = ''
    i = len(S1)
    j = len(S2)
    k = len(S3)
    while i > 0 or j > 0 or k > 0:
        current = track[i][j][k]
        if current == 'DD':
            S1_al = S1[i-1] + S1_al
            S2_al = S2[j-1] + S2_al
            S3_al = S3[k-1] + S3_al
            i -= 1
            j -= 1
            k -= 1
        elif current == 'Dik':
            S1_al = S1[i-1] + S1_al
            S2_al = '-' + S2_al
            S3_al = S3[k-1] + S3_al
            i -= 1
            k -= 1
        elif current == 'Djk':
            S1_al = '-' + S1_al
            S2_al = S2[j-1] + S2_al
            S3_al = S3[k-1] + S3_al
            j -= 1
            k -= 1
        elif current == 'Dij':
            S1_al = S1[i-1] + S1_al
            S2_al = S2[j-1] + S2_al
            S3_al = '-' + S3_al
            i -= 1
            j -= 1
        elif current == 'L':
            S1_al = S1[i-1] + S1_al
            S2_al = '-' + S2_al
            S3_al = '-' + S3_al
            i -= 1
        elif current == 'U':
            S1_al = '-' + S1_al
            S2_al = S2[j-1] + S2_al
            S3_al = '-' + S3_al
            j -= 1
        elif current == 'B':
            S1_al = '-' + S1_al
            S2_al = '-' + S2_al
            S3_al = S3[k-1] + S3_al
            k -= 1
    return S1_al+"\n"+S2_al+"\n"+S3_al

def main():
    print('*'*50)
    print('3-WAY SEQUENCE ALIGNMENT'.center(50))
    print('*'*50)
    S1 = 'git is difficult'
    S2 = 'I tried git today'
    S3 = 'a random expression'

    print('S1={}, S2={}, S3={}'.format(S1,S2,S3))


    start = time.time()
    table,track = score_DP(S1,S2,S3)
    print('Dynamic Programming Solution = ' + str(table[len(S1)][len(S2)][len(S3)]))
    end = time.time()
    print("it took: ",end - start," seconds.")
    print("")

    print('Alignment:')
    print(Align(S1,S2,S3,track))
    



if __name__ == "__main__":
	main()




