--Рабочий вариант 1
image: 
  file:  .gitpod.Dockerfile

tasks:
  # - name: start
- before: |
    pyenv virtualenv flvenv
    source activate flvenv

    export FLASK_APP=learnflask
    export FLASK_ENV=development
      
    pip install flask
  init:  |
    echo "проверка init"
    #   source activate flvenv
    #   pip install Flask  


# List the start up tasks.   Learn more https://www.gitpod.io/docs/config-start-tasks/
# tasks:
#   - init: echo 'init script' # runs during prebuild
  command: flask run

# # List the ports to expose. Learn more https://www.gitpod.io/docs/config-ports/
ports:
  - port: 5000
    onOpen: open-preview

--Рабочий вариант 2    
