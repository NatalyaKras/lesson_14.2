import sqlite3
import json

def selectall(title):
    conn = sqlite3.connect('netflix.db')
    cur = conn.cursor()
    cur.execute(f'''
select * from netflix where title = '{title}';
''')
    return cur.fetchall()

def sql_data_to_dict(select_query):
  try:
      con = sqlite3.connect('netflix.db')
      con.row_factory = sqlite3.Row
      things = con.execute(select_query).fetchall()
      unpacked = [{k: item[k] for k in item.keys()} for item in things]
      return unpacked
  except Exception as e:
      print(f"Ошибка выполнения SQL запроса")
      return []
  finally:
      con.close()

def sql_data_to_list_of_dicts(select_query):
  try:
      con = sqlite3.connect('netflix.db')
      con.row_factory = sqlite3.Row
      things = con.execute(select_query).fetchall()
      unpacked = [{'title': item[2],'release_year': item[7] } for item in things]

      return unpacked
  except Exception as e:
      print(f"Ошибка выполнения SQL запроса")
      return []
  finally:
      con.close()


def sql_data_to_list_of_dicts_rating(select_query):
  try:
      con = sqlite3.connect('netflix.db')
      con.row_factory = sqlite3.Row
      things = con.execute(select_query).fetchall()
      unpacked = [{'title': item[2],'rating':item[8],'release_year': item[7] } for item in things]

      return unpacked
  except Exception as e:
      print(f"Ошибка выполнения SQL запроса")
      return []
  finally:
      con.close()

def sql_data_to_list_of_dicts_genre(select_query):
  try:
      con = sqlite3.connect('netflix.db')
      con.row_factory = sqlite3.Row
      things = con.execute(select_query).fetchall()
      unpacked = [{'title': item[2],'description':item[-1] } for item in things]

      return unpacked
  except Exception as e:
      print(f"Ошибка выполнения SQL запроса")
      return []
  finally:
      con.close()

"""
Шаг 5 ( выполняются при запуске файла main)
"""
def find_two_actors(actors):
    conn = sqlite3.connect('netflix.db')
    cur = conn.cursor()
    cur.execute(f'''
    select n.cast from netflix n where n.cast like '{actors[0]}% {actors[1]}%'  
;
    ''')
    result = cur.fetchall()
    dict_of_k = {}
    list_of_return_actors = []

    for i in result:
        for k in i[0].split(','):
            if k not in dict_of_k.keys():
                dict_of_k[k] = 0

    for i in result:
        for k in i[0].split(','):
            dict_of_k[k] = dict_of_k[k]+1

    for i in dict_of_k:
        if dict_of_k[i] > 2:
            list_of_return_actors.append(i)


    return list_of_return_actors

print(find_two_actors(( 'Jack Black' , 'Dustin Hoffman')))

"""
Шаг 6 ( выполняются при запуске файла main)
"""
def json_list_of_films(film_or_serial,release_year,genre):
    conn = sqlite3.connect('netflix.db')
    cur = conn.cursor()
    cur.execute(f'''
    select n.title, n.description from netflix n where type = '{film_or_serial}'
    and release_year  = '{release_year}'
    and listed_in = '{genre}'
;
        ''')
    result = cur.fetchall()

    dict_result = {}
    for i in result:
        dict_result[i[0]] = i[1]

    json_dict = json.dumps(dict_result)
    return json_dict


print(json_list_of_films("Movie","2018","Dramas, Independent Movies, International Movies"))