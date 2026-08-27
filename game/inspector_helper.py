import inspect

# Method Resolution Order

def inspect_mro(cls):
    print(f"\nMRO for {cls.__name__}:")

    for base in cls.__mro__:
        print(
            f"  {base.__module__}.{base.__name__}"
        )
            #  class module, resolution order dict keys
def inspect_class(cls):
    print("=" * 60)
    print(f"CLASS:   {cls.__name__}")
    print(f"MODULE:  {cls.__module__}")
    print(f"MRO:     {cls.__mro__}")
    print(f"DICT:    {cls.__dict__.keys()}")
    print("=" * 60)
