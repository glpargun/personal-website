import datetime

def constructor(year):
    name = 'Galip Argun'
    traits = ['Engineer', 'DEV']
    age = datetime.datetime.today().year - year
    print(name, traits, age)

constructor(1994)