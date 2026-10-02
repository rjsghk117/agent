# Class는 대문자로 시작!!
# 설계도, 틀, 개념 등등
# class MyClass:
#     x = 5

# # print(MyClass)
# # 출력: <class 'ex1002.mypy.ex_oop.MyClass'>
# # print(MyClass.x) 출력값: 5

# # Object 생성
# p1 = MyClass()
# print(p1.x)

# class Myclass:
#     name = "James"
#     age = 10

# p2 = Myclass()
# print(p2.name)
# print(p2.age)

# # ######################
# # Object 생성할 때 Class 초기화 사용

# class Person:
#     def __init__(self, name, age):
#         self.name = name
#         self.age = age

# p = Person("Timothy", 28)

# print(p.name)
# print(p.age)

# ###############
# Class의 Method(액션)
class Person2:
    def __init__(self, name):
        self.name = name

    def greet(self):
        print("Hello, my name is", self.name)

p3 = Person2("Jonathan")
p3.greet()