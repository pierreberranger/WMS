from models import SetOfPackages, Dimensions, Package, SetOfSomething

def display(set_of_something: SetOfSomething):
    base = "{:<10}|{:<25}|{:<10}"
    header = base.format('id','description','status')
    print(header)
    print ('='*len(header))
    for something in set_of_something:
        print(base.format(something.id, something.description, something.status))