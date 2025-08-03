# Quadcask

Private whiskey collection manager based on WebView

## Project Setup

### Install

```bash
$ pip install -r requirements.txt
$ cd frontend
$ npm install
```

### Get Whiskey Database

* Download CSV file from: https://whiskyanalysis.com/index.php/database/
* Save CSV file as ``whisky_database.csv`` and put it in the quadcask directory

### Development

```bash
$ cd frontend
$ npm run dev
$ cd ../
$ python main.py
```

### Build

```bash
$ cd frontend
$ npm run build
$ cd ..
$ pyinstaller quadcask.spec
$ mkdir -p dist/quadcask/frontend
$ cp -r frontend/dist dist/quadcask/frontend
```
