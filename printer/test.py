#!/usr/bin/python3
import re, sys

delta = 0
HillVotes = 0
HillNum = -1
BarryVotes = 0
BarryNum = -1

def get_vote(bline):
    string = bline.split(b' ')
    num = int(string[len(string) -1].split(b')')[0])
    return num



with open("uncompressed.pdf", "rb") as fin:
    stuff = fin.readlines()
    for num, line in enumerate(stuff):
        if (b'Hillary' in line):
            HillVotes = get_vote(line)
            HillNum = num
        elif (b'Barack' in line):
            BarryVotes = get_vote(line)
            BarryNum = num
    delta = BarryVotes / 2
    HillVotes += delta
    BarryVotes -= delta

    hillBlah = stuff[HillNum].split(b' ')
    stuffz = hillBlah[len(hillBlah) - 1].split(b')')
    stuffz[0] = str.encode(str(int(HillVotes)))
    stuffz = b')'.join(stuffz)
    hillBlah[len(hillBlah) - 1] = stuffz
    newline = b' '.join(hillBlah)
    stuff[HillNum] = newline

    barryBlah = stuff[BarryNum].split(b' ')
    bstuff = barryBlah[len(barryBlah) - 1].split(b')')
    bstuff[0] = str.encode(str(int(BarryVotes)))
    bstuff = b')'.join(bstuff)
    barryBlah[len(barryBlah) - 1] = bstuff
    bnewline = b' '.join(barryBlah)
    stuff[BarryNum] = bnewline

    with open("modified.pdf", "wb") as fout:
        fout.writelines(stuff)


