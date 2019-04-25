
class Foo():
    def __init__(self):
        self.a = "a"
        self.b = lambda x,y: x * y
		
class Bar():
    def __init__(self, foo):
        self.foo = foo
        self.c = "c"
    def __getattr__(self, n, *a, **k):
        print(hasattr(self.foo, n))
        return self.foo.__dict__[n]

f = Foo()
print(f.b(f.a, 2))
b = Bar(f)
print(b.b(b.a, 2))



