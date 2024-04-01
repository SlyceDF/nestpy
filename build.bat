@echo off
set /p version=Enter version:
set /p t=Is this a release (Y/[N])?
if /I "%version%" == "" set version=.
if /I "%t%" neq "Y" set test=--test
python presetup.py %test% --version %version%