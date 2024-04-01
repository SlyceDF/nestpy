set /p version=Enter version:
set /p t=Is this a release (Y/[N])?
if /I "%t%" neq "Y" set test=--test
python presetup.py %test% --version %version%