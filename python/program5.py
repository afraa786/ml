# conditional statements
# age = int(input("Please enter your age: "))

# print("Your age is", age)
# if(age >= 18):
#     print("Can apply for license")

# elif(age < 18):
#     print("Cant get drivers license")

# conditional statement
marks = 45
if(marks >=90):
    grade = "A"

# condtional statemnt nesting
age = 51

age = 51

if age >= 18:
    if age <= 50:
        print("can drive")
    else:
        print("cant drive")
else:
    print("cant drive")

# or 
age = 51

if age >= 18 and age <= 50:
    print("can drive")
elif age > 50:
    print("cant drive")
else:
    print("cant drive")

x = int(input("enter a number:"))
if(x % 5 ==0):
    print("multiple of 5")
else:
    print("no")