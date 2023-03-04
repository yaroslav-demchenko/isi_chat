## Installing using GitHub

```shell
git clone https://github.com/yaroslav-demchenko/isi_chat.git
cd isi_chat
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
