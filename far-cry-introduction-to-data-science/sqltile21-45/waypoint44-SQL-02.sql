SELECT match_id, victim_name AS player_name,
0 AS kill_count,
0 AS suicide_count,
SUM(CASE WHEN victim_name IS NULL THEN 0 ELSE 1 END) AS death_count
FROM match_frag
WHERE victim_name IS NOT NULL
GROUP BY match_id, player_name
