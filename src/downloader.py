import os, subprocess, shutil, os.path
import tempfile
from configparser import ConfigParser
from multiprocessing.dummy import Pool
from pathlib import Path
from typing import Iterable
from urllib.request import urlretrieve
import logging
import jamberry
import sys

extracticc_path = r'argyll\bin\extracticc.exe'
cctiff_path = r'argyll\bin\cctiff.exe'
sRGB_path = r'argyll\ref\sRGB.icm'


def download(args):
    url, download_path = args
    urlretrieve(url, filename=download_path)
    logging.debug(f'downloaded {download_path}')


def correct_colors(destination_dir):
    destination_dir = Path(destination_dir)
    jpg_files = destination_dir.glob('*.jpg')

    logging.info('beginning color profile conversions')
    with tempfile.TemporaryDirectory(prefix='downloader.py') as tmp_converted:
        FNULL = open(os.devnull, 'w')
        for source_jpg_path in jpg_files:
            destination_jpg_path = Path(tmp_converted) / source_jpg_path.name
            extracted_icc_path = destination_dir / (source_jpg_path.name + '.icc')
            subprocess.call(
                [extracticc_path, str(source_jpg_path), str(extracted_icc_path)],
                stderr=FNULL, stdout=FNULL
            )
            if extracted_icc_path.exists():
                subprocess.call([cctiff_path,
                                 '-ip', str(extracted_icc_path),
                                 '-ip', sRGB_path,
                                 str(source_jpg_path), str(destination_jpg_path)
                                 ], stderr=FNULL, stdout=FNULL
                                )
                extracted_icc_path.unlink()
                if destination_jpg_path.exists():
                    shutil.copy(destination_jpg_path, source_jpg_path)
                logging.debug(f'applied icc profile from {source_jpg_path}')
        FNULL.close()
    logging.info('finished color profile conversions')


def download_items(products: Iterable[jamberry.Product], download_dir_path, removed_products_path, new_only=True):
    download_dir_path = Path(download_dir_path)
    removed_products_path = Path(removed_products_path)
    download_dir_path.mkdir(exist_ok=True)
    removed_products_path.mkdir(exist_ok=True)

    all_products = [p for p in products if not p.nas_design]

    catalog_slugs = {p.slug for p in all_products}
    existing_slugs = {j.stem for j in download_dir_path.glob('*.jpg')}
    old_slugs = existing_slugs - catalog_slugs
    new_slugs = catalog_slugs - existing_slugs

    if new_only:
        download_list = list(gen_download_list(download_dir_path, (p for p in all_products if p.slug in new_slugs)))
    else:
        download_list = list(gen_download_list(download_dir_path, all_products))
    logging.info(f'begin {len(download_list)} downloading images')
    Pool(4).map(download, download_list)
    logging.info('end downloading images')

    removed_products_path.mkdir(exist_ok=True)
    # check for existing jpgs that are not in the list of all products
    for slug in old_slugs:
        src_p = download_dir_path / f'{slug}.jpg'
        dest_p = removed_products_path / f'{slug}.jpg'
        shutil.move(str(src_p), str(dest_p))
        logging.info(f'moved old jpg {src_p}')


def gen_download_list(download_dir_path, products):
    yield from ((p.img, download_dir_path / f"{p.slug}.jpg") for p in products)


def fetch_jsons():
    logging.info('getting product catalog json')
    ws = jamberry.JamberryWorkstation()
    result = ws.fetch_autocomplete_json()
    return result.values()


def configure_logging(config):
    logging.basicConfig(
        format='%(asctime)s %(levelname)s: %(message)s',
        filename=config['downloader']['log_location'],
        level=logging.INFO
    )


def main():
    config = get_config(str(Path('~/Documents/catalog_downloader.ini').expanduser()))
    destination_dir = config['downloader']['catalog_folder']
    removed_dir = config['downloader']['removed_files_folder']
    new_only = config['downloader'].getboolean('new_only')
    username = config['credentials']['username']
    password = config['credentials']['password']
    configure_logging(config)
    ws = jamberry.JamberryWorkstation(username=username, password=password)
    all_products = ws.catalog_products()
    download_items(all_products, destination_dir, removed_dir, new_only=new_only)
    correct_colors(destination_dir)


def get_config(file_path):
    config = ConfigParser(interpolation=None)
    config['credentials'] = {
        'username': 'username',
        'password': 'password',
    }
    config['downloader'] = {
        'catalog_folder': '%USERPROFILE%\\Documents\\Catalog Images',
        'removed_files_folder': '%USERPROFILE%\\Documents\\Catalog Images (removed)',
        'log_location': '%USERPROFILE%\\Documents\\catalog_downloader.log',
        'new_only': True,
    }
    if not Path(file_path).exists():
        with Path(file_path).open('w') as f:
            config.write(f)
        os.startfile(file_path)
        sys.exit()
    config.read([file_path])
    config['downloader']['catalog_folder'] = os.path.expandvars(
        config['downloader']['catalog_folder'])
    config['downloader']['removed_files_folder'] = os.path.expandvars(
        config['downloader']['removed_files_folder'])
    config['downloader']['log_location'] = os.path.expandvars(
        config['downloader']['log_location'])
    return config


if __name__ == '__main__':
    main()
