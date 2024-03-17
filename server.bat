@echo off
chcp 65001

cd C:\Users\%username%\Desktop\Work\Other\pySocket
start cmd /k python server.py
echo Server has started.

if "%1" == "" (
    echo empty parameter.
) else (
    call .\clnt.bat %1
)