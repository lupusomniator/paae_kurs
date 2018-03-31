# put your python code here
s = input()
a = sum([int(el) for el in s[0:3]])
b = sum([int(el) for el in s[3:6]])
print(a,b,s[0:2],s[3:5])
if a==b:
    print("Счастливый")
else:
    print("Обычный")



