REM Clean Teal Scripts
md "build" 2>NUL
md "lib" 2>NUL

cd ./build
del *.teal
cd ..

cd ./lib
del *.js
cd ..

REM Build Smart Contracts from Python to Teal - the escrow account script is compile later in deploy.py
python ./src/contract/createPost.py >> ./build/createPost.teal
python ./src/contract/clearProgram.py >> ./build/clearProgram.teal

REM Compile & Deploy TEAL Smart Contracts
python ./src/deploy.py
pause