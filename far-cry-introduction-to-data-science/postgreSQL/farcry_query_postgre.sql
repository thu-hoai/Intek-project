-- Waypoint 49: Determine the Most Versatile Killer
SELECT
  match_id,
  killer_name,
  COUNT(DISTINCT weapon_code) AS weapon_count
FROM match_frag
WHERE
  victim_name IS NOT NULL
GROUP BY
  match_id,
  killer_name
ORDER BY
  match_id,
  weapon_count DESC;

-- Waypoint 50: Determine Players Favorite Victim
  WITH A AS (
    SELECT
      match_id,
      killer_name,
      victim_name,
      COUNT(victim_name) AS kill_count,
      ROW_NUMBER () OVER (
        PARTITION BY match_id,
        killer_name
        ORDER BY
          count(victim_name) DESC
      ) AS row_no
    FROM match_frag
    GROUP BY
      match_id,
      killer_name,
      victim_name
  )
SELECT
  match_id,
  killer_name AS player_name,
  victim_name AS favorite_victim_name,
  kill_count
FROM A
WHERE
  row_no BETWEEN 1
  AND 1
GROUP BY
  match_id,
  killer_name,
  victim_name,
  kill_count;

-- Waypoint 51: Determine Players Worst Enemy
  WITH A AS (
    SELECT
      match_id,
      killer_name,
      victim_name,
      COUNT(victim_name) AS kill_count,
      ROW_NUMBER() OVER(
        PARTITION BY match_id,
        victim_name
        ORDER BY
          COUNT(victim_name) DESC
      ) AS row_num
    FROM match_frag
    GROUP BY
      match_id,
      killer_name,
      victim_name
  )
SELECT
  A.match_id,
  A.victim_name AS player_name,
  A.killer_name AS worst_enemy_name,
  kill_count
FROM A
WHERE
  row_num BETWEEN 1
  AND 1

-- Waypoint 52: Determine Players Killer Class
CREATE
OR REPLACE FUNCTION get_killer_class(weapon_code TEXT) RETURNS TEXT AS $$ DECLARE weapon_class TEXT;
BEGIN CASE
  WHEN weapon_code IN ('Machete', 'Falcon', 'MP5') THEN weapon_class = 'Hitman';
  WHEN weapon_code IN ('SniperRifle') THEN weapon_class = 'Sniper';
  WHEN weapon_code IN ('AG36', 'OICW', 'P90', 'M4', 'Shotgun', 'M249') THEN weapon_class = 'Commando';
  WHEN weapon_code IN (
    'Rocket',
    'VehicleRocket',
    'HandGrenade',
    'StickExplosive',
    'Boat',
    'Vehicle',
    'VehicleMountedRocketMG',
    'VehicleMountedAutoMG',
    'MG',
    'VehicleMountedMG',
    'OICWGrenade',
    'AG36Grenade'
  ) THEN weapon_class = 'Psychopath';
END CASE;
RETURN weapon_class;END;
$$ LANGUAGE plpgsql;


WITH A AS (
  SELECT
    match_id,
    killer_name,
    weapon_code,
    COUNT(weapon_code) AS kill_count,
    ROW_NUMBER() OVER (
      PARTITION BY match_id,
      killer_name
      ORDER BY
        COUNT(weapon_code) DESC
    ) AS row_num
  FROM match_frag
  WHERE
    weapon_code IS NOT NULL
  GROUP BY
    match_id,
    killer_name,
    weapon_code
)
SELECT
  A.match_id,
  A.killer_name AS player_name,
  A.weapon_code,
  kill_count,
  get_killer_class(weapon_code) AS killer_class
FROM A
WHERE
  row_num BETWEEN 1
  AND 1