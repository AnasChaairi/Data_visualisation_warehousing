CREATE OR REPLACE TABLE `airports-data-warehousing.airports_data_visualisation.table_analytics` AS (
SELECT f.name , f.ident  , f.scheduled_service , f.score, t.municipality , d.update_year , d.update_month , d.update_hour , d.update_day , r.latitude_deg , r.elevation_ft,r.longitude_deg , l.region_name
FROM 
`airports-data-warehousing.airports_data_visualisation.fact_table` f
JOIN `airports-data-warehousing.airports_data_visualisation.datetime_dim` d  ON f.datetime_id=d.datetime_id
JOIN `airports-data-warehousing.airports_data_visualisation.airport_type_dim` p  ON p.type_id=f.type_id
JOIN `airports-data-warehousing.airports_data_visualisation.cities_dim` t  ON t.city_id=f.city_id  
JOIN `airports-data-warehousing.airports_data_visualisation.regions_dim` l  ON t.region_id=l.region_id   
JOIN `airports-data-warehousing.airports_data_visualisation.airport_coordinates_dim` r ON r.coordinates_id=f.coordinates_id );
