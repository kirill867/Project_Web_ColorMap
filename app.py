from flask import Flask, render_template, request  # глобальный объект приложения импортируем
from PIL import Image, ImageDraw
import random as rng
import time as t

from database import work_with_db
from sql_provider import SQLProvider

COLORS = ["#ff9900", "#9933cc", "#00ee00", "#00e0ff"]

app = Flask(__name__)  # __name__ имя модуля, точка входа

app.config['DB_CONFIG'] = {    # словарь, видно по всему приложению

    'host': "127.0.0.1",
    'port': 3306,
    'user': 'root',
    'password': "7210109",
    'db': 'femdb'

}


app.config['SECRET_KEY'] = 'I am the only one'

provider = SQLProvider("sql/")

width = 768
height = 512
scale = 3


rng.seed(t.time())


def addColors(inElem):  #основаная функция, добавление цвета для раскрашивания
    for elem1 in inElem:
        if "colorID" not in elem1:
            elem1["colorID"] = rng.randint(0, len(COLORS) - 1)
        nodeSet1 = {elem1["n1"], elem1["n2"], elem1["n3"]}
        for elem2 in inElem:
            if elem1 != elem2:
                nodeSet2 = {elem2["n1"], elem2["n2"], elem2["n3"]}
                if len(list(nodeSet1 & nodeSet2)) == 2:
                    if "colorID" not in elem2:
                        elem2["colorID"] = elem1["colorID"] + 1
                    elif elem1["colorID"] == elem2["colorID"]:
                        elem2["colorID"] += 1
                    if elem2["colorID"] >= len(COLORS):
                        elem2["colorID"] -= len(COLORS)


@app.route("/", methods=['GET', 'POST'])  # @ - декоратор, на входящий урл будет срабатывать эта функция, обработчик POST пароль
def main():
    img = Image.new('RGB', (width, height), color='white')   #создание изображения
    sql1 = provider.get('nodes.sql')     #обращ к классу SQLProvider, для получения данных из файла (метод geet в файле sql_provider)
    sql2 = provider.get('elements.sql')

    nodes = work_with_db(app.config['DB_CONFIG'], sql1)      #приложение конфигурац (словарь, видеть во всем прилож) и обращ к базе данных
    elements = work_with_db(app.config['DB_CONFIG'], sql2)    #файл database 

    addColors(elements)

    draw = ImageDraw.Draw(img)
    for element in elements:
        n1 = nodes[element["n1"] - 1]  #координата первой точки (element c 1, nodes с 0)
        n2 = nodes[element["n2"] - 1]
        n3 = nodes[element["n3"] - 1]
        draw.polygon([((n1["x"] * scale + img.width / 2), (img.height / 2 - n1["y"] * scale)),  #вывод с учетом ширины и высоты, домножение мастаба
                        ((n2["x"] * scale + img.width / 2), (img.height / 2 - n2["y"] * scale)),
                        ((n3["x"] * scale + img.width / 2), (img.height / 2 - n3["y"] * scale))], outline="black",
                            fill=COLORS[element["colorID"]])
    img.save('static/finiteElem.png')   #сохранение в файл

    return render_template("main2.html", im="finiteElem.png")    #функция для передачи html страницы


if __name__ == "__main__":
    app.debug = True
    app.run(host="127.0.0.1", port=7000)

