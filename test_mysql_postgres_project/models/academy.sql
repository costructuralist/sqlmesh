MODEL (
    name academy,
    kind FULL,
    cron '@daily',
    gateway postgres,
    description 'Academy summary with student and course counts'
);

SELECT 
     id
    ,academicTypeCode AS academic_type_code
    ,academyName AS academy_name
FROM
    mysql_source.sunshine.academies a
