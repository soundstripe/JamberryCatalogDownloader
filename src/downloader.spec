# -*- mode: python -*-

extracticc_path = './argyll/bin/extracticc.exe'
cctiff_path = './argyll/bin/cctiff.exe'
sRGB_path = './argyll/ref/sRGB.icm'

block_cipher = None


a = Analysis(['downloader.py'],
             pathex=[],
             binaries=[],
             datas=[
                 (extracticc_path, 'argyll/bin'),
                 (cctiff_path, 'argyll/bin'),
                 (sRGB_path, 'argyll/ref'),
             ],
             hiddenimports=[],
             hookspath=[],
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
          name='downloader',
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
               name='Jamberry Image Downloader',
               icon='downloader.ico')
