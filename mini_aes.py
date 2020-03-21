import numpy as np
def NibbleSub(block):
    bitsub={'0000':'1110','0001':'0100','0010':'1101','0011':'0001','0100':'0010','0101':'1111','0110':'1011','0111':'1000',
            '1000':'0011','1001':'1010','1010':'0110','1011':'1100','1100':'0101','1101':'1001','1110':'0000','1111':'0111'}
    for i in range(2):
        for j in range(2):
            block[i,j]=bitsub[block[i,j]]
    return block
    
def SubBytes(block):
    bitsub={'0000':'1110','0001':'0100','0010':'1101','0011':'0001','0100':'0010','0101':'1111','0110':'1011','0111':'1000',
            '1000':'0011','1001':'1010','1010':'0110','1011':'1100','1100':'0101','1101':'1001','1110':'0000','1111':'0111'}
    return bitsub[block]
    
def ShiftRows(block):
    block[1,0],block[1,1]=block[1,1],block[1,0]
    return block
    
def binary(number):
        binstr=''
        while number != 0:
            binstr+=str(number%2)
            number=number//2
        left=4-len(binstr)
        binstr=binstr[::-1]
        for i in range(left):
            binstr='0'+binstr
        return binstr 
        
def mult_xor(block,key):
  #takes in 2 binary digits
  A,B,C,D,E,F=10,11,12,13,14,15
  table=[[0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0],
         [0, 1 ,2 ,3 ,4 ,5 ,6 ,7 ,8 ,9 ,10 ,11 ,12 ,13 ,14 ,15 ],
         [0 ,2 ,4 ,6 ,8 ,10 ,12 ,14 ,3 ,1 ,7 ,5 ,11 ,9 ,15 ,13],
         [0 ,3 ,6 ,5 ,C ,F ,A ,9 ,B ,8 ,D ,E ,7 ,4 ,1 ,2],
         [0 ,4 ,8 ,C ,3 ,7 ,B ,F ,6 ,2 ,E ,A ,5 ,1 ,D ,9],
         [0, 5, A, F, 7, 2, D, 8, E, B, 4, 1, 9, C, 3, 6],
         [0, 6, C, A, B, D, 7, 1, 5, 3, 9, F, E, 8, 2, 4],
         [0, 7, E, 9, F, 8, 1, 6, D, A, 3, 4, 2, 5, C, B],
         [0, 8, 3, B, 6, E, 5, D, C, 4, F, 7, A, 2, 9, 1],
         [0 ,9 ,1 ,8 ,2 ,B ,3 ,A ,4 ,D ,5 ,C ,6 ,F ,7 ,E],
         [0 ,A ,7 ,D ,E ,4 ,9 ,3 ,F ,5 ,8 ,2 ,1 ,B ,6 ,C],
         [0 ,B ,5 ,E ,A ,1 ,F ,4 ,7 ,C ,2 ,9 ,D ,6 ,8 ,3],
         [0 ,C ,B ,7 ,5 ,9 ,E ,2 ,A ,6 ,1 ,D ,F ,3 ,4 ,8],
         [0 ,D ,9 ,4 ,1 ,C ,8 ,5 ,2 ,F ,B ,6 ,3 ,E ,A ,7],
         [0 ,E ,F ,1 ,D ,3 ,2 ,C ,9 ,7 ,6 ,8 ,4 ,A ,B ,5],
         [0 ,F ,D ,2 ,9 ,6 ,4 ,8 ,1 ,E ,C ,3 ,8 ,7 ,5 ,A]]
  block,key=int(block,2),int(key,2)
  res=table[block][key]
  res=binary(res)
  return res

def MixColumns(block):
    std_matrix=([['0011','0010'],['0010','0011']])
    a=block[0,0]
    b=block[1,0]
    c=block[0,1]
    d=block[1,1]
    print(mult_xor(std_matrix[0][0],a))
    first=XOR_BIT(mult_xor(std_matrix[0][0],a),mult_xor(std_matrix[0][1],b))         
    seco=XOR_BIT(mult_xor(std_matrix[1][0],a),mult_xor(std_matrix[1][1],b)) 
    third=XOR_BIT(mult_xor(std_matrix[0][0],c),mult_xor(std_matrix[0][1],d))  
    four=XOR_BIT(mult_xor(std_matrix[1][0],c),mult_xor(std_matrix[1][1],d))
    print(first)
    print(seco)
    print(third)
    print(four)
    block=np.matrix([[first,third],[seco,four]])
    return block 
    
def XOR_BIT(block,key):
    new=''
    for i in range(4):
        new+=str(int(block[i])^int(key[i]))
    return new
    
def AddRoundKey(block,key):
    for i in range(2):
        for j in range(2):
            block[i,j]=XOR_BIT(block[i,j],key[i,j])
    return block
    
def encrypt(block,key):
    rounds=2
    w4=XOR_BIT(XOR_BIT(key[0,0],SubBytes(key[1,1])),"0001")
    w5=XOR_BIT(key[1,0],w4)
    w6=XOR_BIT(key[0,1],w5)
    w7=XOR_BIT(key[1,1],w6)
    block=AddRoundKey(block,key)
    key=np.matrix([[w4,w6],[w5,w7]])
    w8=XOR_BIT(XOR_BIT(w4,SubBytes(w7)),"0010")
    w9=XOR_BIT(w5,w8)
    w10=XOR_BIT(w6,w9)
    w11=XOR_BIT(w7,w10)
    key2=np.matrix([[w8,w10],[w9,w11]])
    block=NibbleSub(block)
    block=ShiftRows(block)
    block=MixColumns(block)
    #print(block)
    block=AddRoundKey(block,key)
    #print(block)
    block=NibbleSub(block)
    block=ShiftRows(block)
    block=AddRoundKey(block,key2)
    return block
