SELECT A.match_id, A.player_name, A.kill_count, A.suicide_count, SUM(A.death_count) AS death_count

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
	sum(CASE WHEN victim_name IS NULL THEN 0 ELSE 1 END) AS death_count
	FROM match_frag
	WHERE victim_name IS NOT NULL
	GROUP BY match_id, player_name) AS A

GROUP BY match_id, player_name
