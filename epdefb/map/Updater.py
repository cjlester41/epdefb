class Updater:

    # Updater class would be thing that updates Maps
    # I'm thinking might be easier to store Maps in an object rather than in files. i.e. load files, store in memory, would be
    # faster to display. But if not, ditch Map class and just use this to pull down new files


    def __init__(self):
        self.faa_url = ""
        self.edition = get_current_edition()
        return

    def is_map_out_of_date(self):

    def download_maps(self):
        if is_map_out_of_date():
            # download map

