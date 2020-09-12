#!/usr/bin/env python3
"""Database FarCry Game"""
import os
import logging
import datetime
import csv
import sqlite3
import psycopg2
import constants as const

# Set logging
logging.basicConfig(level=logging.INFO, filemode='w')


# Waypoint 1: Read Game Session Log File
def read_log_file(log_file_pathname):
    """Reads and returns all the bytes from the file.

    Arguments: (str): pathname of a Far Cry server log file

    Returns: returms all the bytes from the file

    Raise Error: if given path is not a string.
    """
    # Data valid
    if not isinstance(log_file_pathname, str):
        logging.warning("The given path %s is not a string", log_file_pathname,
                        exc_info=True)

    # Handle log_file_path
    log_file_path = os.path.expanduser(os.path.abspath(log_file_pathname))

    try:
        with open(log_file_path) as log_file:
            data = log_file.read()
            return data
    # except an input/output operation fails
    except IOError:
        logging.warning("Please check your path")


def __get_console_variables(log_data):
    """Get a dictionary of console variables

    Arguments:
        log_data (str)-- data of log file

    Returns: a dictionary of console variables
    """

    # Initialize a dictionary to store all console variables
    console_val_dict = {}

    # Get all console variables from log data
    console_val_list = const.CONSOLE_VARIABLES_PATTERN.findall(log_data)

    # Store it into dictionary
    for console_val in console_val_list:
        lst = console_val.split(',')
        console_val_dict[lst[0]] = lst[1]
    return console_val_dict


# Waypoint 2: Parse Far Cry Engine's Start Time
# Waypoint 3: Parse Far Cry Engine's Start Time with Time Zone
def parse_log_start_time(log_data):
    """Parse log start time to an object datetime.datetime object

    Arguments: log_data: (str) data of log file

    Returns: a datetime.datetime object representing the time
        the Far Cry engine began to log events.
    """
    # Data validation
    if not isinstance(log_data, str):
        logging.error("Data type must be a string")

    # Get timezone from log_file
    time_zone = __get_console_variables(log_data)["g_timezone"]

    # Get date_time string from data of log_data
    log_start_time = const.START_TIME_PATTERN.findall(log_data)[0]

    # Parse string into object datetime.datetime
    without_timezone = datetime.datetime.strptime(log_start_time, '%A, %B %d, %Y %X')

    time_zone_info = datetime.timezone(datetime.timedelta(hours=int(time_zone)))

    return without_timezone.replace(tzinfo=time_zone_info)


# Waypoint 4: Parse Match's Map Name and Game Mode
def parse_match_game_mode_and_map_name(log_data):
    """Get a tuple (mode, map) from log_data

    Arguments:
        log_data:(str) data of log file

    Returns:
        (mode, map): tuple
            mode (str): mode of game (ASSAULT, TDM, FFA)
            map (str): name of map
    """

    # Data validation
    if not isinstance(log_data, str):
        logging.error("Data type must be a string")

    # Find (mode, map) by seach as pattern in log_data
    mode_map_name = const.MODES_PATTERN.search(log_data).groups()

    # Reversed tuple
    return mode_map_name[::-1]


def parse_frags(log_data):
    """Return a list of frags of game

    Arguments: log_data:(str) data of log file

    Returns: a list of frags of game
    """
    # Find frags by seach as pattern in log_data
    frags_list = const.FRAGS_PATTERN.findall(log_data)

    # Reset start time at minute=0 and second=0
    start_time = parse_log_start_time(log_data).replace(minute=0, second=0)

    last_hour_frag = start_time.hour

    # The first frag
    first_frag_time = start_time + datetime.timedelta(hours=start_time.hour - last_hour_frag,
                                                      minutes=int(frags_list[0][0][:2]),
                                                      seconds=int(frags_list[0][0][-2:]))

    # Initial a list of frag history
    frag_history = [tuple([first_frag_time] + [val for val in frags_list[0][1:] if val != ''])]

    for i in range(1, len(frags_list)):

        # Get the last minute and second of each frag
        last_minute_frag = frags_list[i - 1][0].split(':')[0]

        # Get the current minute and second of each frag
        cur_minute_frag = frags_list[i][0][:2]
        cur_second_frag = frags_list[i][0][-2:]

        # In case hour changed
        if cur_minute_frag < last_minute_frag:
            last_hour_frag -= 1
        # Get the current match by hour, minute and second of the current frag
        # plus start time
        cur_frag = start_time + datetime.timedelta(hours=start_time.hour - last_hour_frag,
                                                   minutes=int(cur_minute_frag),
                                                   seconds=int(cur_second_frag))
        # Add to frag history
        frag_history.append(tuple([cur_frag] + [val for val in frags_list[i][1:] if val != '']))

    return frag_history


# Waypoint 7: Prettify Frag History
def prettify_frags(frags):
    """ Display the list of frags on the terminal screen using emoji characters

    Arguments:
        frags: (list) array of tuples of frags parsed from a Far Cry server's log file

    Returns:
        A list of strings, each with the format:
            [frag_time] 😛 killer_name weapon_icon 😦 victim_name
    """
    # Data validation
    if not isinstance(frags, list):
        logging.error("Data type must be a list")

    # Initialize a list to store match with emojis
    frags_with_emojis = []
    for frag in frags:
        # If kill itself
        if len(frag) == 2:
            frags_with_emojis.append('[{}] {} {} {}'
                                     .format(frag[0], const.FROWNING_FACE, frag[1],
                                             const.SKULL_AND_CROSSBONES))
        else:  # normal
            frags_with_emojis.append('[{}] {} {} {} {} {}'
                                     .format(frag[0], const.FACE_WITH_TONGUE,
                                             frag[1], const.WEAPONS_DICT[(frag[3])],
                                             const.FROWNING_FACE, frag[2]))

    return frags_with_emojis


def __conver_string_time_to_object(time_reset, minute_plus, second_plus):
    """Return new datetime object from given time reset and minutes seconds

    Arguments:
        time_reset: (datetime.datetime object)
        minute_plus: (int) minute plus
        second_plus: (int) second plus

    Returns:
        new_time_object: a datetime.datetime object
    """
    new_time_object = time_reset + datetime.timedelta(
        minutes=int(minute_plus),
        seconds=int(second_plus))

    return new_time_object


# Waypoint 8: Determine Game Session's Start and End Times
def parse_match_start_and_end_times(log_data, log_start_time, frags):
    """ Parse a start time and end time of a Game Session

    Arguments:
        log_data:(str) data of log file
        log_start_time: (datetime.datetime object) representing the time
            the Far Cry engine began to log events.
        frags: (list) a list of frags of game

    Returns:
        (start_time, end_time): tuple
            start_time (datetime.datetime object)
            end_time (datetime.datetime object)
    """
    # Data validation
    if not isinstance(log_data, str):
        logging.error("Data type is inappropriate")
    if not isinstance(log_start_time, datetime.datetime):
        logging.error("Data type is inappropriate")
    if not isinstance(frags, list):
        logging.error("Data type is inappropriate")

    # In case Far Cry ends with Statistics
    try:
        end_time_string = const.END_TIME_PATTERN.search(log_data).group(1)
    # In case engine crashed before the end of a game session
    except AttributeError:
        end_time_string = const.END_TIME_ERROR_PATTERN.search(log_data).group(1)
    finally:
        start_time_string = const.START_GAME_SESSION.search(log_data).group(1)
        # Convert start time string to object
        session_start_object = __conver_string_time_to_object(
            log_start_time.replace(minute=0, second=0)
            , start_time_string[:2], start_time_string[-2:])
        # Get end_game time
        end_game = frags[-1][0]
        # Convert end time string to object
        session_end_object = __conver_string_time_to_object(
            end_game.replace(minute=0, second=0)
            , end_time_string[:2], end_time_string[-2:])

    return (session_start_object, session_end_object)


# Waypoint 9: Create Frag History CSV File
def write_frag_csv_file(log_file_pathname, frags):
    """Write data to given csv file

    Arguments:
        log_file_pathname: (str) pathname of the CSV file to store the frags in
        frags: (list)  an array of tuples of the frags
    """
    # Data valid
    if not isinstance(log_file_pathname, str):
        logging.warning("The given path %s is not a string", log_file_pathname, exc_info=True)

    # Create and write by line to csv file
    with open(log_file_pathname, 'w') as csv_file:
        csv_writer = csv.writer(csv_file)
        for frag in frags:
            csv_writer.writerow(frag)


# Waypoint 25: Insert Game Session Data into SQLite
def insert_match_to_sqlite(file_pathname,
                           start_time,
                           end_time,
                           game_mode,
                           map_name,
                           frags):
    """Insert Game Session Data into SQLite

    Arguments:

        file_pathname (str): The path and name of the Far Cry's SQLite database;

        start_time (datetime.datetime object) with time zone information
            corresponding to the start of the game session.

        end_time (datetime.datetime object) with time zone information
            corresponding to the end of the game session.

        game_mode (str): Multiplayer mode of the game session (ASSAULT, TDM, FFA)

        map_name (str): Name of the map that was played

        frags (list): list of tuples of the following form
            (frag_time, killer_name[, victim_name, weapon_code])
                frag_time (required): (datetime.datetime) with time zone when the frag occurred;
                killer_name (required): (str) username of the player
                    who fragged another or killed himself;
                victim_name (optional): (str) username of the player who has been fragged;
                weapon_code (optional): (str) code of the weapon that was used to frag.
    """
    # Data validation
    if not isinstance(file_pathname, str):
        logging.warning("The given path %s is not a string", file_pathname, exc_info=True)
    if not isinstance(start_time, datetime.datetime):
        logging.error("Data type is inappropriate")
    if not isinstance(end_time, datetime.datetime):
        logging.error("Data type is inappropriate")
    if not isinstance(game_mode, str):
        logging.error("Data type is inappropriate")
    if not isinstance(map_name, str):
        logging.error("Data type is inappropriate")
    if not isinstance(frags, list):
        logging.error("Data type is inappropriate")

    # Insert a row of data
    try:
        # Connect to an existing database
        with sqlite3.connect(file_pathname) as conn:
            # Open a cursor to perform database operations
            cur = conn.cursor()
            # Execute a command: pass data
            cur.execute(const.SQLITE_MATCH, (start_time, end_time, game_mode, map_name))
            # execute each line
            insert_frags_to_sqlite(conn, cur.lastrowid, frags)
            logging.info(cur.lastrowid)
    except sqlite3.IntegrityError:
        logging.error("Unable to connect")
    finally:
        # Closing database connection
        if conn:
            # Close the communicateion
            cur.close()
            conn.close()
            logging.info("Connection is closed")


# Waypoint 26: Insert Match Frags into SQLite
def insert_frags_to_sqlite(connection, match_id, frags):
    """Insert Match Frags (new record) into SQLite (the table match_frag)

    Arguments:
        connection: (sqlite3 object) a sqlite3 Connection object
        match_id: (int) the identifier of a match
        frags: (list) a list of frags, as passed to the function insert_match_to_sqlite,
            that occurred during this match
    """
    # Data validation
    if not isinstance(connection, sqlite3.Connection):
        logging.error("Data type is inappropriate")
    if not isinstance(match_id, int):
        logging.error("Data type is inappropriate")
    if not isinstance(frags, list):
        logging.error("Data type is inappropriate")

    # Open a cursor to perform database operations
    cur = connection.cursor()

    for frag in frags:
        # in case kill others by weapon
        if len(frag) != 2:
            cur.execute(const.SQLITE_KILL_OTHER, (match_id, *frag))
        # in case kill itself
        else:
            cur.execute(const.SQLITE_KILL_ITSELF, (match_id, *frag))


# Waypoint 48: Insert Game Session Data to PostgreSQL Database
def insert_match_to_postgresql(properties,
                               start_time,
                               end_time,
                               game_mode,
                               map_name,
                               frags):
    """ Insert Game Session Data to PostgreSQL Database

    Arguments:
        @param properties (tuple) form: (hostname, database_name, username, password)
            hostname: hostname of the PosgtreSQL server to connect to;
            database_name: name of the database to use;
            username: username of the database account
                on which the connection is being made;
            password: password of the database account.

        @param start_time (datetime.datetime obj): with time zone information
            corresponding to the start of the game session;

        @param end_time (datetime.datetime obj): with time zone information
            corresponding to the end of the game session;

        @param game_mode (str): Multiplayer mode of the game session (ASSAULT, TDM, FFA)

        @param map_name (str): Name of the map that was played

        @param frags (list): list of tuples of the following form
            (frag_time, killer_name[, victim_name, weapon_code])
            frag_time (required): (datetime.datetime) with time zone when the frag occurred;
            killer_name (required): (str) username of the player
                who fragged another or killed himself;
            victim_name (optional): (str) username of the player who has been fragged;
            weapon_code (optional): (str) code of the weapon that was used to frag.
    """

    # Data validation
    if not isinstance(start_time, datetime.datetime):
        logging.error("Data type is inappropriate")
    if not isinstance(end_time, datetime.datetime):
        logging.error("Data type is inappropriate")
    if not isinstance(game_mode, str):
        logging.error("Data type is inappropriate")
    if not isinstance(map_name, str):
        logging.error("Data type is inappropriate")
    if not isinstance(frags, list):
        logging.error("Data type is inappropriate")

    try:
        # connect to the PostgreeSQL server
        conn = psycopg2.connect(
            host=properties[0], user=properties[2],
            password=properties[3], dbname=properties[1])
        # create a cursor
        cur = conn.cursor()
        # pass data to match table
        cur.execute(const.POSTGRES_MATCH,
                    (start_time, end_time, game_mode, map_name))
        # Get UUID as match_id
        id_of_new_row = cur.fetchone()[0]
        logging.info("match_id: %s", id_of_new_row)

        # pass data to match_frag table
        for frag in frags:
            if len(frag) != 2:
                cur.execute(const.POSTGRES_KILL_OTHER, (id_of_new_row, *frag))
            else:
                cur.execute(const.POSTGRES_KILL_ITSELF, (id_of_new_row, *frag))
        conn.commit()
    except (psycopg2.Error) as error:
        logging.error('Unable to connect %s', error)
    finally:
        # Closing database connection
        if conn:
            # Close the communicateion with the PostGreSQL
            cur.close()
            conn.close()
            logging.info("PostgreSQL connection is closed")

    return id_of_new_row


# Waypoint 53: Determine Serial Killers
def calculate_serial_killers(frags):
    """Determine Serial Killers:
        A serial killer is a player who has killed several players
        before being killed or until the end of the match.

    Arguments:
        frags (list): a list of frags of game

    Returns:
        (dict): a dictionary of killers with their longest kill series
    """
    return __calculate_serial_killers_losers(frags, is_serial_killer=True)


# Waypoint 54: Determine Serial Losers
def calculate_serial_losers(frags):
    """Determine Serial Losers:
        A serial looser is a player who has been killed by several players
        before killing.

    Arguments:
        frags (list): a list of frags of game

    Returns:
        (dict): a dictionary of losers with their longest series
    """
    return __calculate_serial_killers_losers(frags, is_serial_killer=False)


def __remove_player_from_frag(original_tuple, element_to_remove):
    """Remove specific player from original tuple

    Arguments:
        original_tuple (tuple): a tuple
        element_to_remove (str): element in need of removing

    Returns:
        A new tuple
    """
    new_tuple = []
    for element in list(original_tuple):
        if not element == element_to_remove:
            new_tuple.append(element)
    return tuple(new_tuple)


def __calculate_serial_killers_losers(frags, is_serial_killer=False):
    """Determine Serial Killers or Losers

    Arguments:
        frags (list): a list of frags of game

    Keyword Arguments:
        is_serial_killer {bool}: (default: {False})
            True: calculate serial killer
            False: calculate serial looser

    Returns: (dict)
        is_serial_killer is True: a dictionary of killers with their longest kill series
        is_serial_killer is False: a dictionary of killers with their longest loose series
            where the key corresponds to the name of a player and the value
            corresponds to a list of frag times which contain
            the player's longest series.
            (frag_time, frag_time, victim_name, weapon_code)
    """

    if not isinstance(frags, list):
        logging.error("Data type is inappropriate")

    # An dictionary to store all serial killers/losers temporary
    serial_players_temp = {}
    # Final dict to store killers with their longest killers/losers series
    serial_killers_or_losers = {}
    # key is killer, val is the current longest serial count
    longest_serial = {}

    # Define current killer and current victim of each frag
    for frag in frags:
        player1 = frag[1]
        player2 = frag[2] if len(frag) != 2 else frag[1]

        if is_serial_killer:  # To calculate serial killer
            cur_killer, cur_victim = player1, player2
            # Add current killer and his frag to serial_players_temp
            if cur_killer != cur_victim:  # eleminate kill itself cases
                if cur_killer not in serial_players_temp:
                    serial_players_temp[cur_killer] = [frag]
                else:
                    serial_players_temp[cur_killer].append(frag)
        else:  # To calculate serial looser
            cur_killer, cur_victim = player2, player1
            if cur_killer not in serial_players_temp:
                serial_players_temp[cur_killer] = [frag]
            else:
                serial_players_temp[cur_killer].append(frag)

        # when the player is killed
        if cur_victim in serial_players_temp:
            frag_of_current_vict = serial_players_temp[cur_victim]
            # Remove name of frags
            frag_of_current_vict = tuple([__remove_player_from_frag(frag, cur_victim)
                                          for frag in frag_of_current_vict])
            # only if the number of frags of the player is larger than 1
            # considers as Kill series
            if len(frag_of_current_vict) != 1:
                # player has not existed in result dict (the first serial kill list)
                # -> 1. add all consecutive frags of the player to result dict
                # -> 2. Update longest_serial dict
                if cur_victim not in serial_killers_or_losers:
                    serial_killers_or_losers[cur_victim] = frag_of_current_vict
                    longest_serial[cur_victim] = len(frag_of_current_vict)

                # player existed in result dict
                # --> 1. Compare the number of victim of the player of temporary
                #     to the current longest serial count
                # -> 2. Update longest_serial dict
                else:
                    if longest_serial[cur_victim] == len(frag_of_current_vict):
                        serial_killers_or_losers[cur_victim] += frag_of_current_vict
                    elif longest_serial[cur_victim] < len(frag_of_current_vict):
                        serial_killers_or_losers[cur_victim] = frag_of_current_vict
                        longest_serial[cur_victim] = len(frag_of_current_vict)

            # remove current player from temp dict
            del serial_players_temp[cur_victim]

    # In case player still alive till the end of match
    for (killer, frag_of_killer) in serial_players_temp.items():
        if killer not in longest_serial:
            longest_serial[killer] = 0
        if len(frag_of_killer) == longest_serial[killer]:
            serial_killers_or_losers[killer] += serial_players_temp[killer]
        elif len(frag_of_killer) > longest_serial[killer]:
            serial_killers_or_losers[killer] = serial_players_temp[killer]
            longest_serial[killer] = len(frag_of_killer)

    logging.info("The killer's longest series: %s", longest_serial)

    return serial_killers_or_losers


def main():
    """Demonstrate and run test"""

    log_data = read_log_file('./logs/log08.txt')
    log_start_time = parse_log_start_time(log_data)
    frags = parse_frags(log_data)

    # TEST FOR WAYPOINT 48
    game_mode, map_name = parse_match_game_mode_and_map_name(log_data)
    start_time, end_time = parse_match_start_and_end_times(log_data, log_start_time, frags)
    properties = ('localhost', 'farcry', 'postgres', None)
    insert_match_to_postgresql(properties, start_time, end_time, game_mode, map_name, frags)

    # # TEST FOR WAYPOINT 54
    # serial_losers = calculate_serial_losers(frags)
    # for player_name, death_series in serial_losers.items():
    #     print('[%s]' % player_name)
    #     print('\n'.join([', '.join(([str(e) for e in death]))
    #                      for death in death_series]))

    # # TEST FOR WAYPOINT 53
    # serial_killers = calculate_serial_killers(frags)
    # for player_name, kill_series in serial_killers.items():
    #     print('[%s]' % player_name)
    #     print('\n'.join([', '.join(([str(e) for e in kill]))
    #                      for kill in kill_series]))


if __name__ == "__main__":
    main()
