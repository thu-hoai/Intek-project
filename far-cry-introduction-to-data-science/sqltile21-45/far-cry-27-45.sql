-- Waypoint 27: Select Start and End Times of Matches
SELECT match_id, start_time, end_time
FROM match;

-- Waypoint 28: Select Game Mode and Map Name of Matches
SELECT match_id, game_mode, map_name
FROM match;

-- Waypoint 29: Select all Columns of Matches
SELECT * FROM match;

-- Waypoint 30: Select distinct Killer Names
-- Return the distinct names of players who have killed another player
SELECT DISTINCT killer_name
FROM match_frag
WHERE victim_name IS NOT NULL;

-- Waypoint 31: Order the List of Killer Names
SELECT DISTINCT killer_name
FROM match_frag
WHERE victim_name IS NOT NULL
ORDER BY killer_name
COLLATE NOCASE ASC;

-- Waypoint 32: Calculate the Number of Matches
SELECT COUNT(*)
FROM match;

-- Waypoint 33: Calculate the number of Kills and Suicides
SELECT COUNT(*) AS kill_suicide_count
FROM match_frag;

-- Waypoint 34: Calculate the Number of Suicides
SELECT COUNT(*) AS suicide_count
FROM match_frag
WHERE victim_name IS NULL;

-- Waypoint 35: Calculate the Number of Kills (1)
SELECT COUNT(*) AS kill_count
FROM match_frag
WHERE victim_name IS NOT NULL;

-- Waypoint 36: Calculate the Number of Kills (2)
SELECT COUNT(victim_name) AS kill_count
FROM match_frag;

-- Waypoint 37: Calculate the Number of Kills and Suicides per Match
SELECT match_id,
COUNT(*) AS kill_suicide_count
FROM match_frag
GROUP BY match_id;

-- Waypoint 38: Calculate and Order the Number of Kills and Suicides per Match
SELECT match_id,
COUNT(*) AS kill_suicide_count
FROM match_frag
GROUP BY match_id
ORDER BY kill_suicide_count DESC;

-- Waypoint 39: Calculate and Order the Number of Suicides per Match
SELECT match_id,
COUNT(*) AS suicide_count
FROM match_frag
WHERE victim_name IS NULL
GROUP BY match_id
ORDER BY suicide_count;

-- Waypoint 40: Calculate and Order the Total Number of Kills per Player
SELECT all_player.player_name,
SUM(
	CASE
		WHEN match_frag.victim_name IS NOT NULL -- eleminate suicide players
		AND all_player.player_name == match_frag.killer_name
		THEN 1 ELSE 0
	END) AS kill_count

FROM
	match_frag,
	--table of all players
	(SELECT DISTINCT killer_name AS player_name
	FROM match_frag
	GROUP BY player_name
	UNION -- get unique by UNION
	SELECT DISTINCT victim_name AS player_name
	FROM match_frag
	WHERE victim_name IS NOT NULL) AS all_player

GROUP BY all_player.player_name
--Sort in descending order by the number of kills,
-- then sorted by their ascending alphabetical order.
ORDER BY kill_count DESC, all_player.player_name ASC;



-- Waypoint 41: Calculate and Order the Number of Kills per Player and per Match
SELECT A.match_id, A.player_name,
SUM(
	CASE
		WHEN A.match_id == match_frag.match_id
		AND a.player_name == match_frag.killer_name
		AND match_frag.victim_name IS NOT NULL -- eleminate suicide players
		THEN 1 ELSE 0
	END) AS kill_count

FROM
	match_frag,
	--table of all players with attribute: match_id, player_name
	(SELECT DISTINCT match_id, killer_name AS player_name
	FROM match_frag
	GROUP BY player_name
	UNION -- get unique by UNION
	SELECT DISTINCT match_id, victim_name AS player_name
	FROM match_frag
	WHERE victim_name IS NOT NULL) AS A

GROUP BY A.match_id, A.player_name
--Sort in ascending identification number of match,
--then by the descending number of kills for each match.
ORDER BY A.match_id, kill_count DESC;


-- Waypoint 42: Calculate and Order the Number of Deaths per Player and per Match
-- returns the number of deaths (player that has been killed by another) per player and per match
SELECT A.match_id, A.player_name,
SUM(
	CASE
		WHEN A.match_id == match_frag.match_id
		AND A.player_name == match_frag.victim_name
		THEN 1 ELSE 0
	END) AS death_count

FROM
	match_frag,
	--table of all players with attribute: match_id, player_name
	(SELECT DISTINCT match_id, killer_name AS player_name
	FROM match_frag
	GROUP BY player_name
	UNION
	SELECT DISTINCT match_id, victim_name AS player_name
	FROM match_frag
	WHERE victim_name IS NOT NULL -- eliminate suicide
	) AS A

GROUP BY A.match_id, A.player_name
--Sort the result by ascending identification number of match,
-- and then by the descending number of deaths for each match.
ORDER by A.match_id, death_count DESC;



-- Waypoint 43: Select Matches and Calculate the Number of Players and the Number of Kills and Suicides
SELECT
  A.match_id,
  match.start_time,
  match.end_time,
  COUNT(DISTINCT A.player_name) AS player_count,
  SUM(
    CASE
      WHEN match_frag.killer_name == A.player_name THEN 1
      ELSE 0
    END
  ) AS kill_suicide_count
FROM match,
  match_frag,
  --table of all players with attribute: match_id and player_name
  (
    SELECT
      DISTINCT match_id,
      killer_name AS player_name
    FROM match_frag
    GROUP BY
      player_name
    UNION
    SELECT
      DISTINCT match_id,
      victim_name AS player_name
    FROM match_frag
  ) AS A
WHERE
  A.match_id == match.match_id
  AND A.match_id == match_frag.match_id
GROUP BY
  A.match_id -- Sort the result in ascending order by start date and time of these matches.
ORDER BY
  match.start_time ASC;


--Waypoint 44: Calculate Players Efficiency per Match
--FINAL FILE SQL-05
SELECT match_id, player_name, kill_count, suicide_count,
SUM(death_count) AS death_count,
ROUND(100*(kill_count +0.0)/(kill_count + SUM(death_count) + suicide_count+0.0), 2) AS efficiency

FROM
	(SELECT match_id, killer_name AS player_name,
	COUNT(victim_name) AS kill_count,
	SUM(CASE WHEN victim_name IS NULL THEN 1 ELSE 0 END) AS suicide_count,
	0 AS death_count
	FROM match_frag
	GROUP BY match_id, player_name

	UNION

	SELECT match_id, victim_name AS player_name,
	0 AS kill_count,
	0 AS suicide_count,
	SUM(CASE WHEN victim_name IS NULL THEN 0 ELSE 1 END) AS death_count
	FROM match_frag
	WHERE victim_name IS NOT NULL
	GROUP BY match_id, player_name) AS A

GROUP BY match_id, player_name
ORDER BY match_id ASC, efficiency DESC

-- Waypoint 45: Create Players Match Efficiency View
DROP TABLE IF EXISTS match_statistics;

CREATE VIEW IF NOT EXISTS match_statistics AS
SELECT
	match_id, player_name, kill_count, suicide_count,
	SUM(death_count) AS death_count,
	ROUND(100*(kill_count+0.0)/(kill_count + SUM(death_count) + suicide_count+0.0), 2) AS efficiency

FROM
	(SELECT match_id, killer_name AS player_name,
	COUNT(victim_name) AS kill_count,
	SUM(CASE WHEN victim_name IS NULL THEN 1 ELSE 0 END) AS suicide_count,
	0 AS death_count
	FROM match_frag
	GROUP BY match_id, player_name

	UNION

	SELECT match_id, victim_name AS player_name,
	0 AS kill_count,
	0 AS suicide_count,
	SUM(case when victim_name IS NULL THEN 0 ELSE 1 END) AS death_count
	FROM match_frag
	WHERE victim_name IS NOT NULL
	GROUP BY match_id, player_name) AS A

GROUP BY match_id, player_name
ORDER BY match_id ASC, efficiency DESC;



