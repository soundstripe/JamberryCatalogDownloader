import subprocess, sys

version = '0.2.6'
adv_installer_path = r"C:\Program Files (x86)\Caphyon\Advanced Installer 14.3\bin\x86\AdvancedInstaller.com"


def main():
    result = subprocess.run([
        'pyinstaller',
        'build',
        'downloader.spec',
    ])
    if result.returncode != 0:
        print('build failed')
        sys.exit()
    result = subprocess.run([
        'pyupdater',
        'pkg',
        '-p',
    ])
    if result.returncode != 0:
        print('packaging failed')
        sys.exit()


if __name__ == '__main__':
    main()
