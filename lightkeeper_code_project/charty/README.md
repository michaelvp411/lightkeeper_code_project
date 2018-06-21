# Charty - A Mutli-line Graph Web App

## Overview
A simple multi-graph D3 chart web app using the Python Flask as the framework and server. Yarn is used to manage JS/CSS package dependencies. For deployment, systemd manages the Flask app as a web service. The project is intended for DevOps job candidate roles. 

## Requirements
- [Ubuntu Server 16.04 LTS](http://releases.ubuntu.com/16.04.4/)
- [git](https://git-scm.com/)
- [Python](https://www.python.org/)
- [pip](https://pip.pypa.io/en/stable/)
- [Flask](http://flask.pocoo.org/)
- [Node.js](https://nodejs.org/en/)
- [Yarn](https://yarnpkg.com/en/)
- [D3.js](https://d3js.org/)
- [systemd](https://www.freedesktop.org/wiki/Software/systemd/)
- stocks.csv
- System user name and group name called _ubuntu_ with `sudo` permission
- a code directory set as _/home/ubuntu/Code/lib_.

## App Dependency Setup
The web app requires Python with `pip` and NPM (Node.js) to manage packages. Python 3 is installed by default on Ubuntu Server 16.04 LTS. Python 2.7 can also be used, and installed seperately using `apt`. To install `pip` and Node.js, use `apt` with SUDO permissions for the _ubuntu_ system user account.

#### On Ubuntu 16.04 LTS
```shell
$: sudo apt install update && apt -y upgrade

$: sudo apt install -y python-pip 

$: sudo pip install --upgrade pip

$: curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -

$: sudo apt install -y nodejs
```

### Back-end Dependencies
Use `pip` to install the Python packages listed in _requirements.txt_. 

```shell
$: sudo pip install -r requirements.txt
```

### Front-end Dependencies
The node package manager, [NPM](https://www.npmjs.com/), is automatically installed with **Node.js**. The `npm` command will be used to install **Yarn** for doing JavaScript/CSS dependency management and minifying the static files. 

```shell
$: sudo npm install -g yarn
```

A _package.json_ file is in the static directory. Using **Yarn**, you can run `yarn install` in the static directory. A _node_modules_ folder gets created and includes all the necessary JavaScript and CSS packages to be used in the web app. A _yarn.lock_ file is also generated (if it does not already exist). The lock file stores excatly which versions of each front-end dependency were installed. This is comparable to lockfiles in other package managers like Bundler or Cargo. It’s similar to npm’s `npm-shrinkwrap.json`, however it’s not lossy and it creates reproducible results.

## The CSV File
To load data into the **D3.js** chart,  _static/stocks.csv_ is read using a JavaScript API call in _static/main.js_ with 

```javascript
d3.csv("static/stocks.csv").then(function(data) { 
    // Read CSV file to visualize data here.
});
``` 
[Reference](https://github.com/d3/d3/blob/409ee406ebed323cebeb6bfecaf08641616e79ff/CHANGES.md#L10) 

The D3.js API call uses a [Promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise) to perform an asynchronous to the file system to read the stock CSV file and renders the chart. The _static/stock.csv_ contains public data of four tech trade symbols of Amazon (AMZN), Apple (AAPL), IBM (IBM), and Microsoft (MSFT) of their average price per month for 2000 - 2010. 
 
## The Server
### Running the Server
To serve the front-end of web application, **Flask** will provide the back-end support of the application. The core part of the web app is _app.py_. To run the application, use `python app.py`. The output will be: 

```
 $: /usr/bin/python app.py
 * Running on http://0.0.0.0:8000/ (Press CTRL+C to quit)
 192.168.112.1 - - [11/Apr/2018 18:06:04] "GET /static/node_modules/bootstrap/dist/css/bootstrap.min.css HTTP/1.1" 200 -
192.168.112.1 - - [11/Apr/2018 18:06:04] "GET /static/main.css HTTP/1.1" 200 -
192.168.112.1 - - [11/Apr/2018 18:06:04] "GET /static/node_modules/jquery/dist/jquery.min.js HTTP/1.1" 200 -
192.168.112.1 - - [11/Apr/2018 18:06:04] "GET /static/node_modules/popper.js/dist/umd/popper.min.js HTTP/1.1" 200 -
192.168.112.1 - - [11/Apr/2018 18:06:04] "GET /static/node_modules/bootstrap/dist/js/bootstrap.min.js HTTP/1.1" 200 -
192.168.112.1 - - [11/Apr/2018 18:06:04] "GET /static/node_modules/d3/dist/d3.min.js HTTP/1.1" 200 -
192.168.112.1 - - [11/Apr/2018 18:06:04] "GET /static/main.js HTTP/1.1" 200 -
192.168.112.1 - - [11/Apr/2018 18:06:04] "GET /static/node_modules/popper.js/dist/umd/popper.min.js.map HTTP/1.1" 200 -
192.168.112.1 - - [11/Apr/2018 18:06:04] "GET /static/node_modules/bootstrap/dist/js/bootstrap.min.js.map HTTP/1.1" 200 -
192.168.112.1 - - [11/Apr/2018 18:06:04] "GET /static/node_modules/bootstrap/dist/css/bootstrap.min.css.map HTTP/1.1" 200 -
192.168.112.1 - - [11/Apr/2018 18:06:04] "GET /static/stocks.csv HTTP/1.1" 200 -
```

The default port used is 8000. The app is now accessible in the web browser by going to http://server_or_ip_address:8000/. 

### Managing the Server
Ubuntu comes with **systemd** to managed daemon services. The **Flask** app can daemonized by copying _system/flask.service_ over to _/etc/systemd/system/_. Inside _flask.service_, there are a couple of important configurations:

1. A **user** and **group** is created named _ubuntu_ with `sudo` permission.
2. The _~/Code/lib_ directories are made to store the charty app.

Once these steps are completed, then **systemd** commands can be used. 
Systemd has several options to manage the app as a service. It can manage the Flask app server with `systemctl` for starting and stopping the service and `journalctl` for viewing logged information. 

**systemctl commands**:
```shell
$ sudo systemctl start flask.service

$: sudo systemctl status flask.service
● flask.service - Flask web server
   Loaded: loaded (/etc/systemd/system/flask.service; disabled; vendor preset: enabled)
   Active: active (running) since Wed 2018-04-11 18:44:21 UTC; 1min 1s ago
 Main PID: 19023 (python)
    Tasks: 1
   Memory: 12.6M
      CPU: 94ms
   CGroup: /system.slice/flask.service
           └─19023 /usr/bin/python /home/ubuntu/Code/lib/charty/app.py

Apr 11 18:44:21 lk-test-16 systemd[1]: Started Flask web server.
Apr 11 18:44:21 lk-test-16 python[19023]:  * Running on http://0.0.0.0:8000/ (Press CTRL+C to quit)

$: sudo systemctl stop flask.service
```

**journalctl command**
```shell
$ sudo journalctl -u flask.service
```




