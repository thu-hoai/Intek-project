SELECT match_id, killer_name AS player_name,
COUNT(victim_name) AS kill_count,
SUM(CASE WHEN victim_name IS NULL THEN 1 ELSE 0 END) AS suicide_count,
0 AS death_count
FROM match_frag
GROUP BY match_id, player_name
