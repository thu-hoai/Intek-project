# Elo Rating System

![Smash of Clans](smash_of_clans_eric_crampe.jpg)
(_Drawing courtesy of [Éric Crampe](https://www.linkedin.com/in/eric-crampe-47079843)_)

The [Elo rating system](https://en.wikipedia.org/wiki/Elo_rating_system) is a method for calculating the relative skill levels of players in games. It is named after its creator [Arpad Elo](https://en.wikipedia.org/wiki/Arpad_Elo), a Hungarian-American physics professor.

The difference in the ratings between two players serves as a predictor of the outcome of a match. Two players with equal ratings who play against each other are expected to score an equal number of wins.

A player's Elo rating is represented by a number which may change depending on the outcome of games played. After every game, the winning player takes points from the losing one. The difference between the ratings of the winner and loser determines the total number of points gained or lost after a game.

If the high-rated player wins, then only a few rating points will be taken from the low-rated player. However, if the lower-rated player scores an upset win, many rating points will be transferred. The lower-rated player will also gain a few points from the higher rated player in the event of a draw. This means that this rating system is self-correcting. Players whose ratings are too low or too high should, in the long run, do better or worse correspondingly than the rating system predicts and thus gain or lose rating points until the ratings reflect their true playing strength.

Create a file `elo.py` in which you will write all the code of the following waypoints.

## Waypoint 1: Class `Player`

Write a class `Player` that represents a player and his current Elo rating.

The constructor of the class `Player` takes two arguments `name` (a string) and `rating` (an optional decimal number) corresponding respectively to the name of the player and the initial Elo rating of this player (`0` if not defined). These values **MUST** be stored in two [**private**](https://docs.python.org/3.8/tutorial/classes.html#private-variables) instance [attributes](https://docs.python.org/3.8/tutorial/classes.html).

Write a **read-only [property](https://docs.python.org/3/library/functions.html#property)** `name`
of the class `Player` that returns the name of a player.

Write another [**property**](https://www.datacamp.com/community/tutorials/property-getters-setters) `rating` of the class `Player` that allows read and write accesses to the ranking of a player.

For example:

```python
>>> player = Player("LÝ Thanh Phú")
>>> player.name
'LÝ Thanh Phú'
>>> player.ranking
0.0
>>> player = Player("NGUYỄN Bá Trí", rating=33.1)
>>> player.name
'NGUYỄN Bá Trí'
>>> player.rating
33.1
>>> player.rating = 37.2
>>> player.name = "James Bond"
Traceback (most recent call last):
  File "<input>", line 1, in <module>
AttributeError: can't set attribute
```

## Waypoint 2: Class `MatchResult`

Write a class `MatchResult` that represents a match that occurred between two players.

The constructor of the class `MatchResult` takes five arguments `match_time`, `player1`, `player2`, `player1_points`,and `player2_points`, where:

- `match_time`: A string representing the date when the match occurred. The string complies to the format [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) (`YYYY-MM-DD`).

- `player1` and `player2`: 2 objects `Player` referring to two distinct players.

- `player1_points` and `player2_points`: 2 integer numbers representing the number of points of the first player, respectively the second play, won during this match.

These values **MUST** be stored in **private instance attributes** of the class `MatchResult`.

Write a **read-only properties** `match_time`, `player1`, `player1_points`, `player2`, and `player2_points` of the class `Player` that returns the value of the corresponding private instance attribute.

For example:

```python
>>> player1 = Player("LÝ Thanh Phú")
>>> player2 = Player("NGUYỄN Bá Trí")
>>> match_result = MatchResult('2019-11-13', player1, player2, 21, 19)
>>> match_result.match_time
datetime.datetime(2019, 11, 13, 0, 0)
>>> match_result.player1.name
'LÝ Thanh Phú'
>>> match_result.player2_points
19
>>> match_result = MatchResult('2019-11-13', player1, player1, 21, 19)
Traceback (most recent call last):
  File "<input>", line 1, in <module>
  File "<input>", line 25, in __init__
ValueError: arguments 'player1' and 'player2' must refer to distinct players
>>> match_result = MatchResult('2019-11-13', player1, player2, "foo", 19)
Traceback (most recent call last):
  File "<input>", line 1, in <module>
  File "<input>", line 28, in __init__
TypeError: arguments 'player1_points' and 'player2_points' must be integer numbers
```

_Note: You **SHOULD** use the module [`datetime`](https://docs.python.org/3.8/library/datetime.html) to parse the date & time string._

## Waypoint 3: Match Result CSV File Import

The result of matches between players is stored in a document composed of rows and columns.

Each row corresponds to the result of a match that occurred between two players. Each row is composed of 5 columns that store the following information in this particular order:

1. Date when the match occurred, expressed in the format [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601) (`YYYY-MM-DD`).
1. Name of the first player in this match.
1. Number of points won by this first player during this match.
1. Number of points won by the second player during this match.
1. Name of the second player in this match.

![Match Results Google Sheet Document](match_results_google_sheet.jpg)

This document is exported to a [comma-separated values (CSV)](https://en.wikipedia.org/wiki/Comma-separated_values) file (for instance, the file [badminton_math_results.csv](badminton_math_results.csv)).

Write a function `read_match_results` that takes an argument `csv_file_path_name`, a string, that defines the path and name of a CSV file containing match results.

The function returns `read_match_results` a list of objects `MatchResults` built with the data parsed from the file `csv_file_path_name`.

For example:

```python
>>> match_results = read_match_results('badminton_match_results.csv')
>>> match_results
[<__main__.MatchResult object at 0x10d362f28>, <__main__.MatchResult object at 0x10d362e48>, <__main__.MatchResult object at 0x10d386390>, <__main__.MatchResult object at 0x10d386470>, <__main__.MatchResult object at 0x10d386518>, <__main__.MatchResult object at 0x10d386278>, <__main__.MatchResult object at 0x10d386320>, <__main__.MatchResult object at 0x10d3864a8>, <__main__.MatchResult object at 0x10d3862e8>, <__main__.MatchResult object at 0x10d386588>, <__main__.MatchResult object at 0x10d386438>, <__main__.MatchResult object at 0x10d3865c0>, <__main__.MatchResult object at 0x10d386550>, <__main__.MatchResult object at 0x10d3866a0>, <__main__.MatchResult object at 0x10d386710>, <__main__.MatchResult object at 0x10d386668>, <__main__.MatchResult object at 0x10d386630>, <__main__.MatchResult object at 0x10d386240>, <__main__.MatchResult object at 0x10d386748>, <__main__.MatchResult object at 0x10d3866d8>, <__main__.MatchResult object at 0x10d386780>, <__main__.MatchResult object at 0x10d3867f0>, <__main__.MatchResult object at 0x10d3862b0>, <__main__.MatchResult object at 0x10d386898>, <__main__.MatchResult object at 0x10d3869b0>, <__main__.MatchResult object at 0x10d3867b8>, <__main__.MatchResult object at 0x10d3868d0>, <__main__.MatchResult object at 0x10d386978>, <__main__.MatchResult object at 0x10d3869e8>, <__main__.MatchResult object at 0x10d386a58>, <__main__.MatchResult object at 0x10d386a90>, <__main__.MatchResult object at 0x10d386940>, <__main__.MatchResult object at 0x10d386908>, <__main__.MatchResult object at 0x10d386b00>, <__main__.MatchResult object at 0x10d386b38>, <__main__.MatchResult object at 0x10d386ba8>, <__main__.MatchResult object at 0x10d386b70>, <__main__.MatchResult object at 0x10d386c18>, <__main__.MatchResult object at 0x10d386c50>]
>>> for match_result in match_results:
...     print(
...       f"[{match_result.match_time.strftime('%Y-%m-%d')}] "
...       f"{match_result.player1.name} "
...       f"{match_result.player1_points} - {match_result.player2_points} "
...       f"{match_result.player2.name}")
[2019-11-09] Alfred 17 - 15 Daniel
[2019-11-09] Daniel 15 - 7 Phong
[2019-11-09] Alfred 6 - 15 Phúc
[2019-11-09] Alfred 17 - 15 Phong
[2019-11-09] Phúc 15 - 11 Daniel
[2019-11-09] Phúc 15 - 8 Phong
[2019-11-09] Alfred 12 - 15 Daniel
[2019-11-09] Daniel 15 - 4 Phong
[2019-11-09] Phúc 15 - 7 Alfred
[2019-11-09] Alfred 15 - 4 Phong
[2019-11-09] Daniel 15 - 9 Phúc
[2019-11-09] Phúc 15 - 3 Phong
[2019-11-10] Phúc 15 - 9 Olivier
[2019-11-10] Phúc 15 - 9 Daniel
[2019-11-10] Phong 15 - 8 Olivier
[2019-11-10] Phong 15 - 12 Daniel
[2019-11-10] Alfred 10 - 15 Phúc
[2019-11-10] Alfred 15 - 6 Olivier
[2019-11-10] Daniel 15 - 3 Olivier
[2019-11-10] Alfred 15 - 6 Phong
[2019-11-10] Alfred 15 - 13 Daniel
[2019-11-10] Phong 15 - 9 Olivier
[2019-11-10] Phong 9 - 15 Daniel
[2019-11-10] Florian 7 - 15 Olivier
[2019-11-10] Florian 3 - 15 Daniel
[2019-11-10] Alfred 15 - 9 Phong
[2019-11-10] Phong 15 - 10 Florian
[2019-11-10] Daniel 15 - 10 Alfred
[2019-11-10] Daniel 12 - 15 Phong
[2019-11-10] Daniel 15 - 6 Florian
[2019-11-10] Alfred 15 - 9 Phong
[2019-11-10] Alfred 15 - 12 Daniel
[2019-11-10] Florian 9 - 15 Phong
[2019-11-10] Florian 7 - 15 Alfred
[2019-11-10] Phong 12 - 15 Daniel
[2019-11-13] Daniel 21 - 6 Alfred
[2019-11-13] Daniel 21 - 14 Alfred
[2019-11-13] Daniel 16 - 21 Alfred
[2019-11-13] Daniel 21 - 19 Alfred
```

## Waypoint 4: Command-Line Interface Script

Update your file `elo.py` to transform it to a command-line interface (CLI) script.

This requires declaring a [shebang](<https://en.wikipedia.org/wiki/Shebang_(Unix)>) at the beginning of your script to indicate that this script needs to be run via a Python interpreter.

This also requires you to [change the permission](https://en.wikipedia.org/wiki/Chmod) of your file `elo.py` to allow
executing your file as a program.

This requires to define a [main function](https://realpython.com/python-main-function/) `main` in your file `elo.py`, and to define an entry point in your script so that, when the Python interpreter is running your file as the main program, the Python interpreter eventually calls your main function:

```python
def main():
    pass

__name__ == '__main__
    main()
```

Once you have completed this step, you should be able to execute your script `elo.py` from the command line as follows:

```bash
$ ./elo.py
```

## Waypoint 5: Command-Line Arguments Support

Write a function `parse_arguments` that takes no argument and that returns an object [`Namespace`](https://docs.python.org/3.8/library/argparse.html) corresponding to the command-line arguments passed to your script `elo.py`.

Your script `elo.py` **MUST** accept one required command-line argument `-f` or `--file` that specifies the path of the CSV file containing results of matches between players.

```bash
$ ./elo.py --help
usage: elo.py [-h] -f FILE

ELO Rating Calculator

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  specify the path of the CSV file containing results of
                        matches between players
```

## Waypoint 6: Expected Score Calculation

Add the instance method `calculate_expected_score` to your class `Player` that takes one argument `opponent`, an object `Player` representing a opponent.

The method `calculate_expected_score` return the [expected Elo score](https://en.wikipedia.org/wiki/Elo_rating_system#Mathematical_details) of the player if he were competing against the other player:

![Player Expected Score](player_expected_score_formula.svg).

For example:

```python
>>> player1 = Player("LÝ Thanh Phú", rating=256)
>>> player2 = Player("NGUYỄN Bá Trí", rating=82)
>>> player1.calculate_expected_score(player2)
0.7313778578393882
>>> player2.calculate_expected_score(player1)
0.2686221421606117
```

According to their respective current Elo rating, there is 73% chance that LÝ Thanh Phú would win against NGUYỄN Bá Trí if they were playing a match together.

## Waypoint 7: Match Outcome Player Score Calculation

Write a function `calculate_match_outcome_player_score` that takes two arguments `player_points` and `opponent_points` (both integer numbers) representing respectively the points that a player and his opponent won during a match.

The function `calculate_match_outcome_player_score` returns the score of the player `player`. If the player won against the opponent, the function returns `1`. If the player lost against the opponent, the function returns `0`. If the game is a draw, the function returns `0.5`.

For example:

```python
>>> calculate_match_outcome_player_score(21, 19)
1
>>> calculate_match_outcome_player_score(10, 21)
0
>>> calculate_match_outcome_player_score(21, 21)  # "21 - 21"?! What?!... :))))
0.5
```

_Note: In racquet sports, such as badminton, tennis, table tennis, squash, a game cannot be a draw. However our Elo rating calculator script is not limited to sport games. It works also with other games such as chess where a draw between two players may happen._

## Waypoint 8: Player Rating Update Calculation

Write a function `calculate_player_updated_elo_rating` that takes five arguments:

- `player`: An object `Player` representing a player.
- `opponent`: An object `Player` representing an opponent.
- `player_points`: The points won by the player during a match.
- `opponent_points`: The points won by the opponent during this same match.
- `K` (optional): The value of the Elo _K-factor_ to use. By default, `32`.

The function `calculate_player_updated_elo_rating` return the new Elo rating of the player `player`:

![Player Updating Rating Formula](player_updating_rating_formula.svg)

For example:

```python
>>> player1 = Player("LÝ Thanh Phú", rating=256)
>>> player2 = Player("NGUYỄN Bá Trí", rating=82)

# New Elo ratings of two players with a score of 21-19
>>> calculate_player_updated_elo_rating(player1, player2, 21, 19)
264.59590854913955
>>> calculate_player_updated_elo_rating(player2, player1, 19, 21)
73.40409145086042

# New Elo ratings of two players with a score of 21-0
>>> calculate_player_updated_elo_rating(player1, player2, 21, 0)
264.59590854913955
>>> calculate_player_updated_elo_rating(player2, player1, 0, 21)
73.40409145086042
```

_Note: The standard Elo rating system doesn't take into account the difference of points won by two players during a match. It only takes into account who won, who lost._

## Waypoint 9: Player Rating Update

Write a function `update_player_elo_ratings` that takes one argument `match_result` (an object `MatchResult`). The function updates the Elo rating of two players depending on the outcome of the match they played together.

For example:

```python
>>> import datetime
>>> player1 = Player("LÝ Thanh Phú", rating=256)
>>> player2 = Player("NGUYỄN Bá Trí", rating=82)
>>> match_result = MatchResult(datetime.datetime.strptime('2019-11-13', '%Y-%m-%d'), player1, player2, 21, 19)
>>> update_player_elo_ratings(match_result)
>>> player1.rating
264.59590854913955
>>> player2.rating
73.40409145086042
```

## Waypoint 10: Match Results Processing

Write a function `process_match_results` that takes one argument `match_results` (a list of objects `MatchResult`). The function iterates over all the objects `MatchResult` of the list `match_results` and updates the Elo rating of the players.

For example:

```python
>>> match_results = read_match_results('badminton_match_results.csv')
>>> process_match_results(match_results)

# Display players and their respective Elo rating sorted by descending
# value.
>>> players = set()
>>> for match_result in match_results:
...     players.add(match_result.player1)
...     players.add(match_result.player2)
>>> for rank, player in enumerate(sorted(players, key=lambda player: player.rating, reverse=True), start=1):
...     print(f"{rank}. {player.name} ({round(player.rating, 2)})")
1. Phúc (92.36)
2. Daniel (65.26)
3. Alfred (33.3)
4. Phong (-43.3)
5. Olivier (-58.13)
6. Florian (-89.49)
```

_Note: You need to make sure that your function `process_match_results` processes match results in their chronological order. The match results may have been entered in whatever order in the initial sheet document._

## Waypoint 11: Rating Update Calculation Improvement

You may have noticed that the classic Elo rating system only takes into account the outcome of a game to update the rating of a player, whether this player won, lost, or did a draw.

For example, your Elo rating will be updated exactly the same way, whatever the points you and your opponent won during this match. Either you win 21-0 or you win 25-23, that would not make any difference.

A friend of yours would repeatedly win between 21-17 and 21-19 against you, his Elo rating will continuously increase, match after match. There would be a huge gap between his Elo rating and yours, while your respective levels are quite similar:

```python
>>> import random
>>> player1 = Player("LÝ Thanh Phú")
>>> player2 = Player("NGUYỄN Bá Trí")
>>> match_results = [
...     MatchResult(
...         datetime.datetime.strptime('2019-11-13', '%Y-%m-%d'),
...         player1,
...         player2,
...         21,
...         random.randint(17, 19))
...     for _ in range(20)]
process_match_results(match_results)
>>> player1.rating
165.4351440208619
>>> player2.rating
-165.43514402086188
```

On another, let's imagine that a friend of yours used to be a lot better than you, repeatedly winning between 21-1 and 21-5 against you. However, after taking lessons, you start to play a lot better than before. Your friend still win, but now only between 21-17 and 21-19. However, with the classic Elo rating system, the Elo rating of your friend will still increase, will yours will still decrease:

```python
>>> import random
>>> player1 = Player("LÝ Thanh Phú")
>>> player2 = Player("NGUYỄN Bá Trí")

# Phú used to win between 21-1 and 21-5 against Trí:
>>> match_results = [
...     MatchResult(
...        datetime.datetime.strptime('2019-11-13', '%Y-%m-%d'),
...         player1,
...         player2,
...         21,
...         random.randint(1, 5))
...     for _ in range(20)]
>>> process_match_results(match_results)
>>> player1.rating
165.4351440208619
>>> player2.rating
-165.43514402086188

# Now, Phú still wins against to win Trí but only between 21-17 and 21-19:
>>> match_results = [
...     MatchResult(
...         datetime.datetime.strptime('2019-11-13', '%Y-%m-%d'),
...         player1,
...         player2,
...         21,
...         random.randint(17, 19))
...     for _ in range(5)]
>>> process_match_results(match_results)
>>> player1.rating
184.59464770862184
>>> player2.rating
-184.5946477086218
```

That's not fair. These Elo ratings don't greatly represent the difference of your respective levels. The Elo rating calculation should reflect the real difference of level between two players.

Update your function `calculate_match_outcome_player_score` by adding an optional argument `advanced_calculation` (a boolean with default value `False`). If the value `False` is passed, the function uses the classic Elo rating calculation. If the value `True` is passed, the function uses an advanced calculation method you need to write.

This advanced method calculates the score of the player based on the difference of points won by the players and his opponent during the match. The score is not a value among `1.0` (win), `0.5` (draw), and `0.0` (loss), but a value between `1.0` and `0.0`. For instance, if the player was winning the match 21-0, his Elo score would be `1.0`. However, if the player was only winning the match 23-21, his Elo score would only be, for instance, `0.5227272727272727`, which looks like a draw more than a win.

For example:

```python
>>> player1 = Player("LÝ Thanh Phú")
>>> player2 = Player("NGUYỄN Bá Trí")

# Phú used to win between 21-1 and 21-5 against Trí:
>>> match_time = datetime.datetime.strptime('2019-11-13', '%Y-%m-%d')
>>> match_results = [
...     MatchResult(match_time, player1, player2, 21, 1),
...     MatchResult(match_time, player1, player2, 21, 4),
...     MatchResult(match_time, player1, player2, 21, 2),
...     MatchResult(match_time, player1, player2, 21, 5),
...     MatchResult(match_time, player1, player2, 21, 3),
]
>>> process_match_results(match_results)
>>> player1.rating
49.98451794411288
>>> player2.rating
-49.98451794411287

# Now, Trí improved his game and is now very close to Phú:
>>> process_match_results([MatchResult(match_time, player1, player2, 21, 19)])
>>> player1.rating
46.30375203495154
>>> player2.rating
-46.30375203495153

>>> process_match_results([MatchResult(match_time, player1, player2, 21, 18)])
>>> player1.rating
43.3679964599975
>>> player2.rating
-43.367996459997485
```

Meanwhile Phú is still winning, his rating is decreasing, while Trí's rating is increasing. Indeed, while Phú is still winning, Trí's rating will be always lower than Phú's rating, but closer and closer.

Update your script to support the optional command-line argument `-a` or `--advanced-calculation` (a boolean) that allows to use this new Elo rating calculation method:

```bash
$ ./elo.py --help
usage: elo.py [-h] -f FILE [-a]

ELO Rating Calculator

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  specify the path of the CSV file containing results of
                        matches between players
  -a, --advanced-calculation
                        specify whether to use the advanced Elo rating based
                        on the players' point difference in a match
```

For example:

```bash
# Classic Elo rating system
$ ./elo.py --file badminton_match_result.csv
2019-11-14 11:46:58,398 [INFO] Loading match results from badminton_match_results.csv...
2019-11-14 11:46:58,403 [INFO] 39 match results
2019-11-14 11:46:58,403 [INFO] [2019-11-09] Match Alfred 17-15 Daniel
2019-11-14 11:46:58,403 [INFO]   Alfred: 0.0 -> 16.0 (16.0)
2019-11-14 11:46:58,403 [INFO]   Daniel: 0.0 -> -16.0 (-16.0)
2019-11-14 11:46:58,403 [INFO] [2019-11-09] Match Daniel 15-7 Phong
2019-11-14 11:46:58,403 [INFO]   Daniel: -16.0 -> 0.74 (16.74)
2019-11-14 11:46:58,403 [INFO]   Phong: 0.0 -> -16.74 (-16.74)
(...)
2019-11-14 11:46:58,424 [INFO] [2019-11-13] Match Daniel 21-19 Alfred
2019-11-14 11:46:58,424 [INFO]   Daniel: 49.26 -> 65.26 (16.0)
2019-11-14 11:46:58,424 [INFO]   Alfred: 49.3 -> 33.3 (-16.0)
2019-11-14 11:46:58,424 [INFO] Current leaderboard:
2019-11-14 11:46:58,424 [INFO] 1. Phúc (92.36)
2019-11-14 11:46:58,424 [INFO] 2. Daniel (65.26)
2019-11-14 11:46:58,424 [INFO] 3. Alfred (33.3)
2019-11-14 11:46:58,424 [INFO] 4. Phong (-43.3)
2019-11-14 11:46:58,425 [INFO] 5. Olivier (-58.13)
2019-11-14 11:46:58,425 [INFO] 6. Florian (-89.49)

# Advanced Elo rating system
$ ./elo.py -a --file badminton_match_results.csv
2019-11-14 11:48:20,496 [INFO] Loading match results from badminton_match_results.csv...
2019-11-14 11:48:20,506 [INFO] 39 match results
2019-11-14 11:48:20,506 [INFO] [2019-11-09] Match Alfred 17-15 Daniel
2019-11-14 11:48:20,506 [INFO]   Alfred: 0.0 -> 1.0 (1.0)
2019-11-14 11:48:20,506 [INFO]   Daniel: 0.0 -> -1.0 (-1.0)
2019-11-14 11:48:20,507 [INFO] [2019-11-09] Match Daniel 15-7 Phong
2019-11-14 11:48:20,507 [INFO]   Daniel: -1.0 -> 4.86 (5.86)
2019-11-14 11:48:20,507 [INFO]   Phong: 0.0 -> -5.86 (-5.86)
(...)
2019-11-14 11:48:20,528 [INFO] [2019-11-13] Match Daniel 21-19 Alfred
2019-11-14 11:48:20,528 [INFO]   Daniel: 34.91 -> 34.63 (-0.28)
2019-11-14 11:48:20,528 [INFO]   Alfred: 11.5 -> 11.78 (0.28)
2019-11-14 11:48:20,528 [INFO] Current leaderboard:
2019-11-14 11:48:20,528 [INFO] 1. Daniel (34.63)
2019-11-14 11:48:20,528 [INFO] 2. Phúc (31.05)
2019-11-14 11:48:20,529 [INFO] 3. Alfred (11.78)
2019-11-14 11:48:20,529 [INFO] 4. Phong (-21.7)
2019-11-14 11:48:20,529 [INFO] 5. Olivier (-22.64)
2019-11-14 11:48:20,529 [INFO] 6. Florian (-33.12)
```

_Note: The output of our script is just given as an example. The values are correct. The logging information output may differ from your script._
