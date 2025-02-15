from pathlib import Path
from shutil import copyfile
from threading import Thread
import logging
import argparse

parser = argparse.ArgumentParser(description="Sorting folder")
parser.add_argument("--source", "-s", help="Source folder", required=True)
parser.add_argument("--output", "-o", help="Output folder", default="dist")

args = vars(parser.parse_args())
source = Path(args["source"])
output = Path(args["output"])

folders = []

def grabs_folder(path: Path):
    for el in path.iterdir():
        if el.is_dir():
            folders.append(el)
            grabs_folder(el)


def copy_file(path: Path):
    for el in path.iterdir():
        if el.is_file():
            ext = el.suffix[1:]
            ext_folder = output / ext
            try:
                ext_folder.mkdir(exist_ok=True, parents=True)
                copyfile(el, ext_folder / el.name)
                logging.info(f"Copied {el} to {ext_folder}")
            except OSError as err:
                logging.error(f"Error copying {el}: {err}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(threadName)s %(message)s")

    folders.append(source)
    grabs_folder(source)

    threads = []
    for folder in folders:
        th = Thread(target=copy_file, args=(folder,))
        th.start()
        threads.append(th)

    for th in threads:
        th.join()

    logging.info(f"Sorting completed. All files moved to {output}")
