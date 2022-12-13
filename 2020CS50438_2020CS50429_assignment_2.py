from symbol import term
from tkinter import *
from PIL import Image, ImageTk
from K_map_gui_tk import *

def makegraycode( n ):
    gray_code = ["0","1"]
    if(n<1):
        return {"0"}
    while(len(gray_code)<pow(2,n)):
        l = len(gray_code)
        for i in range(l-1,-1,-1):
            gray_code.append(gray_code[i])
        # append 0 to the first half
        for j in range(l):
            gray_code[j] = "0" + gray_code[j]
 
        # append 1 to the second half
        for j in range(l, 2 * l):
            gray_code[j] = "1" + gray_code[j]
    # print(gray_code)
    return gray_code


def is_legal_region(kmap_function, term, nones, graycol, grayrow):
    n= len(term)
    count=0
    r = len(kmap_function)
    c = len(kmap_function[0])
    goodterms=[]
    for i in range(r):
        for j in range(c):
            kmapterm = graycol[j]+grayrow[i]
            match=True
            for k in range(len(term)):
                if term[k]!=None:
                    if term[k]!=int(kmapterm[k]):
                        # print(f"false ... {kmapterm}")
                        match=False
                        break
                if(k==len(term)-1 and match==True):
                    goodterms.append([i,j])
            if(match==True):
                count=count+1 
    if(count == pow(2,nones)):
        for i in range(len(goodterms)):
            if(kmap_function[goodterms[i][0]][goodterms[i][1]]==0):
                return (0, 0, False)
        return (1, 1, True)
    else:
        return (0, 0, False)


def comb_function_expansion(func_TRUE, func_DC):
    n = 0 
    for c in func_TRUE[0]:
        if ord(c) > 96:
            n=n+1
    grayrow = makegraycode(int(n/2))
    graycol = makegraycode(n - int(n/2))

    mat = []
    term_array = []
    for i in range(len(grayrow)):
        r = [0 for i in range(len(graycol))]
        mat.append(r)

    for t in func_TRUE: # ab in col,  cd in row
        tt = ""
        tt_arr =[]
        i=0
        while i<len(t):
            if i+1<len(t):
                if ord(t[i+1])<97: #apostrophe
                    tt_arr.append(0)
                    tt = tt+"0"
                    i=i+2
                else:
                    tt_arr.append(1)
                    tt = tt+"1"
                    i=i+1
            else:
                tt_arr.append(1)
                tt = tt+"1" 
                i=i+1
        term_array.append(tt_arr)
        ttcol = tt[0:n-int(n/2)] # first variables in col
        ttrow = tt[n-int(n/2):] # last n/2 variables in row
        mat[grayrow.index(ttrow)][graycol.index(ttcol)] = 1

    for t in func_DC:
        tt = ""
        i=0
        while i<len(t):
            if i+1<len(t):
                if ord(t[i+1])<97: #apostrophe
                    tt = tt+"0"
                    i=i+2
                else:
                    tt = tt+"1"
                    i=i+1
            else:
                tt = tt+"1" 
                i=i+1
        ttcol = tt[0:n-int(n/2)] # first variables in col
        ttrow = tt[n-int(n/2):] # last n/2 variables in row
        mat[grayrow.index(ttrow)][graycol.index(ttcol)] = None 
    ans = []
    for x in term_array:
        a = max_legal_region(mat,x.copy(), graycol, grayrow)
        
        ans.append(a)
    print(f"FINAL EXPANDED TERMS: {printterm(ans)}")
    return ans


def max_legal_region(kmap, term, graycol, grayrow):
    pterm = printterm([term])
    nextnone = 0
    exp_list1 =[]
    exp_list2 =[]
    list1 = 1
    ans =term
    for i in range(len(term)):
        temp = term.copy()
        temp[i]= None
        temp1= is_legal_region(kmap, temp, list1, graycol, grayrow ) 
        if(temp1[2]==True):
            ans =temp
            exp_list1.append(temp)
    list1=list1+1

    # print(f"Expansion List for {pterm[0]}:{exp_list1}")
    print(f"Terms for next expansion for {pterm[0]}: {printterm(exp_list1)}")
    print(f"Updated answer for {pterm[0]}: {printterm([ans])}")   
    print()
    while(len(exp_list1)>0 or len(exp_list2)>0):
        if(list1%2==0):
            for t in exp_list1:
                for i in range(len(t)):
                    tmp = t.copy()
                    if(tmp[i]!=None):
                        tmp[i]= None
                        tmp1= is_legal_region(kmap, tmp, list1,  graycol, grayrow)
                        if(tmp1[2]== True):
                            ans = tmp
                            if tmp not in exp_list2:
                                exp_list2.append(tmp) 
            # print(f"exp list 2:{exp_list2}")  
            # print(f"Expansion List for {pterm[0]}:{exp_list2}")
            print(f"Terms for next expansion for {pterm[0]}: {printterm(exp_list2)}")
            print(f"Updated answer for {pterm[0]}: {printterm([ans])}") 

            print()   
            exp_list1=[]
            list1=list1+1
        else:
            for t in exp_list2:
                for i in range(len(t)):
                    tmp = t.copy()
                    if(tmp[i]!=None):
                        tmp[i]= None
                        tmp1= is_legal_region(kmap, tmp, list1,  graycol, grayrow)
                        if(tmp1[2]== True):
                            ans =tmp
                            if tmp not in exp_list1:
                                exp_list1.append(tmp)  
            # print(f"Expansion List for {pterm[0]}:{exp_list1}")
            print(f"Terms for next expansion for {pterm[0]}: {printterm(exp_list1)}")
            print(f"Updated answer for {pterm[0]}: {printterm([ans])}")  
            print()
            exp_list2=[]
            list1=list1+1
    print(f"Final expanded term for {pterm[0]}: {printterm([ans])} ------------------------------------------------------------------")
    print()
    print()
    return ans

def printterm(term):
    p=[]
    for i in range(len(term)):
        s=""
        n = len(term[i])
        for j in range(n):
            if(term[i][j]!=None):
                s=s+chr(97+j)
                if(term[i][j]==0):
                    s+="'"
        p.append(str(s+""))
    return p

func_TRUE = ["a'b'c'd'e'", "a'b'cd'e", "a'b'cde'", "a'bc'd'e'",
"a'bc'd'e", "a'bc'de", "a'bc'de'", "ab'c'd'e'", "ab'cd'e'"]
func_DC = ["abc'd'e'", "abc'd'e", "abc'de", "abc'de'"]

comb_function_expansion(func_TRUE, func_DC)
print(f"func_TRUE = {func_TRUE}")
print(f"func_DC = {func_DC}")