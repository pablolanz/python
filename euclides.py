def euc(a,b):
    if(a<b):
        x=a     #this just in case someone enters b bigger than a
        a=b
        b=x
    x=a%b
    while(x!=0):
        a=b
        b=x
        x=a%b
    return(b)

def extended_euc(a,b):
    if(a<b):
        x=a     #this just in case someone enters b bigger than a
        a=b
        b=x
    x=a%b
    x1=x
    a1=a
    b1=b
    j=0
    q=[a//b]
    while(x1!=0):
        a1=b1
        b1=x1
        q.append(a1//b1)
        x1=a1%b1
        j=j+1
    
    gcd=b1
    u=0
    v=0

    u0=1
    v0=-(a//b)
    u1=-(b//(a%b))  
    v1=1+(a//b)*(b//(a%b))

    for i in range(j-2):
        u=u0-q[i+2]*u1
        v=v0-q[i+2]*v1
        u0=u1
        u1=u
        v0=v1
        v1=v        
    return(u,v)

x=int(input())
y=int(input())
z=extended_euc(x,y)
print(z)