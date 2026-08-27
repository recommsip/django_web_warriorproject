class A:

    def hello(self):
        print("A")


class B(A):

    def hello(self):
        print("B")
        super().hello()

# class something(anotherthing) - something extends anotherthing.
class C(B):
    @property   
    def hello(self):
        print("C")
        super().hello()

def main():
    obj = C()
    obj.hello

if __name__ == "__main__":
    main()
        


    