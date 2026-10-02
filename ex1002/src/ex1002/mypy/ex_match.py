# Python Match Statement
# day = 5
# match day:
#     case 1:
#         print("dog")
#     case 2:
#         print("cat")
#     case 3:
#         print("elephant")
#     case 4: 
#         print("duck")
#     case 5:
#         print("mole")
#         print("horse")

# Default Value
# Use the underscore (_) as the last case value if you want a code block to execute when there are not other matches

# animal = 1
# match animal:
#     case 5:
#         print("rat")
#     case 6:
#         print("mouse")
#     case _:
#         print("dragon")
# The value _ will always match, so it is imoprtant to place it as the last case to make it behave as a default case.

# Combine Values
# Use the pip | as an "or" operator in the case evaluation to check for more than ove value match in one case
# creature = 3
# match creature:
#     case 1 | 2 | 3 | 4 | 5:
#         print("giant squid")
#     case 6 | 7:
#         print("megalodon")

# If Statements as Guards
# You can add "if" statements in the case evaluation as an extra condition-check
x = 5
y = 4
match y:
    case 1 | 2 | 3 | 4 | 5 if x == 4:
        print("What is this thing?!")
    case 1 | 2 | 3 | 4 | 5 if x == 5:
        print("What is that?!")
    case _:
        print("How on Earth?")