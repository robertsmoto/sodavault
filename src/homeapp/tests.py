# from django.test import TestCase

# Create your tests here
class Test():
    def __init__(self):
        self.var1 = "hello"
        self.var2 = "world"


def clean(v):
    if not v:
        return
    return "has been cleaned"


if __name__ == "__main__":
    test = Test()
    print(vars(test))

    for k, v in vars(test).items():
        vars(test)[k] = "cleaned"

    print("cleaned", vars(test))
