# -*- mode: python -*-

block_cipher = None
extracticc_path = './src/argyll/bin/extracticc.exe'
cctiff_path = './src/argyll/bin/cctiff.exe'
sRGB_path = './src/argyll/ref/sRGB.icm'

a = Analysis(['src\\downloader.py'],
             pathex=['C:\\Users\\steve\\Downloads\\JamberryCatalogDownloader', 'C:\\Users\\steve\\Downloads\\JamberryCatalogDownloader'],
             binaries=[],
             datas=[
                 (extracticc_path, 'argyll/bin'),
                 (cctiff_path, 'argyll/bin'),
                 (sRGB_path, 'argyll/ref'),
             ],
             hiddenimports=[],
             hookspath=['c:\\users\\steve\\py_jamberry_api\\lib\\site-packages\\pyupdater\\hooks'],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='win',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='win',
               icon='downloader.ico')
