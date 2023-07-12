class Size():

    # Class initializer. It has 5 custom parameters, with the
    # special `self` parameter that every method on a class
    # needs as the first parameter.
    def __init__(self, id, carets, price ):
        self.id = id
        self.carets = carets
        self.price = price
        
new_size = Size(1, 0.5, 405)