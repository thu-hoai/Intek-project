# Flickr Photostream Mirroring

## Introduction

[Flickr](https://www.flickr.com/) is certainly the most popular photo-sharing platform and social network where users upload photos for others to see. Users create a free account and upload their own photos to share with friends and followers online. Flickr has more than ten million registered members worldwide. Between 3 and 4 million new images are uploaded daily.

Flickr supports an [Application Programming Interface (API)](https://www.youtube.com/watch?v=GZvSYJDk-us) that [allows developers](https://www.smashingmagazine.com/2018/01/understanding-using-rest-api/) to [access Flickr data](https://www.flickr.com/services/api/).

## What the project does

Fetching Information from Flickr API to mirror a photostream with:

- The image in the highest available resolution of each photo.
- The data of this photo (title, description, and comments).

_Note_: This script

- Support for 2 downloading method FIFO and LIFO

  - FIFO: reading a user's photostream from their first published photos to the most recent (e.g., reading from the current last page of the user's photostream to the current first page).
  - LIFO: reading a user's photostream from their most recent published photo to their first published photos (e.g., reading from the first page of the user's photostream to the last page)

- Support for only fetches the pages of a user's photostream that it has not completely processed yet (consider that a flickr user nerver deletes phots from their photostream).

## Usage Information

### Prerequisites

- Python 3.6+ is required. <br/>

### Usage

- Setup a directory to install our Flickr mirroring utility
  ```
  $ mkdir ~/Documents/username/flickr_photostream
  $ cd ~/Documents/username/flickr_photostream
  ```
- Setup a Python virtual environment: `$ pipenv shell --three`
- Install our Flickr mirroring utility `pipenv install flickr_photostream` to install virtual environment.
- Get help our Bash script
  `$ mirror_flickr --help`

  ```
  usage: __main__.py [-h] [--fifo | --lifo] [--cache-path CACHE PATH]
                    [--image-only | --info-only] [--info-level LEVEL]
                    [--save-api-keys] [--debug DEBUG] [--verify-image]
                    --username USERNAME

  Flickr Mirorring

  optional arguments:
    -h, --help            show this help message and exit
    --fifo                specify the First-In First-Out method to mirror the
                          user's photostream, from the oldest uploaded photo to
                          the earliest
    --lifo                specify the Last-In First-Out method to mirror the
                          user's photostream, from the earliest uploaded photo
                          to the oldest (default option)
    --cache-path CACHE PATH
                          specify the absolute path where the photos downloaded
                          from Flickr need to be cached
    --image-only          Specify whether the script must only download photos'
                          images'
    --info-only           Specify whether the script must only download photos'
                          information
    --info-level LEVEL    Specify the level of information of a photo to fetch
                          (value between 0 and 2)
    --save-api-keys       Specify whether to save the Flickr API keys for
                          further usage.
    --debug DEBUG         specify the logging level, value between 0 and 4, from
                          critical to debug
    --verify-image        specify whether the script must verify images that
                          have been download
    --username USERNAME   Username of the account of a user on Flickr
  ```

- Executive bash example:
  - The first time
```bash
$ mirror_flickr --username hoai.kt178 --save-api-keys --image-only --debug 3 --verify-image
Enter your Flickr API key:    <input your own API key>
Enter your Flickr API secret: <input your own API secrect>
```

```
---MODE: VERIFY IMAGES WHICH HAVE BEEN DOWNLOADED---
List of photos which are downloaded []
Pages which are downloaded []
Scanning page 1/34 .......
Size of photo queue 8
Caching image of photo 224dd73facb6da1ae279d6c2e6c2eb16.jpg
Caching image of photo 13324e9fdf02f8d127b1223cadd9148e.jpg
Caching image of photo eecada3d5e7c44fb3472f657ad44f3fc.jpg
Caching image of photo 9e29a904df71b58799968b754ff86add.jpg
Caching image of photo 2bcc5dc6002811fccbb014454b33d840.jpg
Caching image of photo a914fdb51cf408b9c47dbee5a7fd3fb5.jpg
Caching image of photo 7108bfb6fb0c7a6e8630ca0e7073eb7e.jpg
Caching image of photo 170b28ac6ad24c2897430dbcb52cc62a.jpg
Scanning page 2/34 .......
Size of photo queue 8
Caching image of photo 296cf002db8200dfdeff5c243fd3247d.jpg
Caching image of photo dbd3145cecfd61680815e1d4efd42091.jpg
...........................................................
```

  - The seconde time

```bash
$ mirror_flickr --username hoai.kt178 --image-only --debug 3 --verify-image
---MODE: VERIFY IMAGES WHICH HAVE BEEN DOWNLOADED---
List of photos which are downloaded [270, 269, 268, 267, 266, 265, 264, 263, 262]
Pages which are downloaded [1]
Photos in page 1 have been downloaded. Skip it
Scanning page 2/34 .......
Size of photo queue 8
296cf002db8200dfdeff5c243fd3247d.jpg existed
Caching image of photo dbd3145cecfd61680815e1d4efd42091.jpg
Caching image of photo 19755286854077f5b4dc2a467cc42466.jpg
Caching image of photo 6fe37c6a97c4d2d8c13557dec9d49ff5.jpg
Caching image of photo 6b911dff2f7c68a52489ffb191b03c98.jpg
Caching image of photo 06c0798587c760bd88016baeea0e16ea.jpg
Caching image of photo eb0a67f24166f0f3017b0e1e2bbef994.jpg
Caching image of photo 1b1cb27285bc4943511229ce1753e85e.jpg
Scanning page 3/34 .......
Size of photo queue 8
Caching image of photo 901e285ecaf1012b4fd18d3793cb85e3.jpg
Caching image of photo 49671fc6cbfafcd841acad6521675380.jpg
Caching image of photo 23cd5d46c5458868fe0661d163410fd2.jpg
Caching image of photo 978b5721a1d2ecc7ae3a72fa226f4fec.jpg
Caching image of photo 33d19a85c708cc474ecb9d2cb06d7f6d.jpg
Caching image of photo 51d2f64fec43e03ec208e813b86ddd2c.jpg
Caching image of photo 87c8f2260f38f8883020221f7585ddc9.jpg
Caching image of photo f9667729105d742ced5bee6e082ea0f3.jpg
Scanning page 4/34 .......
..........................................................

```

## Contact Information

- If you have any problems using this library, please use the contact below. <br/>
  `Email: hoai.le@f4.intek.edu.vn`
