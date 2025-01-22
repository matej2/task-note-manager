# task-note-manager
App to manage task notes

# Run instructions

1. `pipenv install`
2. `pienv run python main.py`

# Build instructions

Before you build this app, note that antivirus may flag it as potencially malicious executable. This is normal, you should add an exception for file in your antivirus program.

1. `pipenv install --dev`
2. Get directory of virtual environment by running `pipenv --venv`
3. Run `pipenv run pyinstaller --paths <virtual env path> --noconsole --onefile main.py`. Option --noconsole will build app so that console window will not be displayed when running executable. Option --onefile will bundle all files into one executable. 