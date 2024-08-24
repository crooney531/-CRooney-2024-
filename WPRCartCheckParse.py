# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 15:51:35 2024

@author: roone
"""

import os

# Set the base directory to the new folder path
fbase = r'C:\Users\roone\Downloads\wprStartupAll'
out = []

def checkCartCheck(segs):
    out = []
    LimitPDSigma = 0.00600
    LimitAttenSigma = 0.001200
    LimitNearRMSSigma = 10.0
    LimitFarRMSSigma = 10

    for m in segs:
        dat = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ignore = 0
        m = m.replace("\r", "")
        if m.find("T1 -") >= 0 and m.find("│") >= 0:
            dat[0] = "T1"
        elif m.find("T2 -") >= 0 and m.find("│") >= 0:
            dat[0] = "T2"
        elif m.find("T3 -") >= 0 and m.find("│") >= 0:
            dat[0] = "T3"
        elif m.find("T4 -") >= 0 and m.find("│") >= 0:
            dat[0] = "T4"
        else:
            ignore = 1

        if ignore == 0:
            if m.find("400 KHz") >= 0 and m.find("│") >= 0:
                dat[1] = "400 KHz"
            elif m.find("2 MHz") >= 0 and m.find("│") >= 0:
                dat[1] = "2 MHz"

        if ignore == 0:
            sss = m.split("│")
            dat[2] = sss[2].replace(" ", "")
            dat[3] = sss[3].replace(" ", "")
            dat[4] = sss[4].replace(" ", "")
            dat[5] = sss[5].replace(" ", "")
            dat[6] = sss[6].replace(" ", "")
            dat[7] = sss[7].replace(" ", "")
            dat[8] = sss[8].replace(" ", "")
            dat[9] = sss[9].replace(" ", "")

        if ignore == 0:
            print(["cc data", dat])

            if (dat[0] == "T1" or dat[0] == "T2" or dat[0] == "T3" or dat[0] == "T4") and (dat[1] == "400 KHz" or dat[1] == "2 MHz"):
                out.append(dat)
    return out

def checkTransmitterTest(segs):
    tars = [
        "T1 - 400 KHz Power", "T1 - 400 KHz Total AGC", "T1 - 400 KHz Rcvd Signal",
        "T1 - 2 MHz Power", "T1 - 2 MHz Total AGC", "T1 - 2 MHz Rcvd Signal",
        "T2 - 400 KHz Power", "T2 - 400 KHz Total AGC", "T2 - 400 KHz Rcvd Signal",
        "T2 - 2 MHz Power", "T2 - 2 MHz Total AGC", "T2 - 2 MHz Rcvd Signal",
        "T3 - 400 KHz Power", "T3 - 400 KHz Total AGC", "T3 - 400 KHz Rcvd Signal",
        "T3 - 2 MHz Power", "T3 - 2 MHz Total AGC", "T3 - 2 MHz Rcvd Signal",
        "T4 - 400 KHz Power", "T4 - 400 KHz Total AGC", "T4 - 400 KHz Rcvd Signal",
        "T4 - 2 MHz Power", "T4 - 2 MHz Total AGC", "T4 - 2 MHz Rcvd Signal"
    ]

    try:
        LimitRcvdSignal = [16170, 17770]
        dat = [0, 0, 0, 0, 0, 0]
        for m in segs:
            m = m.replace("\r", "")
            for tar in tars:
                if m.find(tar) >= 0:
                    if m.find("Power") >= 0:
                        dat[0] = m.split(":")[1].split(" mw")[0]
                        dat[1] = m.split("VBatt: ")[1].split(" V")[0]
                        dat[2] = m.split("Current: ")[1].split(" ma")[0]
                        dat[3] = m.split("Pot: ")[1].split(" dB")[0].split(")")[0]
                    if m.find(" Total AGC") >= 0:
                        dat[4] = m.split(":")[1].split(" ")[1]
                    if m.find(" Rcvd Signal") >= 0:
                        dat[5] = m.split(":")[1].split(" ")[1]
                        i1 = int(dat[5])
                        if i1 > LimitRcvdSignal[1] or i1 < LimitRcvdSignal[0]:
                            print (["Limit AGC", dat])
                        print([tar[0:8], dat])
                        dat = [0, 0, 0, 0, 0, 0]
    except:
        pass

def checkPreamp(segs):
    tars = [
        "T1 - 400 KHz R1", "T1 - 400 KHz R2", "T1 - 2 MHz R1", "T1 - 2 MHz R2",
        "T3 - 400 KHz R1", "T3 - 400 KHz R2", "T3 - 2 MHz R1", "T3 - 2 MHz R2"
    ]
    try:
        for m in segs:
            m = m.replace("\r", "")
            for tar in tars:
                dat = [0, 0, 0]
                if m.find(tar) >= 0:
                    sss = m.split(" Tuned ")
                    dat[0] = sss[1].split(",")[0]
                    sss = m.split("Mistuned ")
                    dat[1] = sss[1].split(",")[0]
                    sss = m.split(" Ratio ")
                    dat[2] = sss[1]
                    print ([tar, dat])
    except:
        pass

out = []
dout = []
for path, sdir, files in os.walk(fbase):
    cnt = 1
    for f in files:
        with open(os.path.join(path, f), "rb") as file:
            rd = file.read()
            guts = rd.decode().split("\n")
            sn = "?"
            for line in guts:
                line = line.replace("\r", "")
                if line.find(" : Serial Number ") >= 0:
                    sn = line.split(" : Serial Number ")[1].split(",")[0]

                tag = "Tool Size   "

                if line.find(tag) >= 0:
                    tt = line.split(tag)[1].split(": ")[1]
                    if tt[0] == "3":
                        tsize = "3"
                    elif tt[0] == "4":
                        tsize = "4"
                    elif tt[0] == "5":
                        tsize = "5"
                    elif tt[0] == "6":
                        tsize = "6"
                    elif tt[0] == "7":
                        tsize = "7"
                    elif tt[0] == "8":
                        tsize = "8"
                    if len(tt) == 2:
                        if tt[1] == "½":
                            tsize += ".5"
                        elif tt[1] == "¾":
                            tsize += ".75"
                        else:
                            print(["tt", tt])
                            print("OVER")
                    if len(tt) == 3:
                        if tt[2] == "½":
                            tsize += ".5"
                        elif tt[2] == "¼":
                            tsize += ".25"
                        elif tt[2] == "¾":
                            tsize += ".75"
                        else:
                            print(["tt", tt])
                            print("OVER")
                    print(tsize)
                    if len(tt) > 3:
                        if tt[1:4] == ".75":
                            tsize += ".75"
                        else:
                            print(["tt", tt])
                            print("OVER")

            found4 = 0
            found5 = 0
            found6 = 0
            for gut in guts:
                if found4 == 0 and gut.find("Transmitter Test") >= 0:
                    found4 = 1
                    segs = []
                if found4 == 1:
                    if gut.find("--------------") >= 0:
                        found4 = 2
                        print("Transmitter")
                        checkTransmitterTest(segs)
                    else:
                        segs.append(gut)
                if found5 == 0 and gut.find("Preamp Test") >= 0:
                    found5 = 1
                    segs = []
                if found5 == 1:
                    if gut.find("---------------") >= 0:
                        found5 = 2
                        print("Preamp")
                        checkPreamp(segs)
                    else:
                        segs.append(gut)
                if found6 == 0 and gut.find("Cart Check") >= 0:
                    found6 = 1
                    segs = []
                if found6 == 1:
                    if gut.find("Technician Sign") >= 0:
                        found6 = 2
                        print("Cart Check")
                        resp = checkCartCheck(segs)
                        if resp != "":
                            print([sn, resp])
                            if len(resp) > 0:
                                for rr in resp:
                                    dout.append([sn, tsize, rr])
                    else:
                        segs.append(gut)

lines = []
for d in dout:
    print(d)
    lines.append(d[0] + "," + d[1] + "," + ",".join(d[2]))
with open("StartUpCartCheckOutput.csv", "w") as f:
    f.write("\n".join(lines))
