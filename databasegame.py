import psycopg2


class DatBase:

    def __init__(self):
        # подключение к базе данных
        self.connection = psycopg2.connect(database='j72508840_world_domination',
                                           user='j72508840_mazik',
                                           password='yZL_Au6z_NRjLVe',
                                           host='postgresql.j72508840.myjino.ru',
                                           port='5432')
        self.cursor = self.connection.cursor()

    # TODO:кнопка удаления

    def add_world(self,data):
        with self.connection:
            self.data = data
            query = "Insert into world (title,ecology) values (%s,%s)"
            self.cursor.executemany(query,[data])
            self.connection.commit()


    def add_country(self,data):
        with self.connection:
            self.data=data
            query = "Insert into country (title,balance,lifeStandard, nuclearProgram,rocket,worldId) values (%s,%s,%s,%s,%s,%s)"
            self.cursor.executemany(query,[data])
            self.connection.commit()


    def get_title_country_str(self,country):
        with self.connection:
            query = "select c.title from country as c inner join World W on W.id = c.worldId where W.id=1 and c.title='"+country+"'"
            self.cursor.execute(query)
            self.connection.commit()
            return format("".join(self.cursor.fetchone()))

    def get_max_id_select_world(self):
        with self.connection:
            self.cursor.execute("select id from World where id=(select max(id) from world)")
            self.connection.commit()
            return self.cursor.fetchone()[0]

    def get_max_id_select_country(self):
        with self.connection:
            self.cursor.execute("select id from Country where id=(select max(id) from country)")
            self.connection.commit()
            return self.cursor.fetchone()[0]

    def get_id_select_country(self, title):
        with self.connection:
            self.cursor.execute("select id from Country where worldId=(select max(id) from world) and title='"+title+"'")
            self.connection.commit()
            return self.cursor.fetchone()[0]

    def insert_city(self,data):
        with self.connection:
            self.data=data
            query = "Insert into city (title, lifeStandard, condition, shield, countryId) " \
                    "values (%s,%s,%s,%s,%s)"
            self.cursor.executemany(query,[data])
            self.connection.commit()

    def delete_city(self,data):
        with self.connection:
            self.data = data
            query = "DELETE FROM city where title=%s and countryId=%s"
            self.cursor.executemany(query, [data])
            self.connection.commit()

    def select_countries(self):
        with self.connection:
            quary = "Select * from country"
            self.cursor.execute(quary)
            self.connection.commit()
            return self.cursor.fetchall()

    def select_balance_ctr(self, title):
        with self.connection:
            query = "Select balance from Country where worldId=(select max(id) from world) and title='"+title+"'"
            self.cursor.execute(query)
            self.connection.commit()
            return self.cursor.fetchone()[0]

    def select_rockets(self, country):
        with self.connection:
            query = "Select rocket from Country where worldId=(select max(id) from world) and title='"+country+"'"
            self.cursor.execute(query)
            self.connection.commit()
            return self.cursor.fetchone()[0]

    def select_nuclear(self,country):
        with self.connection:
            query = "Select nuclearProgram from Country where worldId=(select max(id) from world) and title='"+country+"'"
            self.cursor.execute(query)
            self.connection.commit()
            return self.cursor.fetchone()[0]

    def select_ecology(self):
        with self.connection:
            query = "Select ecology from World where id=(select max(id) from world) "
            self.cursor.execute(query)
            self.connection.commit()
            return self.cursor.fetchone()[0]

    def get_id_city(self, id_country, title):
        with self.connection:
            self.cursor.execute("select id from City where countryId='"+id_country+"' and title = '"+title+"'")
            self.connection.commit()
            return self.cursor.fetchone()[0]

    def get_all_cities(self, id_country):
        with self.connection:
            query = "Select title from City where countryId='" + str(id_country) + "'"
            self.cursor.execute(query)
            self.connection.commit()
            return self.cursor.fetchall()

    def get_all_id_cities(self, id_country):
        with self.connection:
            query = "Select id from City where countryId='" + str(id_country) + "'"
            self.cursor.execute(query)
            self.connection.commit()
            return self.cursor.fetchall()

    def select_id_cities(self, id_country, title):
        with self.connection:
            query = "Select id from city where countryId='" + str(id_country) + "' and title='"+title+"'"
            self.cursor.execute(query)
            self.connection.commit()
            return self.cursor.fetchone()[0]

    def select_ls_city(self, id_country, title):
        with self.connection:
            query = "Select lifeStandard from city where countryId='" + str(id_country) + "' and title='"+title+"'"
            self.cursor.execute(query)
            self.connection.commit()
            return self.cursor.fetchone()[0]

    def select_shield_city(self, id_country, title):
        with self.connection:
            query = "Select shield from city where countryId='" + str(id_country) + "' and title='"+title+"'"
            self.cursor.execute(query)
            self.connection.commit()
            return self.cursor.fetchone()[0]
