cd ./build
del *.teal
cd ..

python ./src/contract/escrow_account.py >> ./build/escrow_account.teal

python ./src/deploy.py
pause