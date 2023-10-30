import os
from string import Template


class SQLProvider:

    def __init__(self, file_path: str) -> None:    #
        self._scripts = {}  # = > _scripts = {'book_by_genre': "select * from book ...  #поле scripts

        for file in os.listdir(file_path):
            self._scripts[file] = Template(open(f'{file_path}/{file}', 'r').read())  #в поле scripts записать то, что находится в файле

    # => get('book_by_genre.sql', genre =, author=)

    def get(self, name, **kwargs):      #get запрос, получение данных из scripta
        return self._scripts[name].substitute(**kwargs)