<p align="left"><img src="logo/horizontal.svg" alt="lifelog" height="100px"></p>

[![Travis (.org)](https://img.shields.io/travis/andreyvpng/lifelog.svg?style=for-the-badge)](https://travis-ci.com/andreyvpng/lifelog)
[![GitHub issues](https://img.shields.io/github/issues/andreyvpng/lifelog.svg?style=for-the-badge)](https://github.com/andreyvpng/lifelog/issues)
[![GitHub forks](https://img.shields.io/github/forks/andreyvpng/lifelog.svg?style=for-the-badge)](https://github.com/andreyvpng/lifelog/network)
[![GitHub stars](https://img.shields.io/github/stars/andreyvpng/lifelog.svg?style=for-the-badge)](https://github.com/andreyvpng/lifelog/stargazers)
[![GitHub license](https://img.shields.io/github/license/andreyvpng/lifelog.svg?style=for-the-badge)](https://github.com/andreyvpng/lifelog/blob/master/LICENSE)

Life log app gives you the opportunity to track your activity.

## Demo

https://lifelogdjango.herokuapp.com

## Build & Run

Add .env. For developping I'm using this:

    DJANGO_DB_NAME=lifelog
    DJANGO_DB_USER=lifelog
    DJANGO_DB_PASSWORD=lifelog
    DJANGO_DB_HOST=db
    DJANGO_DB_PORT=5432
    DJANGO_SETTINGS_MODULE=config.dev_settings

For build and run, use:

    docker-compose build && docker-compose up

## Logo

Thank you, @reallinfo, for the logo and favicon.

## License

lifelog is free software under terms of the Apache License 2.0

Copyright (C) 2018 by Andrey Varfolomeev
