# rubix-cli
command line tools for interacting with MCUs running MicroPython

### Description
after some time of using shell utils built on top of the `pyboard.py` (using telnetlib which has been deprecated & removed in Python 3.13) I decided to build my own toolset for interacting with MicroPython boards.

### Features
- pure Python, no 3rd party dependencies
- `termios` used for serial port communication.
- various commands for files & system management.
- type hinted
- tests coverage.

### Compatibility
program has been tested on RP2040W & ESP32 devkit boards, both running MicroPython v1.25

### How to use it
package can be installed via `pip` just add following line to your
`requirements.txt`.

```
rubix-cli @ git+https://github.com/zNitche/rubix-cli.git@<version>
```

after that verify installation
```
rubix-cli --version
```

### Examples
```
rubix-cli --help
```

- list all available commands with accepted parameters
```
rubix-cli --commands
```

- list all files stored at root directory of MCU
```
rubix-cli --device /dev/tty1 --cmd ls /
```

- wipe device
```
rubix-cli --device /dev/tty1 --cmd purge
```

- flash board
```
rubix-cli --device /dev/tty1 --cmd flash ./source
```

this will copy content of `./source` directory to `/` directory on MCU, for control over what to copy, `.flashignore` file should be created in `./source` directory. 

##### Example .flashignore
```
/.DS_Store
/.git
/.github
/.gitignore
^/commands
lightberry_config.template.json
pyproject.toml
README.md
LICENSE
requirements.txt
```

- preview REPL 
```
rubix-cli --device /dev/tty1 --cmd cat_repl
```

this simple utility allows you to preview what is being written to MicroPython shell. 

For more advanced interactions use `screen` or `minicom` programs.

### Development setup
for smooth development, package should be installed in editable mode

```
pip3 install -e .
```

### Tests
all available commands have full tests coverange. 

Note that running tests requires connected MCU running supported MicroPython version.

##### Install tests dependencies
```
pip3 install -r requirements/tests.txt
```

##### Run tests
`WARNING - All files stored on microcontroller will be removed`

```
pytest -v ./tests --device /dev/tty1
```

### Resources
- [docs.micropython.org](https://docs.micropython.org/en/latest/reference/repl.html)
- [man7.org](https://man7.org/linux/man-pages/man3/termios.3.html)
