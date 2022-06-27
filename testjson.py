import json

import requests

str_data = """
        {
          "worldId": 0,
          "friendlyCountry": [
            {
              "nuclearProgram": true,
              "rocket": 0,
              "ecology": 0,
              "countryId": 0,
              "friendlyCities": [
                {
                  "development": true,
                  "shield": true,
                  "cityId": 0
                },
                {
                  "development": true,
                  "shield": true,
                  "cityId": 0
                },
                {
                  "development": true,
                  "shield": true,
                  "cityId": 0
                },
                {
                  "development": true,
                  "shield": true,
                  "cityId": 0
                }
              ],
              "enemyCountries": [
                {
                  "sanctions": true,
                  "moneyTransfer": 0,
                  "countryId": 0,
                  "enemyCities": [
                    {
                      "bomb": true,
                      "cityId": 0
                    },
                    {
                      "bomb": true,
                      "cityId": 0
                    },
                    {
                      "bomb": true,
                      "cityId": 0
                    },
                    {
                      "bomb": true,
                      "cityId": 0
                    }
                  ]
                },
                {
                  "sanctions": true,
                  "moneyTransfer": 0,
                  "countryId": 0,
                  "enemyCities": [
                    {
                      "bomb": true,
                      "cityId": 0
                    },
                    {
                      "bomb": true,
                      "cityId": 0
                    },
                    {
                      "bomb": true,
                      "cityId": 0
                    },
                    {
                      "bomb": true,
                      "cityId": 0
                    }
                  ]
                },
                {
                  "sanctions": true,
                  "moneyTransfer": 0,
                  "countryId": 0,
                  "enemyCities": [
                    {
                      "bomb": true,
                      "cityId": 0
                    },
                    {
                      "bomb": true,
                      "cityId": 0
                    },
                    {
                      "bomb": true,
                      "cityId": 0
                    },
                    {
                      "bomb": true,
                      "cityId": 0
                    }
                  ]
                }
              ]
            }
          ]
        }"""
# data = json.loads(str_data)
# for country in data["friendlyCountry"]:
#     country["nuclearProgram"] = nuclearProgram
#     country["rocket"] = rocket
#     country["ecology"] = ecology
#     country["countryId"] = countryId
#     print(country)
#     for city in country["friendlyCities"]:
#         city["development"] = development
#         city["shield"] = shield
#         city["cityId"] = cityId
#         cityId += 1
#     for enemy_c in country["enemyCountries"]:
#         enemy_c["sanctions"] = sanctions
#         enemy_c["moneyTransfer"] = money
#         enemy_c["countryId"] = e_countryId
#         e_countryId += 1
#         for city_enemy in enemy_c["enemyCities"]:
#             city_enemy["bomb"] = bomb
#             city_enemy["cityId"] = en_cityId
#             en_cityId += 1
# newjson = json.dumps(data, indent=2)
# print(newjson)
print("\n")
# nuclearProgram = False
# rocket = 2
# ecology = 55
# countryId = 2
# development = True
# shield = False
# cityId = 3
# sanctions = False
# money = 1
# e_countryId = 1
# en_cityId = 1
# bomb = True


class all_to_Json:
    def convert_Json(self, Idworld: int, old_rockets_value: int, old_ecology_value: int, id_country: int,
        dic_fr_cities: dict, bomb_process: dict, dic_ctrId_CityId: dict, sanctin: dict):

        class Object:
            def toJSON(self):
                return json.dumps(self, default=lambda o: o.__dict__,
                                  sort_keys=True, indent=2)

        me = Object()
        me.friendlyCountry = Object()
        me.friendlyCountry.rocket = old_rockets_value
        me.friendlyCountry.ecology = old_ecology_value
        me.friendlyCountry.countryId = id_country
        me.worldId = Idworld
        me.friendlyCountry.friendlyCities = [Object(), Object(), Object(), Object()]
        i = 0
        for city in me.friendlyCountry.friendlyCities:
            city.development = dic_fr_cities['Development'][i]
            city.shield = dic_fr_cities['Shield'][i]
            city.cityId = dic_fr_cities['CityId'][i]
            i += 1
        i = 0

        me.friendlyCountry.enemyCountries = [Object(), Object(), Object()]
        for en_country in me.friendlyCountry.enemyCountries:
            en_country.sanctions = sanctin['Sanc'][i]
            en_country.moneyTransfer = 0
            en_country.countryId = dic_ctrId_CityId['CountryId'][i]
            en_country.enemyCities = [Object(), Object(), Object(), Object()]
            j = 0
            for en_city in en_country.enemyCities:
                en_city.bomb = bomb_process['Bomb'][j]
                en_city.cityId = dic_ctrId_CityId['CityId'][i][j]
                j += 1
            i += 1

        print(me.toJSON())
        json_params = me.toJSON()
        ### URL
        url = 'https://api.github.com/some/endpoint'
        resp = requests.post(url, data=json_params)

# if __name__ == '__main__':
#     js = all_to_Json()
#     newListCounties = ['USA', 'RUSAIN', 'HHui']
#     newListCities = ['Нью-Йорк', 'Лос-Анджелес', 'Сан-Франциско', 'Чикаго',
#                      'Геленджик', 'Москва', 'Калининград', 'Самара',
#                      'Минск', 'Витебск', 'Брест', 'Гродно']
#
#     Idworld = 111
#     old_rockets_value = 1
#     old_ecology_value = 22
#     id_country = 22
#     list_city_choos = ['Геленджик', 'Москва', 'Калининград', 'Самара']
#     list_development_fr_city = [60, 60, 60, 60]
#     list_shield_fr_city = [False, False, False, False]
#     list_CityId_fr = [1, 2, 3, 4]
#     dic_fr_cities = {"Title": list_city_choos,
#                      "Development": list_development_fr_city,
#                      "Shield": list_shield_fr_city,
#                      "CityId": list_CityId_fr}
#     bomb_process = {
#         "Title": [newListCities],
#         "Bomb": [False, False, False, False, False, False, False, False,
#                  False, False, False, False, False, False, False, False]
#     }
#
#     sanctin = {"Title": [newListCounties],
#                "Sanc": [False, False, False]}
#     bomb_process = {
#         "Title": [newListCities],
#         "Bomb": [False, False, False, False, False, False, False, False,
#                  False, False, False, False]
#     }
#     list_id_country_en = [5, 6, 8]
#     list_cityId_en = [[8, 10, 11, 12], [13, 14, 15, 16], [17, 18, 19, 20], [21, 22, 23, 24]]
#
#     dic_ctrId_CityId = {"CountryId": list_id_country_en, "CityId": list_cityId_en}
#     print(dic_ctrId_CityId['CityId'][1][2])
#     js.convert_Json(Idworld, old_rockets_value, old_ecology_value, id_country,
#                     dic_fr_cities, bomb_process, dic_ctrId_CityId, sanctin)
