from __future__ import division
from collections import defaultdict
import math
import sys

param = defaultdict(list)

train_file = tuple(open(sys.argv[1], "r"))
test_file = tuple(open(sys.argv[2], "r"))

f_name = [sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6]]
with open('train1.txt', 'w') as out_file:
    for f in f_name:
        with open(f) as in_file:
            for line in in_file:
                out_file.write(line)

f_name = [sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[7]]
with open('train2.txt', 'w') as out_file:
    for f in f_name:
        with open(f) as in_file:
            for line in in_file:
                out_file.write(line)

f_name = [sys.argv[3], sys.argv[4], sys.argv[6], sys.argv[7]]
with open('train3.txt', 'w') as out_file:
    for f in f_name:
        with open(f) as in_file:
            for line in in_file:
                out_file.write(line)

f_name = [sys.argv[3], sys.argv[5], sys.argv[6], sys.argv[7]]
with open('train4.txt', 'w') as out_file:
    for f in f_name:
        with open(f) as in_file:
            for line in in_file:
                out_file.write(line)

f_name = [sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7]]
with open('train5.txt', 'w') as out_file:
    for f in f_name:
        with open(f) as in_file:
            for line in in_file:
                out_file.write(line)

t_file1 = tuple(open("train1.txt","r"))
t_file2 = tuple(open("train2.txt","r"))
t_file3 = tuple(open("train3.txt","r"))
t_file4 = tuple(open("train4.txt","r"))
t_file5 = tuple(open("train5.txt","r"))

split_file1 = tuple(open(sys.argv[3], "r"))
split_file2 = tuple(open(sys.argv[4], "r"))
split_file3 = tuple(open(sys.argv[5], "r"))
split_file4 = tuple(open(sys.argv[6], "r"))
split_file5 = tuple(open(sys.argv[7], "r"))

def train(files, smooth):
    y0 = y1 = 0
    x1y0 = [0]*68000
    x1y1 = [0]*68000
    Px1y0 = [0]*68000
    Px1y1 = [0]*68000
    for i in range(len(files)):
        line = files[i]
        line = line.rstrip()
        line = line.split()
        label = int(line[0])
        if label == 1:
            y1 = y1 + 1
            for j in range(len(line)):
                if j != 0:
                    wording = line[j].split(":")
                    f = int(wording[0])
                    x1y1[f-1] = x1y1[f-1] + 1
        else:
            y0 = y0 + 1
            for j in range(len(line)):
                if j != 0:
                    wording = line[j].split(":")
                    f = int(wording[0])
                    x1y0[f-1] = x1y0[f-1] + 1
    y = y0 + y1
    Py0 = y0/y
    Py1 = y1/y
    for i in range(68000):
        Px1y0[i] = (x1y0[i] + smooth)/(y0 + (2 * smooth))
        Px1y1[i] = (x1y1[i] + smooth)/(y1 + (2 * smooth))
    return Py0, Py1, Px1y0, Px1y1

def test(files, smooth, Py0, Py1, Px1y0, Px1y1):
    accuracy = 0.0
    count = 0.0
    for i in range(len(files)):
        indexT = []
        FeatureValueT = [0]*68000
        temp0 = 1.0
        temp1 = 1.0
        EachLineT = files[i]
        EachLineStripT = EachLineT.rstrip()
        EachLineListT = EachLineStripT.split()
        LinelengthT = len(EachLineListT)
        YT = int(EachLineListT[0])
        for j in range(LinelengthT):
            if j != 0:
                Index_ValueT = EachLineListT[j].split(":")
                m = int(Index_ValueT[0])
                FeatureValueT[m-1] = 1
        for d in range(68000):
            if (FeatureValueT[d] == 1):
                temp0 = temp0 + math.log(Px1y0[d],2)
                temp1 = temp1 + math.log(Px1y1[d],2)
            else:
                temp0 = temp0 + math.log((1 - Px1y0[d]),2)
                temp1 = temp1 + math.log((1 - Px1y1[d]),2)
        temp0 = temp0 + math.log(Py0,2)
        temp1 = temp1 + math.log(Py1,2)
        if (temp0 > temp1):
            Yi = -1
        else:
            Yi = 1
        count = count + 1
        if (Yi == YT):
            accuracy = accuracy + 1
    accuracy = accuracy / count
    accuracy = accuracy * 100
    return accuracy

def main():
    values = [2, 1.5, 1.0, 0.5]
    for v in values:
        acc = avg_acc = 0.0
        Py0, Py1, Px1y0, Px1y1 = train(t_file1, v)
        accuracy = test(split_file5, v, Py0, Py1, Px1y0, Px1y1)
        acc = acc + accuracy
        Py0, Py1, Px1y0, Px1y1 = train(t_file2, v)
        accuracy = test(split_file4, v, Py0, Py1, Px1y0, Px1y1)
        acc = acc + accuracy
        Py0, Py1, Px1y0, Px1y1 = train(t_file3, v)
        accuracy = test(split_file3, v, Py0, Py1, Px1y0, Px1y1)
        acc = acc + accuracy
        Py0, Py1, Px1y0, Px1y1 = train(t_file4, v)
        accuracy = test(split_file2, v, Py0, Py1, Px1y0, Px1y1)
        acc = acc + accuracy
        Py0, Py1, Px1y0, Px1y1 = train(t_file5, v)
        accuracy = test(split_file1, v, Py0, Py1, Px1y0, Px1y1)
        acc = acc + accuracy
        avg_acc = acc/5.0
        param[v] = avg_acc
        print v, avg_acc
    best = max(param, key=param.get)
    print "Best hyperparamerter: ", best
    print "Cross Validation Accuracy: ", param[best]
    Py0, Py1, Px1y0, Px1y1 = train(train_file, best)
    accuracy = test(train_file, best, Py0, Py1, Px1y0, Px1y1)
    print "Traning Accuracy: ", accuracy
    accuracy = test(test_file, best, Py0, Py1, Px1y0, Px1y1)
    print "Test Accuracy: ", accuracy

if __name__ == '__main__':
    main()
