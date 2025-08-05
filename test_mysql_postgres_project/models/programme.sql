MODEL (
    name programme,
    kind FULL,
    cron '@daily',
    gateway postgres,
    description 'Academic programmes'
);

SELECT 
     id
    ,programCode AS programme_code
    ,programName AS programme_name
FROM
    mysql_source.sunshine.programs p
