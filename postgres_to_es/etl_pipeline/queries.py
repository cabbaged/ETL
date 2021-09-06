get_entity_ids = "SELECT id, modified " \
                 "FROM {entity} " \
                 "WHERE modified > '{start_date}' " \
                 "ORDER BY modified " \
                 "LIMIT 100;"

get_related_filmwork_ids = "SELECT fw.id, fw.modified " \
                   "FROM film_work fw " \
                   "LEFT JOIN {entity}_film_work efw ON efw.film_work_id = fw.id " \
                   "WHERE efw.{entity}_id IN {entity_ids} " \
                   "ORDER BY fw.modified " \
                   "LIMIT 100; "

get_data_for_load = "SELECT " \
                    "   fw.id as fw_id, " \
                    "   fw.title, " \
                    "   fw.description, " \
                    "   fw.rating, " \
                    "   fw.type, " \
                    "   fw.created, " \
                    "   fw.modified, " \
                    "   pfw.role, " \
                    "   p.id, " \
                    "   p.first_name, " \
                    "   p.second_name, " \
                    "   g.name as genre_name " \
                    "FROM film_work fw " \
                    "LEFT JOIN person_film_work pfw ON pfw.film_work_id = fw.id " \
                    "LEFT JOIN person p ON p.id = pfw.person_id " \
                    "LEFT JOIN genre_film_work gfw ON gfw.film_work_id = fw.id " \
                    "LEFT JOIN genre g ON g.id = gfw.genre_id " \
                    "WHERE fw.id IN {} " \
                    "ORDER BY fw_id;"
