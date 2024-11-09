#!/bin/bash

VENV_DIR=".bookbridge"
SCRIPT_PATH="$(cd "$(dirname "$0")"; pwd -P)"
PYTHON_EXEC="$SCRIPT_PATH/$VENV_DIR/bin/python"
PIP_EXEC="$SCRIPT_PATH/$VENV_DIR/bin/pip"

build() {
  if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment in $VENV_DIR..."
    python3 -m venv $VENV_DIR
  else
    echo "Virtual environment $VENV_DIR already exists."
  fi

  # Verifica se o Python da venv está no caminho correto
  if [[ "$($PYTHON_EXEC -c 'import sys; print(sys.prefix)')" == "$SCRIPT_PATH/$VENV_DIR" ]]; then
    echo "Python is correctly using the virtual environment: $PYTHON_EXEC"
  else
    echo "Warning: Python is not using the virtual environment. Check your venv settings."
    return 1
  fi

  # Instala as dependências se o requirements.txt existir
  if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    $PIP_EXEC install -r requirements.txt
  else
    echo "No requirements.txt file found. Skipping dependency installation."
  fi

  echo "Build completed successfully."
}

start() {
  if [ -d "$VENV_DIR" ]; then
    echo "Virtual environment at $VENV_DIR is ready to use."
    echo "To use the 'bookbridge' command, add the following line to your ~/.bashrc or ~/.zshrc:"
    echo "alias bookbridge='bash $SCRIPT_PATH/bookbridge.sh'"
  else
    echo "Virtual environment $VENV_DIR not found. Please run 'bookbridge build' first."
  fi
}

test() {
  if [ -d "$VENV_DIR" ]; then
    $PYTHON_EXEC -m pytest tests/
  else
    echo "Virtual environment $VENV_DIR not found. Please run 'bookbridge build' first."
  fi
}

install() {
  if [ -d "$VENV_DIR" ]; then
    $PIP_EXEC install $@
    $PIP_EXEC freeze > requirements.txt
    echo "New dependencies installed and saved to requirements.txt"
  else
    echo "Virtual environment $VENV_DIR not found. Please run 'bookbridge build' first."
  fi
}

refresh_dependencies() {
  $PIP_EXEC install -r requirements.txt
}

command() {
  if [ -d "$VENV_DIR" ]; then
    $PYTHON_EXEC $@
  else
    echo "Virtual environment $VENV_DIR not found. Please run 'bookbridge build' first."
  fi
}

case "$1" in
  build) build ;;
  start) start ;;
  test)  test ;;
  install) install ;;
  refresh ) refresh_dependencies ;;
  *) shift; command $@ ;;  # Qualquer comando não identificado será passado para o ambiente virtual usando o Python da venv
esac
