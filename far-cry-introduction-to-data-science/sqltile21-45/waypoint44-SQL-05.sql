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
