@echo off
chcp 65001

cd C:\Users\%username%\Desktop\Work\Other\pySocket

if "%1" == "" (
    set clients=1
) else (
    set clients=%1
)

for /l %%i in (1 1 %clients%) do (
    echo Client %%i has connected.
    start cmd /k python main.py
)