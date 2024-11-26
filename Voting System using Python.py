vote1=input("Enter name of 1st candidate =")
vote2=input("Enter name of 2nd candidate =")

list1=[vote1,vote2]
print(list1)

print("Setup Complete, Voting Started..")

Voter_id_list=[101,102,103,104,105]
count_vote1=0
count_vote2=0
while True:
    id=input("Enter your id =")
    if id not in Voter_id_list:
        # Voter_id_list.append(id)
        print(f'1 .{vote1}')
        print(f'2 .{vote2}')
        choice=input("Enter your choice = ")
        if choice=="1":
            print(f"you voted {vote1}")
            count_vote1+=1
        elif choice=="2":
            print(f"you voted {vote2}")
            count_vote2+=1
        else:
            print("Choice Correct opption")
    else:
        print("You already Voted. Thank You")
        







    