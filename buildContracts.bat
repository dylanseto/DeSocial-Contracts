REM Clean Teal Scripts
md "build" 2>NUL

cd ./build
del *.teal
cd ..

REM Build Smart Contracts from Python to Teal
python ./src/contract/escrow_account.py >> ./build/escrow_account.teal

REM Compile & Deploy TEAL Smart Contracts
python ./src/deploy.py
pause