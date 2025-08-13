def agecalculator():
    birth = int(input("Hvilket år er du født: "))
    age = 2024 - birth
    
    if age < 0:
        print("Hold din kæft, du lyver!")
    elif age >= 18:
        print("Du er myndig og er " + str(age) + " år gammel.")
    else:
        print("Du er " + str(age) + " år gammel, så du er ikke myndig endnu.")

# agecalculator()

def convertdegree():
    cel=int(input("Hvor varmt er det i Celcius:"))
    farenheit = cel * 9/5 +32
    print("Det er "+str(farenheit)+" Grader farenheit")
    
# convertdegree()

def sortertal():
    talrække = input("Skriv nogle tal som er adskilt med mellemrum:").split
    print(talrække)
sortertal()