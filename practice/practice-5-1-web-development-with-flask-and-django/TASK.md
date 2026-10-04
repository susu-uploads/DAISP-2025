---
ru: "Практика 5_1"
en: "Practice 5_1"
code: "practice-5-1-web-development-with-flask-and-django"
origin: "https://edu.susu.ru/mod/assign/view.php?id=8134740"
---



Срок выполнения - 31 декабря

#### Задание 1.

Вам нужно написать REST API (backend) для сайта объявлений.

Должны быть реализованы методы создания/удаления/редактирования объявления.

У объявления должны быть следующие поля:

- заголовок
- описание
- дата создания
- владелец

Результатом работы является API, написанное на Flask.

Этапы выполнения задания:

1. Сделайте роут на Flask.
2. POST метод должен создавать объявление, GET - получать объявление, DELETE - удалять объявление.

#### Задание 2.

Вам дана [заготовка](https://github.com/netology-code/dj-homeworks/tree/drf/1.1-first-project/first_project) с Django
проектом. В проект уже добавлено 1 приложение – `app`.

Вам необходимо реализовать 3 view функции и настроить для них правильные урлы.

- `/` - домашняя страница, содержит список доступных страниц;
- `current_time/` - показывает текущее время в любом удобном вам формате;
- `workdir/` – выводит содержимое [рабочей директории](https://ru.wikipedia.org/wiki/%D0%A0%D0%B0%D0%B1%D0%BE%D1%87%D0%B8%D0%B9_%D0%BA%D0%B0%D1%82%D0%B0%D0%BB%D0%BE%D0%B3).

В первую очередь обратите внимание на
файл [urls.py](https://github.com/netology-code/dj-homeworks/blob/drf/1.1-first-project/first_project/first_project/urls.py).
В нем задаются пути ко view-функциям, которые отвечают по соответствующим запросам.

Приложение `app` уже добавлено в проект и включено в `INSTALLED_APPS` (обязательно убедитесь в этом, проверив файл с
настройками).

`home_view` использует шаблон для генерации контента страницы. Шаблоны мы еще не изучали, это материал дальнейших
лекций. Поэтому ориентируйтесь на подсказки, часть кода уже написано, вам нужно вписать недостающее 🙂.

Вам нужно вписать свой код в следующие файлы:

- [urls.py](https://github.com/netology-code/dj-homeworks/blob/drf/1.1-first-project/first_project/first_project/urls.py)
- [views.py](https://github.com/netology-code/dj-homeworks/blob/drf/1.1-first-project/first_project/app/views.py)
