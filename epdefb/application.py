# Main application
import os

# (1) Determine if we are running on raspberry pi or emulator
# If ENV environmental variable is not set, assume Production (Raspberry Pi environment)
environment = getattr(os.environ['ENV'], "Production")
if environment == "Emulator":
    # Spin up flask app

# (3) Run your while loop using the Interface class

# TODO: How do you expect to update the maps? On startup? Periodically with cronjob? Prior to shutdown? This will determine if
#       Updater is even used here. Right now it feels like we're overloading the purpose of the repo. If it's not something
#       you want to run as a part of the application.py, perhaps we have two main applications.. app_epdefb and app_update
