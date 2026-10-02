# # 값을 실행한 결과를 전달: return
# def myfunction(num1):
#     result = num1 + 100
#     return result

# sum = myfunction(77)
# print(sum)

# # ###############

# # 매개변수(fname, lname)의 인수를 똑같이 맞춰줘야함
# def my_function(fname, lname):
#     print(fname + " " + lname)

# my_function("Emily", "Freeman")

# # my_function("Sean Kingston")
# # 오류 메세지:
# # TypeError: my_function() missing 1 required positional argument: 'lname'

# # ################

# def myfunc(country = "Norway"):
#     # 공통 출력 기능
#     print("I am from", country)

# myfunc("Uganda")
# myfunc("Australia")
# myfunc() # default로 실행 됨 (Norway)
# myfunc("Japan")

# # #############

# def pet(animal, name):
#     print("I have a", animal)
#     print("My", animal + "'s name is", name)

# pet(animal="cat", name="Lemon")
# pet(name="John", animal="dog")

