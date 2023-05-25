import time

class CustomTimer:
    def __init__(self):
        try:
            self.timer = time.perf_counter
        except AttributeError:
            self.timer = time.time

    def time(self):
        return self.timer()

from pathlib import Path

def make_folder(path):
    try: 
        path.mkdir(parents=True)
    except:
        # Folder already exists
        pass
    return path

def create_path(results_path = "_out", id=None): 
    if id:
        for i in ["rgb", "sem", "lidar"]:
            save_dir = Path(results_path) / id / i
            make_folder(save_dir)
        return Path(results_path) / id 
    else:
        save_dir = Path(results_path)
        make_folder(save_dir)

RESULTS_PATH = Path("_out")
make_folder(RESULTS_PATH)
