from importer import Importer
from downloader import Downloader


class Updater:
    def update_all(self):
        total_count = 0
        for dataset in Downloader.download_all():
            total_count += Importer.from_lines(dataset)
        print("Inserted ", total_count)



