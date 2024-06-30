class Input:

    # Input class would be responsible for gathering input from display, regardless of if raspberry pi or emulator
    # Consider not even checking if it's a raspberry pi or emulator here, but instantiating the class with that information
    def __init__(self, display):
        self.display = display


