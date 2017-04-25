#!/bin/bash

### instala a stack de comandos do python2.7
#sudo apt-get install python-dev

### instala o setuptools, pip e easy_install na nova stack do python2.7
#curl https://bootstrap.pypa.io/get-pip.py | python2.7

### cria virtualenv
virtualenv --python=python2.7 venv

# instala dependencias do python ou termina com erro
function pip_install_req() {
  local requirement_file=$1
  ./venv/bin/pip install -r "$requirement_file"

  local pip_return_code=$?
  if [ "$pip_return_code" -ne "0" ]; then
    echo "Error on install pip requirements, quiting..."
    exit $pip_return_code
  fi
}

# seleciona quais tipos de dependencias deve instalar
case $1 in
  'dev')   pip_install_req requirements/dev.txt  ;;
  'prod')  pip_install_req requirements/prod.txt ;;
  *)       pip_install_req requirements/prod.txt ;;
esac

echo "---"
echo "Now you need to load your virtualenv:"
echo "$ source venv/bin/activate"
echo
echo "To check if virtualenv is enabled:"
echo "$ which python2.7"
exit 0
