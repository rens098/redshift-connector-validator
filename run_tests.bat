@echo off

echo Clearing Cache...

pytest --cache-clear

echo Cache cleared!

echo Validation in progress...

call py -m pytest script_test.py -vv -s > result_output.txt

type result_output.txt

echo Validation completed!

echo Check results_output.txt for more details

pause