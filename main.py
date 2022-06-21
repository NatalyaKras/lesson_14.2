from flask import Flask, render_template, request, redirect
import db

app = Flask(__name__, template_folder="pages")


#step_1
@app.route('/check_info', methods =['POST','GET'])
def check_info():
    """
    Шаг 1 - поиск по названию. Реализован на странице, отправка названия через форму.
    :return: страницу с формой для отправки и получением результата запроса SQL
    """

    title = ''
    result =''
    if request.method == 'POST':
        title = request.form.get('title')
        result = db.sql_data_to_dict(f'''
select * from netflix where title = '{title}';
''')
    template_context = dict(title=title,result = result)
    return render_template('check_info.html',**template_context)

@app.route('/check_info/<title>', methods =['POST','GET'])
def find_by_title(title):
    """
    Шаг 1 - поиск по названию. Но через <title>
    :return: страницу результата запроса SQL
    """
    result = db.sql_data_to_dict(f'''
select * from netflix where title = '{title}';
''')
    template_context = dict(title=title,result = result)
    return render_template('check_info.html',**template_context)


@app.route('/movie/year/to/year', methods =['POST','GET'])
def find_by_date():
    """
    Шаг 2 - поиск по дате.
    :return: страницу формы отправки данных и результата запроса SQL
    """
    title = ''
    result =''
    date_from = ''
    date_to = ''
    if request.method == 'POST':
        title = request.form.get('title')
        date_from = request.form.get('date_from')
        date_to = request.form.get('date_to')
        result = db.sql_data_to_list_of_dicts(f'''
select * from netflix where  release_year > '{date_from}'
 and release_year < '{date_to}';
''')
    template_context = dict(title=title,result = result)
    return render_template('check_info_by_date.html',**template_context)


"""
Следующие три функции это Шаг 3
"""
@app.route('/rating/children')
def find_by_children_rate():
    result = db.sql_data_to_list_of_dicts_rating(f'''
    select * from netflix where rating = 'R' ;
    ''')
    return str(result)

@app.route('/rating/family')
def find_by_famile_rate():
    result = db.sql_data_to_list_of_dicts_rating(f'''
    select * from netflix where rating = 'G' or  rating = 'PG' or  rating = 'PG-13' ;
    ''')
    return str(result)

@app.route('/rating/adult')
def find_by_adult_rate():
    result = db.sql_data_to_list_of_dicts_rating(f'''
    select * from netflix where rating = 'R' or  rating = 'NC-17' ;
    ''')
    return str(result)

"""
Шаг 4
Поиск по жанру
"""

@app.route('/genre/<genre>')
def find_new_films_by_genre(genre):
    result = db.sql_data_to_list_of_dicts_genre(f'''
    select * from netflix where listed_in like '{genre}%'
     ORDER BY release_year DESC  LIMIT 5;
    ''')

    return str(result)

"""
Шаг 5 и Шаг 6 расписаны в файле db.py и выполняются при запуске файла main
"""

if __name__ == "__main__":
    app.secret_key = 'key'
    app.run()