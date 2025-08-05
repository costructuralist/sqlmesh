MODEL (
    name programme,
    kind FULL,
    cron '@daily',
    gateway mysql_target,
    description 'Academic programmes'
);

SELECT 
     id
    ,programCode AS programme_code
    ,programName AS programme_name
FROM
    mysql_source.sunshine.programs p
