#!/usr/bin/env python3
"""Hack TV5MONDE Web site's data, to download and rebuild the episode videos"""
import json
import http.client
import urllib.parse
import urllib.request
import urllib.error
import hashlib
import os
import time
import re
import socket
import logging
import shutil

DOMAIN_URL = "http://www.tv5monde.com"
# Set extra header
HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us)\
            AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405'}

# HTTP errors
TEMPORARY_ERROR = [408, 429, 500, 502, 503, 504, 506, 507, 511, 501, 505]
PERMANENT_ERROR = [x for x in range(400, 499) if x not in (408, 429)]

# Valid_keys to check to data fetched
VALID_KEYS = ["title", "url", "image", "date", "duration"]

# Get path running script
BASE_DIR = os.path.dirname(os.path.realpath(__file__))

# Address of Temp folder to store all downloaded video
TEMP_DIR = os.path.join(BASE_DIR, '.cache')

# Set logging
logging.basicConfig(level=logging.INFO, filemode='w')

def parse_url(url):
    """Check and parse a specific url

    Parameter: param url: A Uniform Resource Locator (URL) that references the
            endpoint to open and read data from.

    Raise: TypeError: if given URL is not formatted as standard

    Return: A named tuple ParseResult
    """
    # splitting a URL string into its components
    parsed = urllib.parse.urlparse(url)

    # Check URL
    standard_url = r"^(https?\:\/\/(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),\{}])+)"
    if not re.match(standard_url, url):
        logging.error("Invalid URL", exc_info=True)

    return parsed

# Waypoint 1: Write a Python Class Episode
class Episode:
    """Class Episode on TV5MONDE Web site

    Attributes:
        title (str): (Read-only) The title of the episode
        page_url (str): (Read-only) URL of the Web page dedicated to this episode
        image_url (str): (Read-only) URL of the image
        broadcasting_date (str): (Read-only) The date when this episode has been broadcast
        duration (str): (Read-only) duration of this episode
    """
    def __init__(self, title, page_url, image_url, broadcasting_date, duration):
        """The constructor for Version class

        Parameters:
            title (str): The title of the episode
            page_url (str): URL of the Web page dedicated to this episode
            image_url (str): URL of the image
            broadcasting_date (str): The date when this episode has been broadcast
            duration (str): duration of this episode
        """
        self.__title = title
        self.__page_url = page_url
        self.__image_url = image_url
        self.__broadcasting_date = broadcasting_date
        self.__duration = duration
        # Additional attribute episode_id as the ID of the episode
        self.__episode_id = self.__parse_episode_id(self.__image_url)
        # Additional attribute key as hash value of URL web page
        self.__key = self.__generate_key(self.__page_url)

    @staticmethod
    def from_json(payload):
        """Return an object Epidode when pass Episode info

        Parameter: payload (dict) -- a JSON expression of one Episode

        Raise ValueError: if passed data is not a dic and key is inappropriate

        Return: An object Episode
        """
        # Data validation
        # In case passed data is not a dict
        if not isinstance(payload, dict):
            logging.error("Data is inappropriate", exc_info=True)
        # In case keys' passed data fails expectation
        if set(VALID_KEYS) != set(payload.keys()):
            logging.error("Data is inappropriate", exc_info=True)

        # Get values as an object Episode
        return Episode(payload["title"], payload["url"],
                       payload["image"], payload["date"],
                       payload["duration"])

    @staticmethod
    def __generate_key(s):
        """Get the MD5 hash of the url

        Argument: s: (str) web page of the episode

        Return: MD5 hash value """
        return hashlib.md5(s.encode()).hexdigest()

    # Waypoint 2: Retrieve the Identification of an Episode
    @staticmethod
    def __parse_episode_id(url):
        """Get identification from given URL string

        Argument: url (str): URL of the image of an episode

        Returns: the identification of the episode (str)
        """
        return (url.split('/')[-1]).split('.')[0]

    @property
    def key(self):
        """ Return the episode's hash key """
        return self.__key

    @property
    def title(self):
        """ Return the episode's title """
        return self.__title

    @property
    def image_url(self):
        """ Return the episode's image_url"""
        return self.__image_url

    @property
    def broadcasting_date(self):
        """ Return the episode's broadcasting_date"""
        return self.__broadcasting_date

    @property
    def page_url(self):
        """ Return the episode's page_url"""
        return '{}{}'.format(DOMAIN_URL, self.__page_url)

    @property
    def duration(self):
        """ Return the episode's duration"""
        return self.__duration

    @property
    def episode_id(self):
        """ Return the valiue of episode_id """
        return self.__episode_id

# Waypoint 3: Fetch the List of Episodes
def read_url(url, maximum_attempt_count=3, sleep_duration_between_attempts=10):
    """ Return data fetched from a HTTP endpoint.

    Parameters
        param url: A Uniform Resource Locator (URL) that references the
            endpoint to open and read data from.
        param maximum_attempt_count: Maximal number of failed attempts to
            fetch data from the specified URL before the function raises an
            exception.
        param sleep_duration_between_attempts: Time in seconds during which
            the current thread is suspended after a failed attempt to fetch
            data from the specified URL, before a next attempt.

    Return: The data read from the specified URL.

    Raise HTTPError: If an error occurs when trying unsuccessfully
        several times to fetch data from the specified URL, after
    """
    # start number of failed attempts to fetch data as 0
    failed_attempt = 0

    while failed_attempt < maximum_attempt_count:

        try:
            # connect and make request
            connection = http.client.HTTPConnection(parse_url(url).netloc)
            connection.request("GET", f'{parse_url(url).path}?{parse_url(url).query}'
                               , headers=HEADERS)
            resp = connection.getresponse()

            # In case of Temporary Errors
            if resp.status in TEMPORARY_ERROR:
                # Retry every catch a temporary error HTTP
                logging.info("Attempt in 10s")
                failed_attempt += 1
                # When reach a maximum_attempt, raise Error
                if failed_attempt == maximum_attempt_count:
                    logging.error('Fail to fetch data', exc_info=True)
                # Close connection every time attempt
                connection.close()
                # Sleep after a failed attempt to fetch data from URL, before a next attempt.
                time.sleep(sleep_duration_between_attempts)
                continue

            # In case of Permanent Errors
            if resp.status in PERMANENT_ERROR:
                logging.error('Fail to fetch data', exc_info=True)

            # in case of the request is ok
            return resp.read().decode("utf-8")

        except http.client.HTTPException:
            logging.error("Fail to access URL", exc_info=True)

        finally:
            # Always close the connection to the server
            connection.close()

# Waypoint 4: Fetch the List of all the Episodes
def fetch_episodes(url):
    """
    Read the JSON expression representing a list of episodes fetched from API

    Parameter: url (str): A Uniform Resource Locator (URL) that references the
        endpoint to open and read data from.

    Return: list object of all episodes
    """
    # Get the number of pages from the first page
    numpages = json.loads(read_url(url))["numPages"]

    # check url then format to get index page number
    url += "?page={}"

    # initialize a list of Episodes object
    episodes = []

    # Read data from each numpage, then pass each Episode info to an object
    for i in range(1, numpages + 1):

        # Loads data each page
        json_data = json.loads(read_url(url.format(i)))

        # Get data from each episode
        episodes_data = json_data["episodes"]

        # Return an object Epidode when pass Episode info
        for data in episodes_data:
            episodes.append(Episode.from_json(data))

    return episodes

# Waypoint 5: Parse Broadcast Data of an Episode
def fetch_episode_html_page(episode):
    """
    Take an object Episode to return textual HTML content of the episode page

    Parameter: param episode: object of Episode

    Return: the textual HTML content of the episode page
    """
    return read_url(episode.page_url)

def parse_broadcast_data_attribute(html_page):
    """
    Take source code of the HTML page of an episode to
    get JSON expression of the data-broadcasd

    Paramemter: param html_page: (str) the source code of the HTML page of an episode

    Return: a JSON expression corresponding to
        the string value of the attribute data-broadcast
    """
    # Reg for the string represent data-broadcast, then return Json exp
    return json.loads(re.findall("data-broadcast='(.*)' data-duration", html_page)[0])

# Waypoint 6: Build a URL Pattern of the Video Segments of an Episode
def build_segment_url_pattern(broadcast_data):
    """
    Get URL pattern that refer to the video segments of the episode.

    Parameter: param broadcast_data (dict): the broadcast data of an episode

    Return: URL pattern (str): the video segments of this episode
    """
    # Get url of file
    url = broadcast_data["files"][0]["url"]

    # In case of broadcast data is not "m3u8"
    if url.split(".")[-1] != "m3u8":
        return url

    # Take path of url tp convert to new path of URL video
    path_split = parse_url(url).path.split("/")

    join_path = '/'.join(path_split[:(len(path_split)-1)])
    new_path = '{}/{}'.format(join_path, 'segment{}_3_av.ts')

    # Get new URL by replace by new_path and new query
    replaced = parse_url(url)._replace(path=new_path, query='null=0')
    return replaced.geturl()


def _download_segment_video(video_link, output_dir):
    """Download video to given directory
    
    Prameters:
        param video_link (str) : url video
        param output_dir (str): directory where to save downloaded video
    """
    # Send request
    req = urllib.request.Request(video_link, headers=HEADERS)
    # Open then write in binary mode to download
    with urllib.request.urlopen(req, timeout=10) as response:
        data = response.read()
    with open(output_dir, 'wb') as out_file:
        out_file.write(data)


def _check_local_exists(direct_path, tail):
    """Check if given path is exist locally or not

    Prameters:
        param dir_path (str) : url video
        param tail (str): tail format of path
    
    Return:
        True if directory exist. Inform if it exists
        False otherwise
    """
    file_name = os.path.join(direct_path, tail)
    if os.path.exists(file_name):
        logging.info("%s existed", tail)
        return True
    return False


# Waypoint 7-9-10-11: Download the Video Segments of an Episode
def download_episode_video_segments(episode, path=BASE_DIR):
    """
    Take an object Episode then return the absolute path names of video segments

    Parameter:
        param episode: object of Episode
        param path: (str) dir the video segment files need to be saved into.
            set default in the current working directory.

    Return: the absolute path and file names of these video segments
        in the order of the segment indices.
    """
    # Get an absolute path of working directory
    abs_path = os.path.abspath(os.path.expanduser(path))

    # Initialize a list to episode video segments
    video_segment_lst = []

    # Store episode_id to save file name
    episode_id = episode.episode_id

    # In case episode_id is an empty str, get a key to downd
    if episode_id == "":
        episode_id = episode.key

    file_name_mp4 = f'{episode_id}.mp4'

    # Get the segment pattern of the video
    segment_pattern = build_segment_url_pattern(
        parse_broadcast_data_attribute(fetch_episode_html_page(episode)))

    # Download file if video format is MP4
    try:
        if segment_pattern.split(".")[-1] == "mp4":
            # Identify working dir and TEMP_DIR
            output_dir_temp = os.path.join(TEMP_DIR, file_name_mp4)
            output_dir = os.path.join(abs_path, file_name_mp4)
            # Download final video to TEMP_DIR
            _download_segment_video(segment_pattern, output_dir_temp)
            # Copy final video from output_dir_temp to working directory
            shutil.copyfile(output_dir_temp, output_dir)
            return [output_dir]
    # Raise error if occurring an error 
    except urllib.error.HTTPError as exp:
        logging.error('video link is broken', exc_info=True)

    # Download file if video format is M3U8
    segment_index = 0
    # Loop by incrementing the index of video segment for ever until
    # there is no more video segment - catching 404 error
    while True:
        segment_index += 1
        # Identify file name of each segments
        file_name = f'segment_{episode_id}_{segment_index}.ts'
        segment_video = segment_pattern.format(segment_index)
        # Get output dir to save video segment
        output_dir_temp = os.path.join(TEMP_DIR, file_name)
        output_dir = os.path.join(abs_path, file_name)
        try:
            # Not download if video segment exists on working directory
            if _check_local_exists(abs_path, file_name):
                video_segment_lst.append(output_dir)
                continue
            # Start download each segment
            _download_segment_video(segment_video, output_dir_temp)
            video_segment_lst.append(output_dir)
            # Move video_segment from TEMP dir to output directory
            shutil.move(output_dir_temp, output_dir)

        except urllib.error.HTTPError as exp:
            if exp.code == 404: # break if catching 404 errors
                break
            logging.error('Fail to fetch data', exc_info=True) # Raise other
        except socket.timeout:
            pass # Pass if timeout

    return video_segment_lst

# Waypoint 8-9-10-11: Build the Final Video of an Episode
def build_episode_video(episode, segment_file_path_names, path=None):
    """
    Assemble all these video segments in one video named
    after the identification of the episode.

    Arguments:
        episode: object of Episode
        segment_file_path_names (list): a list of absolute path
            and file names of TS video segments in the order of their index.

    Keyword Arguments:
        path (str): directory the episode's video file need to be saved into. 
            (default: None)

    Return: the absolute path and file name of the episode's video
    """

    # Do nothing if final video existed or catching URL video error
    if segment_file_path_names == []:
        return None

    # Store episode_id to save file
    episode_id = episode.episode_id

    # Define path as var {output_path} to save file two cases
    if path is None:
        # If default as None, path identified by the first video segment
        direct_path = os.path.dirname(segment_file_path_names[0])
        output_dir_temp = os.path.join(direct_path, f'{episode_id}.ts')
        abs_path = os.path.abspath(os.path.expanduser(direct_path))
    # In case input path
    else:
        output_dir_temp = os.path.join(TEMP_DIR, f'{episode_id}.ts')
        abs_path = os.path.abspath(os.path.expanduser(path))

    # Identify where to download final fideo
    output_final = os.path.join(abs_path, f'{episode_id}.ts')

    # In case episode_id is an empty str, get a key to down
    if episode_id == "":
        episode_id = episode.key

    # Move final video from segment directory to final working dir if *.mp4
    if segment_file_path_names[0].split(".")[-1] == 'mp4':
        shutil.move(segment_file_path_names[0],\
        os.path.join(abs_path, f'{episode_id}.mp4'))
        return segment_file_path_names[0]

    # Open each of segments to read byte downloads final video to TEMP_DIR
    with open(output_dir_temp, 'wb') as out_file:
        for segment in segment_file_path_names:
            with open(segment, 'rb') as seg_path:
                out_file.write(seg_path.read())

    # Remove video segments whenever the final video is downloaded
    if os.path.exists(output_dir_temp):
        for file_path in segment_file_path_names:
            os.remove(file_path)

    # Copy final video from TEMP_DIR to working directory
    if path is not None:
        shutil.copyfile(output_dir_temp, output_final)

    return output_final

# Waypoint 9: Cache improvement
def download_video(episode, segment_folder, final_folder=None):
    """Check if video of given episode is downloaded or not, 
    proceed if it hasn't downloaded, skip if downloaded
    
    Arguments:
        episode: an object of the episode
        segment_folder (str): dir the video segment files need to be saved into.
        final_folder (str): dir the episode's video file need to be saved into. 
            (default: None)
    """

    # Store episode_id to save file name
    episode_id = episode.episode_id

    # Define path as var {output_path} to save file two cases
    if final_folder is None:
        final_folder = segment_folder

    segment_abs_path = os.path.abspath(os.path.expanduser(segment_folder))
    final_abs_path = os.path.abspath(os.path.expanduser(final_folder))

    # Create new dir if working directory doesn't exist
    # Create TEMP_DIR to store all file downloaded
    for path in (segment_abs_path, final_abs_path, TEMP_DIR):
        if not os.path.exists(path):
            os.makedirs(path)

    # In case episode_id is an empty str, get a key to downd
    if episode_id == "":
        episode_id = episode.key

    # Define file name tail
    file_name_mp4 = f'{episode_id}.mp4'
    file_name_m3u8 = f'{episode_id}.ts'

    # Do not download if the final video existed in local FINAL directory
    if _check_local_exists(final_abs_path, file_name_m3u8)\
        or _check_local_exists(final_abs_path, file_name_mp4):
        return

    # Move final video from CACHE dir to FINAL dir if it existed in CACHE dir
    for tail_video_path in (file_name_m3u8, file_name_mp4):
        if _check_local_exists(TEMP_DIR, tail_video_path):
            shutil.move(os.path.join(TEMP_DIR,tail_video_path), final_abs_path)
            return

    # Download video if final video doesn't exist at CACHE and FINAL directory 
    segment_file_path = download_episode_video_segments(episode, segment_folder)
    build_episode_video(episode, segment_file_path, final_folder)
    

def main():
    """ Demonstrate and run tests """
    
    url1 = "http://www.tv5monde.com/emissions/episodes/merci-professeur.json"
    episodes = fetch_episodes(url1)
    # episode1 = episodes[3]
    download_dir1 = "./downloadHoai_segment"
    download_dir2 = "./downloadHoai2_final"
    for i in range(9,10):
        download_video(episodes[i], download_dir1, download_dir2)
if __name__ == "__main__":
    main()
