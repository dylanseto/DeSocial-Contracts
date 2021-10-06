REM Clean Teal Scripts
md "build" 2>NUL
md "lib" 2>NUL

cd ./build
del *.teal
cd ..

cd ./lib
del *.js
cd ..

cd ./src
del contract_config.py
cd ..

REM Build Smart Contracts from Python to Teal - the escrow account script is compile later in deploy.py
python ./src/contract/createPost.py >> ./build/createPost.teal
python ./src/contract/createAccount.py >> ./build/createAccount.teal
python ./src/contract/clearProgram.py >> ./build/clearProgram.teal

REM Compile, Deploy and setup TEAL Smart Contracts
python ./src/deploy.py
python ./src/deploy_account_application.py
python ./src/setupContract.py

REM Format JS file with ESLint
cd ./lib
npx eslint .\contracts.js --fix
pause