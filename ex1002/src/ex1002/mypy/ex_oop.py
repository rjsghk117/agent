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
print(p3.name)
print("-"*60)


##################################

class Person3:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"{self.name} ({self.age})"

pp1 = Person3("장영실", 36)
print(pp1)

##################################
# class Student(Person3):
#     pass

# st1 = Student("Kure", 24)
# print(st1.name)

############################

class Student(Person3):
    def __init__(self, name, age, school, grade):
        super().__init__(name, age)
        self.school = school
        self.grade = grade
        
# super 부모의 값을 사용
st01 = Student("한석봉", 20, "HOSEO", 4)
print(st01.school)
print(st01.grade)
print(st01.name)
print(st01.age)

############################

class Shape:
    def __init__(self, shape, name):
        self.shape = shape
        self.name = name

class Square(Shape):
    def __init__(self, shape, name, width, height):
        super().__init__(shape, name)
        self.width = width
        self.height = height

class Triangle(Shape):
    def __init__(self, shape, name, width, height):
        super().__init__(shape, name)
        self.width = width
        self.height = height

sq = Square("Square", "Square", 4, 4)
print(sq.name)
print(sq.shape)
print(sq.width)
print(sq.height)

tr = Triangle("Triangle", "Triangle", 4, 4)
print(tr.shape)
print(tr.name)
print(tr.width)
print(tr.height)

########################################

class Food():
    def __init__(self, name, type):
        self.name = name
        self.type = type

class Rice(Food):
    def __init__(self, name, type, how, when):
        super().__init__(name, type)
        self.how = how
        self.when = when

class Soup(Food):
    def __init__(self, name, type, how, when):
        super().__init__(name, type)
        self.how = how
        self.when = when

r1 = Rice("밥", "Eat", "Grow", "Fall")
print(r1.name)
print(r1.type)
print(r1.how)
print(r1.when)

s1 = Soup("국", "Drink", "Make", "After Cook")
print(s1.name)
print(s1.type)
print(s1.how)
print(s1.when)