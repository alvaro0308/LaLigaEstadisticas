## LaLigaEstadisticas

[![GitHub Action 
Status](https://github.com/alvaro0308/LaLigaEstadisticas/actions/workflows/workflow.yaml/badge.svg)](https://github.com/alvaro0308/)

### Install dependencies
```
pip3 install --ignore-installed -r requirements.txt 
sudo apt install ruby ruby-dev rubygems build-essential
sudo gem install --no-document fpm
```

### Test:
```
fbs run
```

### Creating installer .deb, .exe or .dmg (It can be downloaded from Releases):
```
fbs freeze
fbs installer
``` 

### Installing .deb:
```
sudo dpkg -i target/LaLigaEstadisticas.deb
```

### Installing .exe:

Open target/LaLigaEstadisticasSetup.exe

## Keys path to database access

keys: keys/keys.json

# Example
![](https://github.com/alvaro0308/LaLigaEstadisticas/blob/master/src/main/resources/gif.gif)
