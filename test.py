
from time import sleep 

def run():
    print("press 'Enter' to continue and 'ctrl+c' to stop sec hand of clock")
    attempt=1
    name=input("Enter name of player :")
    point=0
    point_table={}
    
    while True:
        for digit in range(1,13):
            try:
                print(digit)
                sleep(0.4)
            except KeyboardInterrupt:
                print(f"Stopped at {digit}")
                print("Point are Added.")
                sleep(2)
                if digit in [1,5,9,11]:
                    point=point+10
                elif digit in [4,7,8,10]:
                    point=point+20
                elif digit in [3,2,6,12]:
                    point=point+30
                attempt+=1
                if attempt==4:
                    print(f'Final Score of {name} is {point}.')
                    point_table[name]=point
                    ans=input("Are you continue y/n =")
                    ans=ans.lower()
                    if ans=="y":
                        point=0
                        attempt=1
                        name=input("Enter name of player :")
                    else:
                        print(f"Final result of gave is {point_table}")
                        return
                
    
run()
