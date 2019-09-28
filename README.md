# SBB-Surprise app

App for HackZurich 2019

## Usage
#### Start UI(Client)
```
  cd ui/
  yarn install
  yarn start
```

#### Start Server
```
  cd service
  virtualenv -p Python3 .
  source bin/activate
  pip install -r requirements.txt
  FLASK_APP=app.py flask run

```

Template example: https://towardsdatascience.com/create-a-complete-machine-learning-web-application-using-react-and-flask-859340bddb33
