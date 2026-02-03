import random

print("select the number of players (1 to 5) :")
numPlay=int(input())

numPlay=numPlay+1
cards=[]
value=[]
total=0
newcard=0
for i in range(numPlay):
    cards.append(random.randrange(1,14))
    cards.append(random.randrange(1,14))
for i in range(len(cards)):
    value.append(cards[i])
    if cards[i]==1:
        cards[i]="Ace"
        value[i]=11
    elif cards[i]==11:
        cards[i]="Jack"
        value[i]=10
    elif cards[i]==12:
        cards[i]="Queen"
        value[i]=10
    elif cards[i]==13:
        cards[i]="King"
        value[i]=10
for i in range(0,numPlay-1):
    print("Player",i," cards are:",cards[2*i],cards[2*i+1])
print("dealer has",value[2*numPlay-1])

ans=0
total=[]
for i in range(numPlay-1):
    total.append(0)
for i in range(numPlay-1):
    answer="yes"
    total[i]=value[2*i]+value[2*i+1]
    while(answer=="yes"):
        if (total[i]==21):
            print("Blackjack!")
            answer="bj"
        elif (total[i]>21):
            if (value[2*i]==11 and value[2*i+1]==11):
                value[2*i]=1

            elif (value[2*i+1]==11):
                value[2*i+1]=1

            elif (value[2*i]==11):
                value[2*i]=1

            else:
                print("Game Over")
                answer="go"
                total[i]=111

        else:
            print("Does player",i," want to be dealt another card?(y/n):")
            ans=input()
            if (ans=="y"):

                newcard=random.randrange(1,14)
                if (newcard==1):
                    print("Ace")
                elif (newcard==11):
                    print("Jack")
                elif (newcard==12):
                    print("Queen")
                elif (newcard==13):
                    print("King")
                else:
                    print(newcard)
                                    
                if (total[i]>11):
                    total[i]=total[i]+newcard
                else:
                    if (newcard==1):
                        total[i]=total[i]+11
                    elif(1<newcard<10):
                        total[i]=total[i]+newcard
                    else:
                        total[i]=total[i]+10
            else:
                answer="no"

length=numPlay-1
totald=value[2*length]+value[2*length+1]
while (totald<17):
                newcard=random.randrange(1,14)
                if (newcard==1):
                    print("Dealer gets an Ace")
                elif (newcard==11):
                    print("Dealer gets a Jack")
                elif (newcard==12):
                    print("Dealer gets a Queen")
                elif (newcard==13):
                    print("Dealer gets a King")
                else:
                    print("Dealer gets a ",newcard)
                                    
                if (totald>11):
                    totald=totald+newcard
                else:
                    if (newcard==1):
                        totald=totald+11
                    elif(1<newcard<10):
                        totald=totald+newcard
                    else:
                        totald=totald+10
print("Dealer has", totald)
for i in range(numPlay-1):
    if (total[i]==totald):
        print("player",i," has",total[i])
        print("player",i,"gets his money back")
    elif (totald<total[i]<22):
        print("player",i," has",total[i])
        print("player",i,"wins!")
    elif(total[i]<totald):
        print("player",i," has",total[i])
        print("player",i,"loses")
    else:
        print("player",i," has over 21 and lost his money")
