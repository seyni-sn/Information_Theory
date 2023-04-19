#!/usr/bin/python3

import math

def entropy(a):
    s=sum(a)
    e=0
    for x in a:
        p=x/s
        e+=(p)*math.log2(p)
    return -e

def test_entropy():
    assert entropy([1,1]) == 1
    assert entropy([1,1,2]) == 1.5
    print("pass")

def huffman_len(a):
    s=sum(a)
    if(len(a)<=1):
        return 0
    a=sorted(a,reverse=True)
    x=a.pop()+a.pop()
    a.append(x)
    return x/s+huffman_len(a)

def test_huffman_len():
    assert huffman_len([1,1]) == 1
    assert huffman_len([1,1,2]) == 1.5
    print("pass")


test_entropy()
test_huffman_len()
a=[1,1,2,4,8,1,1,2,4,8]
print(huffman_len(a))
print(entropy(a))
a=[1,1,1,1,1,1,1,2]
print(huffman_len(a))
print(entropy(a))


