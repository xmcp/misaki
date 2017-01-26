import sys
import os,shutil
from cx_Freeze import setup, Executable
base = None
executables = [Executable(script='misaki.py',
               base=base,
               targetName="Misaki.exe",
               compress=True),]
setup(name='Misaki',
      version='1.0',
      description='Misaki Broadcast Toolbar',
      executables=executables,
      options={'build_exe':{'optimize':2}},)

print('===== CLEANING UP =====')

#os.remove('build/exe.win32-3.4/unicodedata.pyd')
# os.remove('build/exe.win32-3.4/_hashlib.pyd')
# os.remove('build/exe.win32-3.4/_elementtree.pyd')
# os.remove('build/exe.win32-3.4/_ssl.pyd')
shutil.rmtree('build/exe.win32-2.7/tcl/tzdata')
shutil.rmtree('build/exe.win32-2.7/tcl/msgs')
shutil.rmtree('build/exe.win32-2.7/tcl/encoding')
shutil.rmtree('build/exe.win32-2.7/tk/demos')
shutil.rmtree('build/exe.win32-2.7/tk/images')
shutil.rmtree('build/exe.win32-2.7/tk/msgs')

os.rename('build/exe.win32-2.7','build/Misaki-exe.win32-2.7')

print('===== DONE =====')

