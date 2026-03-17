select name,
       street,
       city,
       zip,
       partner_latitude as lat,
       partner_longitude as lon,
       country_id
  from res_partner;

select column_name,
       data_type,
       character_maximum_length,
       is_nullable
  from information_schema.columns
 where table_name = 'res_partner'
 order by ordinal_position;

select column_name,
       data_type
  from information_schema.columns
 where table_name = 'res_partner'
   and column_name like '%country%';


select p.name,
       p.street,
       p.street2,
       p.city,
       p.zip,
       p.partner_latitude as lat,
       p.partner_longitude as lon,
       c.name as country_name  -- For geocoding
  from res_partner p
  left join res_country c
on p.country_id = c.id
 where p.active = true
   and p.is_company = false;

select p.name,
       p.street,
       p.city,
       p.zip,
       p.partner_latitude as lat,
       p.partner_longitude as lon,
       c.code as country_code
  from res_partner p
  left join res_country c
on p.country_id = c.id
 where p.active = true
   and p.is_company = false;