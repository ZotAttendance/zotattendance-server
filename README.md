# ZotAttendance
This repository hosts the prototype for ZotAttendance, which allows students to indicate their physical presence for the class.

## Getting Started
1. Install Python 3.7+
2. Set up a virtual environment
   + Windows
     + Run `python -m venv .`, `cd Scripts`, and `activate` inside project directory
     + Execute `pip install flask`
   + Linux
     + Run `python3 -m venv .`, `cd bin`, and `source ./activate` inside project directory
     + Execute `pip install flask`
3. Type `export FLASK_ENV=development`
4. Start the application with `flask run`

## Deployment
1. Follow step one and two from the "Getting Started" section
2. Install UWSGI with ```pip install uwsgi```
3. Install systemd service file which runs uwsgi
    ```
    [Unit]
    Description=ZotAttendance
    After=network.target

    [Service]
    User=www-data
    WorkingDirectory=/home/user/zotattendance-server
    Environment="PATH=/home/user/zotattendance-server/bin"
    ExecStart=/home/user/zotattendance-server/bin/uwsgi --ini zotattendance.ini
    Restart=always

    [Install]
    WantedBy=multi-user.target
    ```
4. Add uwsgi sock as a backend to nginx
    ```
    location / {
        include uwsgi_params;
        uwsgi_pass unix:/home/user/zotattendance-server/zotattendance.sock;
    }
    ```

## Credits
+ Yizhen Liu
+ Surya Teja Palavalasa
+ Duo Wang
