<div style="text-align:center"><img src="https://github.com/OT-Rax/swsb-project/blob/main/logo.png" width="200"></div>

# Librachain project
Software Security and Blockchain course project.
The goal is implementing blockchain sharding by splitting the distributed ledger into multiple blockchains.

### Requirements
To run our application you need to have installed:
* [Python3.10 or higher](https://www.python.org/downloads/release/python-3100/)
* [Pip](https://pip.pypa.io/en/stable/installation/)
* [Solc 0.8.19](https://docs.soliditylang.org/en/latest/installing-solidity.html)
* [Solc-select](https://pypi.org/project/solc-select/)
* [Docker](https://docs.docker.com/engine/install/)
* [Docker-compose](https://docs.docker.com/compose/install/linux/)

#### Setting up the solidity compiler

The solidity compiler can be installed in different ways, such as using your operating system packet manager or pip.
Make sure `solc` is in your PATH (e.g. by adding $HOME/.local/bin to your path if you have installed it via pip).
The newer solidity compiler versions has some compatibility problems with the other libraries. 
We highly suggest to install the 0.8.19 solidity compiler version in order to avoid them. 
The `solc-select` package allows to switch between different versions, if you have installed it you can run:

```
solc-select install 0.8.19
solc-select use 0.8.19
```

This will ensure that you are using the 0.8.19 solidity compiler version.

### How to setup our program in your PC 

* [Setup in UNIX-like OS's](#setupunix)
* [Setup in Windows](#setupwin)

<a name="setupunix"></a>
#### Setup in UNIX-like OS's
1. First you need to clone this repository.
```
  git clone https://github.com/OT-Rax/swsb-project
```
2. You can change the configuration parameters in the *configuration.yml* file inside the config folder.
3. Then, you need to run the *install.sh* file. In order to do this, you first need to make this file executable with the command *chmod +x install.sh*. This file will start the containers.
```
  chmod +x install.sh
  ./install.sh
```
4. Finally you can run the *run.sh* file to start the program. Again, remeber to make this file executable before executing it.
```
  chmod +x run.sh
  ./run.sh
```

<a name="setupwin"></a>
#### Setup in Windows
To setup the application on windows, you need to run the following files in the specified order:
1. `docker-compose.yml`
2. `deploy_on_chain.py`
3. `set_up.py` (optional)
4. `main.py`


### Documentation
In this section you can find the documentation of our project: [Documentation](mettilink)

### Contributors
| Contributor name | Contacts |
| :-------- | :------- | 
| `El Mechri Rahmi`     | rahmi.elmechri@gmail.com | 
| `Giuliani Rebecca`     | giuliani.rebecca1999@gmail.com | 
| `Gobbi Chiara`     | chiaragobbi2001@gmail.com | 
| `Moretti Alice`     | morettialice@outlook.it | 
| `Ronci Arianna`     | ariannaronci15@gmail.com | 
