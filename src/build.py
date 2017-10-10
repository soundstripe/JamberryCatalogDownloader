import subprocess, sys

adv_installer_path = r"C:\Program Files (x86)\Caphyon\Advanced Installer 14.3\bin\x86\AdvancedInstaller.com"

def main():
    result = subprocess.run([
        'pyinstaller',
        '--distpath=..\\dist',
        '--workpath=..\\build',
        '--noconfirm',
        'downloader.spec',
    ])
    if result.returncode != 0:
        sys.exit()
    result = subprocess.run([
        adv_installer_path,
        '/build', 'Jamberry Catalog Downloader.aip',
    ])


if __name__ == '__main__':
    main()
