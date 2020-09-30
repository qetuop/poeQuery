# poeQuery
git clone https://github.com/qetuop/poeQuery.git poeq
cd poeq
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp config.json.default config.json
# edit config.json

python3 test.py 
