# a1, d, n= int(input()), int(input()), int(input())
# an=a1+d*(n-1)
# print(an)

# x=int(input())
# print(x, 2*x, 3*x, 4*x, 5*x, sep='---')
# b1, q, n=int(input()), int(input()), int(input())
# bn=b1*q**(n-1)
# print(bn)
# lengthSm=int(input())
# lengthM=lengthSm//100
# print(lengthM)
# n, k=int(input()), int(input())
# ostatok=k//n
# kolvo=k%n
# print(ostatok,kolvo,sep="\n")
# print(lengthM)
# m=int(input())
# x = 1
# while x < 36:
#     print(((x-1)//4)+1)
#     x += 1
# num=int(input())
# a = str(num % 10)
# b = str((num % 100) // 10)
# c = str((num // 100) % 10)
# d = str(num // 1000)
# print("Цифра в позиции тысяч равна", d)
# print("Цифра в позиции сотен равна", c)
# print("Цифра в позиции десятков равна", b)
# print("Цифра в позиции единиц равна", a)
# n=98765
# print(n % 10000 // 1000)
# print(n // 10000)
# print(n % 1000 // 100)
# print(n % 100 // 10)
# a,b,c,d=int(input()),int(input()),int(input()),int(input())
# print(a**b+c**d)    
# a=str(input())
# b=str(input())
# num=int(input())
# d = (num % 10)
# c = ((num % 100) // 10)
# b = ((num // 100) % 10)
# a = (num // 1000)
# if a+d==b-c:
#     print("ДА")
# else:
#     print("НЕТ")
# a,b,c,d=int(input()), int(input()),int(input()), int(input())
# if a<b:
#     a1=a
# else:
#     a1=b
# if c<d:
#     b1=c
# else:
#     b1=d
# if a1<b1:
#     print(a1)
# else:
#     print(b1)

# old=int(input())
# if old<15:
#     print("детство")
# if old>15 and old<25:
#     print("молодость")
# if old>24 and old<60:
#     print("зрелость")
# if old>59:
#     print("старость")
# a,b,c=int(input()),int(input()),int(input())
# i = 101
# x = 2 if i>100 else 1 if i<100 else 0
a=int(input())
a=a if a>0 else 0
b=int(input())
b=b if b>0 else 0
c=int(input())
c=c if c>0 else 0
print(a+b+c)