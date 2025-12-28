# rubix-cli
MicroPython REPL emulator for Unix


```
pip3 install -e .
```

```
rubix-cli --commands
```

```
rubix-cli --device /dev/tty1 --cmd ls /test
```

```
pip3 install -r requirements/tests.txt
pytest -v ./tests
```


### Resources
- [docs.micropython.org](https://docs.micropython.org/en/latest/reference/repl.html)
- [man7.org](https://man7.org/linux/man-pages/man3/termios.3.html)
