@echo off
rem Runs a command inside the VS 2022 x64 developer environment, so cl, cmake and ninja are on PATH.
rem usage: vsenv-build.cmd <command...>
call "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat" >nul
if errorlevel 1 exit /b 1
%*
