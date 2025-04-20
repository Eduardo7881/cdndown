# CDNdown - Python CDN Package Manager
#
# Licensed under MIT License
# Author: EduardoPlayss121

import os
import sys
import requests
import zipfile
import shutil
from tqdm import tqdm
from urllib.parse import urlparse

def download_zip(zip_url, zip_filename):
    print(f"[INFO] Downloading from: {zip_url}")

    response = requests.get(zip_url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024

    with open(zip_filename, "wb") as file, tqdm(
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024,
        desc="Downloading",
        ascii=True
    ) as bar:
        for data in response.iter_content(block_size):
            bar.update(len(data))
            file.write(data)

def extract_zip(zip_filename, output_path):
    with zipfile.ZipFile(zip_filename, 'r') as zip_ref:
        file_list = zip_ref.namelist()
        print(f"[INFO] Extracting {len(file_list)} files...")

        os.makedirs(output_path, exist_ok=True)

        with tqdm(total=len(file_list), desc="Extracting", ascii=True) as bar:
            for file in file_list:
                zip_ref.extract(file, output_path)
                bar.update(1)

def list_downloaded_packages(output_base="python-packages"):
    print(f"Listing packages in: {output_base}")
    if not os.path.exists(output_base):
        print("\nNo packages installed.")
        return
    
    packages = sorted(os.listdir(output_base))
    if not packages:
        print("\nNo packages installed.")
        return
    
    for pkg in packages:
        print(f" - {pkg}")

def show_help():
    print("Usage: cdndown.py [argument] or <url>")
    print("Argument list:\n")
    print("--help or -h              # Shows this message")
    print("--list or -l              # Lists the installed packages.")
    print("--remove or -r <pkg_name> # Removes a package")
    return

def remove_package(package_name, output_base="python-packages"):
    package_path = os.path.join(output_base, package_name)
    if os.path.exists(package_path) and os.path.isdir(package_path):
        shutil.rmtree(package_path)
        print(f"[OK] Removed package: {package_name}\n")
    else:
        print(f"[ERROR] Package not found: {package_name}\n")

def main():
    if len(sys.argv) == 1:
        print(f"Usage: cdndown.py <url>")
        print(" cdndown.py [argument]")
        print(" cdndown.py --help")
        sys.exit(1)

    if sys.argv[1] == "--list" or sys.argv[1] == "-l":
        list_downloaded_packages()
        sys.exit(0)

    if sys.argv[1] == "--help" or sys.argv[1] == "-h":
        show_help()
        sys.exit(0)

    if sys.argv[1] == "--remove" or sys.argv[1] == "-r":
        if len(sys.argv) != 3:
            print("[ERROR] You must specify a package name to remove.")
            print("Usage: cdndown.py --remove <package-name>")
            sys.exit(1)
        remove_package(sys.argv[2])
        sys.exit(0)

    zip_url = sys.argv[1]
    parsed = urlparse(zip_url)
    zip_filename = os.path.basename(parsed.path)

    if not zip_filename.endswith(".zip"):
        print("[ERROR] The link must point to a .ZIP file")
        sys.exit(1)

    package_name = zip_filename[:-4]
    output_base = "python-modules"
    output_path = os.path.join(output_base, package_name)

    try:
        download_zip(zip_url, zip_filename)
        extract_zip(zip_filename, output_path)
        os.remove(zip_filename)
        print(f"[OK] Package extracted to: {output_path}")
        print("\n[WARNING] This package may require other libraries.")
        print("          Dependencies are not installed automatically.")
    except Exception as e:
        print(f"[ERROR] Something went wrong. {e}")

if __name__ == "__main__":
    main()
