# Tyrano Save Reader  

![release](https://img.shields.io/github/v/release/Galactic647/Tyrano-Save-Reader?label=Release)

Tyrano save file `.sav` data are usually just json stored in an URL encoding or a percent-encoding. For example `@` will be encoded into `%40`.

This tool can convert `.sav` into `.json` and back. This tool also have a monitor function that keep track the changes between the save file and the parsed file, so you can edit the values without touching the save file.

-------------------

## Convert Usage

```cmd
usage: convert [-h] -i INPUT [-o OUTPUT]
```

options:

* `-h`, `--help`                 show this message and exit
* `-i INPUT`, `--input INPUT`    `.sav` or `.json` input file
* `-o output`, `--output OUTPUT` defaults to `auto` it will detect what output it should do, the location of the converted file is in the same location as the `INPUT`, the file name is default into `parsed.json` or `packed.sav`.

You often want to use this for settings which is usually also stored in `.sav` format. As a note, you should never monitor a setting file since it changes every time it got accessed.

Different from monitor function, the convert function has no checks of whether the `.sav` parsing or the `.json` parsing will give the correct output. If no error shows up then the problem might get masked, but most of the time this isn't really a problem.

### Example usage

* `convert -i "C:\Game Folder\Game\game_tyrano_data.sav"`
* `convert -i "C:\Game Folder\Game\parsed.json" -o "Parsed Saves\game_data_repacked.sav"`

-------------------

## Monitor Usage

```cmd
usage: monitor [-h] -i INPUT [-o OUTPUT] [-c CPS] [-b BUFFER] [-s] [-k BACKUP_LIMIT] [-l {debug,info,warning,error,critical}]
```

options:

* `-h`, `--help`                 show this message and exit
* `-i INPUT`, `--input INPUT`    the save file to monitor
* `-o output`, `--output OUTPUT` parsed output (default `auto`)

additional options:

* `-c CPS`, `--cps CPS`          number of checks per second (default `5`)
* `-b BUFFER`, `--buffer BUFFER` number of seconds of save buffer, increase the value if the program is going on parsing loop between source and json (min `0.25`s default `1`s)
* `-s`, `--step-backup`          create backup every parsing (from json to sav)
* `-k BACKUP_LIMIT`, `--backup-limit BACKUP_LIMIT` max number of backups to keep, old backup will be replaced with new ones (min `2` default `5`)
* `-l {debug,info,warning,error,critical}`, `--log-level {debug,info,warning,error,critical}` log level (default `info`)

If you are playing a game and you want to change some values in the save, then you can use this monitor function to do a realtime parsing of the save file into a json file. You can have an application like `notepad++` to open the json file and start changing values. Once you've saved the changes from the json file, it will by synced into the save file automatically. You can then reload your game from the save and the value will be changed.

Note: It's recommended to turn off auto save and only do saves manually in the text editor.

### Example usage

* `monitor -i "C:\Game Folder\Game\game_tyrano_data.sav" -s -c 10 -b 2`
* `monitor -i "C:\Game Folder\Game\game_tyrano_data.sav" -o "Session\parsed.json" -s -b 2 -k 10 -l debug`

-------------------

## Troubleshooting

This section is mostly for the monitor function. Before actually watching your save file, the monitor will check if the repacked output (`.sav` file that's parsed from `.json` file) is exactly the same. If it doesn't, it will show an integrity check error and it will highlight the differences between your original save file and the repacked save file.

Here's an example:
![image](https://github.com/Galactic647/GI-3DMigoto-Tools/assets/44773161/d79e83fb-f7f1-4b70-b19c-f2dbac8ca520)

You can see that the hash signature between the original source and the repacked source are different. In this particular file, the difference are located in the `8,764,099th` charater.

In this particular case, you can see that the original source has a line with `@` between `F01` and `echioto` however, on the repacked one it has `%40` instead. This is a really simple problem and the solution to this is to add `@` into the exclusion list in the `monitor config.ini` in the same directory as the input, this will skip the encoding for the characters in the exclusion list.

![image](https://github.com/Galactic647/GI-3DMigoto-Tools/assets/44773161/975a3d6b-09bd-42a3-9d48-e7f60dee0d87)

If the problem was solved, you will see no error and it will prompt you to open the output in a text editor like this.

![image](https://github.com/Galactic647/GI-3DMigoto-Tools/assets/44773161/9a097b6c-5c55-4453-a582-d2989fc8fea8)

-------------------

When error like this occured, you can try and figure out if the character (e.g. `@`) and the quote (e.g. `%40`) is related, you can try it by either doing.

* `chr(int('40', 16))` for `%40`, this will output `@`, or
* `hex(ord('@'))` for `@`, this will output `0x40`

or you can use `urllib` for exact output

* `urllib.parse.quote('@')` -> `%40`
* `urllib.parse.unquote('%40')` -> `@`

If any of them shows any resemblance (`%40` -> `0x40`) then that means it's just an encoding issue. Each game will have it's own settings (idk, maybe, didn't play that much tyrano games), sometimes you might add more exclusion or even remove some of them, but if you see the highlighted difference shows some hot garbage like this.

![image](https://github.com/Galactic647/GI-3DMigoto-Tools/assets/44773161/c6e51cd6-bf03-4bbc-9594-d19dd3d4d206)

then you can issue this repo and attach your game save for me to figure out the problem.
