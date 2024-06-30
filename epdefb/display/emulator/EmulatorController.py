class EmulatorController:

    # I would consider this class a good way to handle flask app routes
    # I'm not sure what the pattern is for flask, but I don't think handling routes in a separate class' method
    # makes sense. At the very least, this pulls out routes into something more manageable.

    def __init__(self):
        return