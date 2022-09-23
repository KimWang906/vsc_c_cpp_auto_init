@echo off

REM WRITTEN BY HOPLIN / 2021.10.30 / VSCode C_C++ ENV AUTO INITIATOR : MINGW GCC/G++ COMPILER

REM Directory : Save the directory where the batch file was called.
set currentpath="%1"
REM Directory : Save the directory where the batch file saved
set batchpath=%~p0
REM Directory : Save the directory where the configuration files saved
set settingfiles=%~p0vscode

set copypath=C:%batchpath%vscode

xcopy %copypath%\*.* %currentpath%\.vscode\ /e /h /k