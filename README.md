# nba

Downloads data using the [stats.nba.com](http://stats.nba.com) API via the [nba_py](https://github.com/seemethere/nba_py) package and updates the MySQL database designated by the `BYU_NBA_DATABASE_URL` environment variable using the [peewee](http://docs.peewee-orm.com/en/latest/) database Object Relational Map (ORM). 

## requirements 

optional: 
```
pip install requests-cache
```

## usage

1. Set up the database settings (replacing `<user>`, `<password>`, `<host>`):
  bash, zsh etc: 

  Add 
  ```
  export BYU_NBA_DATABASE_URL="mysql://<user>:<password>@<host>/nba"
  ``` 
  to your `~/.bashrc`, `~/.bash_profile`, `~/.profile` or similar shell startup file.

  [fish shell](https://fishshell.com):
  
  ```
  set -U BYU_NBA_DATABASE_URL 'mysql://<user>:<password>@<host>/nba'
  ```
  
  You may also want to export `NBA_PY_CACHE_EXPIRE_MINUTES` to something more than the default `10` so that you don't have to download NBA data as much. 
  
2. Ensure that you have `pip` installed and then install the package:
  
  ```
  pip install git+git://github.com/byu-stats-sports/nba.git
  ```

3. Get help:
  
  ```
  nba --help
  ```

## devlop

1. Get the source:
  
  ```
  git clone https://github.com/byu-stats-sports/nba.git
  ```
  
2. Install the application: 
  
  ```
  pip install --editable nba/
  ```
