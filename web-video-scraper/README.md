# "_Merci professeur !_" Episode Video Scraper
---

## Description

- Purposes: These functions show step by step to  to download and rebuild the episode videos from website, here is TV5MONDE Web site's data ["_Merci professeur !_"](http://www.tv5monde.com/emissions/episodes/merci-professeur). Those step are demonstrated through below waypoints:

    - WP1: Write a Python Class `Episode`
    - WP2: Retrieve the Identification of an Episode
    - WP3: Fetch the List of Episodes
    - WP4: Fetch the List of all the Episodes
    - WP5: Parse Broadcast Data of an Episode
    - WP6: Build a URL Pattern of the Video Segments of an Episode
    - WP7: Download the Video Segments of an Episode
    - WP8: Build the Final Video of an Episode
    - WP9: Implement a Cache Strategy
    - WP10: Support Downloading of Old Episodes
    - WP11: Support Episodes with no Representative Image

- _Note_ : _more details, please refer to initial_istruction.md file_

---
## How to use

### Prerequisites
- Python3 installation is required to get started (check by using python3 --version)

### Usage

- Clone this repo to your local machine using `https://github.com/intek-training-jsc/web-video-scraper-hoaithu1.git`
- Please follow my instruction carefully to download and build video:

  - `Step 1`: Open teminal then import episode_video_scraper.py

  - `Step 2`: Input `url1 = "http://www.tv5monde.com/emissions/episodes/merci-professeur.json"`

  - `Step 3:`
    - Input where you want to store video each segments of the video. Assign it to name (below example it's assign as name `download_segment`). It directory is not exist, it will automatically created. _Note_: _These segments will be automatically deleted after the final video is build_
    - Input where you want to store final video. Assign it to name (below example it's assign as name `download_final`).

  - `Step 4: `Call the function to download video segments `download_video` as below: 

      ```text
      download_video(episodes[3], download_dir1, download_dir2)

      ```
  Below is example of the whole process:
    ```python
    >>> from episode_video_scraper import *
    >>> url1 = "http://www.tv5monde.com/emissions/episodes/merci-professeur.json"
    >>> episodes = fetch_episodes(url1)
    >>> download_segment = "./downloadHoai_segment"
    >>> download_final = "./downloadHoai2_final"
    >>> for i in range(9,10):
    ...     download_video(episodes[i], download_dir1, download_dir2)
    ```
  _Note_: _Please note that these functions don't download again any final video either segment video that have been already downloaded. It will raise status. You can see as below:_
    ```python
    >>> download_video(episodes[1], download_dir1, download_dir2)
    INFO:root:5148897.ts existed
    ```
  ```python
  >>> download_video(episodes[2], download_dir1, download_dir2)
  INFO:root:segment_5148881_1.ts existed
  INFO:root:segment_5148881_2.ts existed
  INFO:root:segment_5148881_3.ts existed
  INFO:root:segment_5148881_4.ts existed
  INFO:root:segment_5148881_5.ts existed
  INFO:root:segment_5148881_6.ts existed
  INFO:root:segment_5148881_7.ts existed
  INFO:root:segment_5148881_8.ts existed
  INFO:root:segment_5148881_9.ts existed
  INFO:root:segment_5148881_10.ts existed
  INFO:root:segment_5148881_11.ts existed
  ```
  _Note_:  _These funtion based on the principle that all videos are managed at the temporary folder .cache. To get everything downloaded under your control, you could refer to that directory at address `your_current_directory/.cache`._


## Support

Reach out to me (author)at the following place!

- Email at hoai.le@f4.intek.edu.vn
---
