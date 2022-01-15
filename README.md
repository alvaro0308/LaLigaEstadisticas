## LaLigaEstadisticas

[![GitHub Action 
Status](https://github.com/alvaro0308/LaLigaEstadisticas/actions/workflows/workflow.yaml/badge.svg)](https://github.com/alvaro0308/)

### Install dependencies
```
pip3 install --ignore-installed -r requirements.txt 
sudo apt install ruby ruby-dev rubygems build-essential
sudo gem install --no-document fpm
```

### Instructions to test:
```
fbs run
```

### Instructions to create installer (.deb, .exe or .dmg):
```
fbs freeze
fbs installer
```

### Instructions to install .deb:
```
sudo dpkg -i target/LaLigaEstadisticas.deb
```

### Instructions to install .exe:

Open target/LaLigaEstadisticasSetup.exe


## Keys path to database access

keys: keys/keys.json

![](https://github.com/alvaro0308/LaLigaEstadisticas/blob/master/src/main/resources/gif.gif)