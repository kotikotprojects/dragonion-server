# 🐲 dragonion-server
Websocket chat server on-top of onion network for 
[dragonion](https://github.com/dragonionx/dragonion)

## 📜 Table of Contents
* [🐲 dragonion-server](#-dragonion-server)
  * [📜 Table of Contents](#-table-of-contents)
  * [🛣️ Usage plan](#%EF%B8%8F-usage-plan)
  * [🔖️ About](#%EF%B8%8F-about)
  * [💻 Usage](#-usage)
  * [⚙️ Configuration guide](#%EF%B8%8F-configuration-guide)
  * [📃 Credits](#-credits)

## 🛣️ Usage plan
1. Check [Table of Contents](#-table-of-contents) (optionally)
2. Read [About](#%EF%B8%8F-about) (optionally)
3. Read [Usage guide](#-usage)
4. Go to [Configuration guide](#%EF%B8%8F-configuration-guide), choose your platform,
navigate to opted installation method (they are arranged from most to least 
recommended)
5. Install pre-requirements, install app, run it, 
checking [usage guide](#-usage) if needed

## 🔖️ About
A configured and running dragonion-server is required for dragonion chat to work. 
Built on-top of dragonion-core, it implements work with the protocol and 
websockets server, that broadcasts and handles messages.

## 💻 Usage
To use dragonion-server, you need to install it first. To do this, you can visit
[Configuration guide](#%EF%B8%8F-configuration-guide).

dragonion-server is controlled from cli. When you run it in some location on your
disk, `data` folder with tor and `data.storage` config file are created. You should
keep them safe to avoid data and key leaks. Using `data.storage` file anyone can
start server on your onion service id.

#### Guide sections:
- [Getting help](#getting-help)
- [Running a service](#running-a-service)
- [Updating a service](#updating-a-service)
- [Removing a service](#removing-a-service)

#### Getting help
To check all available commands, you can run
```commandline
dragonion-server --help
```
To get help for specific command, you should run
```commandline
dragonion-server command-name --help
```
where `command-name` is name of existing command, for example
```commandline
dragonion-server service-run --help
```

#### Running a service
To use dragonion chat, you need to run onion service with dragonion-server. 
In this situation, service is an onion service, an anonymous network service 
that is exposed over the Tor network. dragonion-server runs service, that
points to local endpoint with running websocket server.

To run a service, you should run
```commandline
dragonion-server service-run --name SERVICE_NAME
```

Available command options:

- `-n` or `--name` is required and used to specify service name. If service with
this name exists in config, it will run with saved parameters (like port), and 
if not - new will be created
- `-p` or `--port` is used to specify port, where local server will be started.
It is saved to config file. Remember, that it isn't only port, that server will
take. You cannot control tor ports using this option. If not specified, random 
available will be picked.
- `-wt` (`--without-tor`) and `-ot` (`--only-tor`) are used mostly for development,
to separate the processes of the proxy and the server itself

After running this command, `tor` will start, and you will see that service is now
available on onion host. To connect to service, you should share two colorful
strings (orange and purple), that are service id and auth string, to your users.
Also, sharing `SERVICE_NAME.auth` file, that is created in working dir can be more
convenient for some users as connect option, so you should share it also.

[Backs to sections](#guide-sections)

#### Updating a service
You may have a situation where you need to update or write a service without 
actually starting it. In such cases, you can use the command provided below. 
It allows you to generate an id-key pair for a new name and overwrite the port 
for an existing name.

To run update a service, you should run
```commandline
dragonion-server service-write --name SERVICE_NAME --port PORT
```

Available command options:

- `-n` or `--name` is required and used to specify service name to write.
- `-p` or `--port` is required here and will rewrite port in settings.

[Backs to sections](#guide-sections)

#### Removing a service
In some situations, you may need to remove the service. In this case, you will no 
longer be able to run the server on the same id due to the nature of the tor 
network, so be careful with this. Also, do not forget that the loss of the 
`.storage` (config file) means no access to the service ID-key pair, which also 
means the loss of the ability to start the server without the possibility of 
recovery.

To run update a service, you should run
```commandline
dragonion-server service-remove --name SERVICE_NAME
```

Available command options:

- `-n` or `--name` is required and used to specify service name to remove.

[Backs to sections](#guide-sections)

## ⚙️ Configuration guide
- [Windows](#windows)
- [Linux](#linux)
- [MacOS](#macos)

### Windows
#### Pre-requirements:
- [Python3](https://www.python.org/downloads/) (with pip)
- [Git](https://git-scm.com/download/win)
- [Windows terminal](https://github.com/microsoft/terminal) is recommended, 
[install it from Microsoft Store](https://aka.ms/terminal)

#### Install options:
- [Use pipx](#use-pipx)
- [Clone repo and use venv](#clone-repo-and-use-venv)

##### Use pipx
pipx is a tool to help you install and run end-user applications written in Python.
It creates isolated environments for each application to install it.

Fresh installation:
```
pip install pipx
pipx ensurepath
pipx install git+https://github.com/dragonionx/dragonion-server
```
Launch options:
- After fresh install, re-run your shell, than run `dragonion-server` 
(it is in your PATH because of pipx)

Updating:

```commandline
pipx upgrade dragonion-server
```

[Back to Usage guide](#-usage)

##### Clone repo and use venv
Fresh installation:
```commandline
git clone https://github.com/dragonionx/dragonion-server
cd dragonion-server
python -m venv venv
venv\Scripts\activate
pip install .
```
Launch options:
- After fresh install, run `dragonion-server` in environment 
(or `python -m dragonion-server`)
- `cd` to app folder, run `venv\Scripts\activate`, than `dragonion-server` in 
environment (`python -m dragonion-server`)
- Run `dragonion-server.exe` from `venv\Scripts`. You can also copy it anywhere you
want, but remember that data and config files are saved near executable file

Updating:

`cd` to app directory, than 
```commandline
git pull
```
If there are new changes, run
```commandline
venv\Scripts\activate
pip install .
```

[Back to Usage guide](#-usage)

### Linux
#### Pre-requirements (install them via your package manager):
For x64/x86 systems:
- `python3` `python3-pip` `python3-venv`
- `git`

For arm (arm64, aarch64) systems:
- All from above
- `tor`

#### Install options:
- [Use pipx](#use-pipx-1)
- [Clone repo and use venv](#clone-repo-and-use-venv-1)

##### Use pipx
pipx is a tool to help you install and run end-user applications written in Python.
It creates isolated environments for each application to install it.

Install pipx:
```commandline
apt install pipx
```
or
```commandline
pip install pipx
```

Fresh installation:
```
pipx ensurepath
pipx install git+https://github.com/dragonionx/dragonion-server
```
You may use `python3 -m pipx` for this

Launch options:
- After fresh installation relaunch your shell (if pipx was previously installed,
you can skip this), than run `dragonion-server` (it is in your env because of pipx)

Updating:

```commandline
pipx upgrade dragonion-server
```

[Back to Usage guide](#-usage)

##### Clone repo and use venv
Fresh installation:
```commandline
git clone https://github.com/dragonionx/dragonion-server
cd dragonion-server
python3 -m venv venv
. venv/bin/activate
pip install .
```
Launch options:
- After fresh install, run `dragonion-server` in environment 
(or `python3 -m dragonion-server`)
- `cd` to app folder, run `. venv/bin/activate`, than `dragonion-server` in 
environment (`python3 -m dragonion-server`)
- Run `dragonion-server` from `venv\bin`. You can also copy it anywhere you
want, but remember that data and config files are saved near executable file

Updating:

`cd` to app directory, than 
```commandline
git pull
```
If there are new changes, run
```
. venv/bin/activate
pip install .
```

[Back to Usage guide](#-usage)


### MacOS
#### Pre-requirements (install them via your package manager):
- `python3` `python3-pip` `python3-venv`
- `git`

#### Install options:
- [Use pipx](#use-pipx-2)
- [Clone repo and use venv](#clone-repo-and-use-venv-2)

##### Use pipx
pipx is a tool to help you install and run end-user applications written in Python.
It creates isolated environments for each application to install it.

Install pipx:
```commandline
brew install pipx
```
or
```commandline
pip3 install pipx
```

Fresh installation:
```
pipx ensurepath
pipx install git+https://github.com/dragonionx/dragonion-server
```
You may use `python3 -m pipx` for this

Launch options:
- After fresh installation relaunch your shell (if pipx was previously installed,
you can skip this), than run `dragonion-server` (it is in your env because of pipx)

Updating:

```commandline
pipx upgrade dragonion-server
```

[Back to Usage guide](#-usage)

##### Clone repo and use venv
Fresh installation:
```commandline
git clone https://github.com/dragonionx/dragonion-server
cd dragonion-server
python3 -m venv venv
. venv/bin/activate
pip install .
```
Launch options:
- After fresh install, run `dragonion-server` in environment 
(or `python3 -m dragonion-server`)
- `cd` to app folder, run `. venv/bin/activate`, than `dragonion-server` in 
environment (`python3 -m dragonion-server`)
- Run `dragonion-server` from `venv\bin`. You can also copy it anywhere you
want, but remember that data and config files are saved near executable file

Updating:

`cd` to app directory, than 
```commandline
git pull
```
If there are new changes, run
```
. venv/bin/activate
pip install .
```

[Back to Usage guide](#-usage)


## 📃 Credits
- [OnionShare project](https://github.com/onionshare) - code inspiration for 
integrating application with tor
