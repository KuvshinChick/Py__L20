#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import sys
import json
from dotenv import load_dotenv


def add_human(people, name, zodiac_sign, birth):
    # Вернуть словарь
    people.append(
        {
            "name": name,
            "zodiac_sign": zodiac_sign,
            "birth": birth
        }
    )
    return people


def display_people(people_list):
    if people_list:
        # Заголовок таблицы.
        line = (f'{"+" + "-" * 15 + "+" + "-" * 12 + "+"}'
                f'{"-" * 15 + "+"}')
        print(line)
        print(f"|{'Name' :^15}|{'Birth ' :^12}|{'Zodiac_sign ' :^15}|")
        print(line)

        # Вывести данные о всех людях.
        for idx, man in enumerate(people_list):
            print(
                f'|{man.get("name", "") :^15}'
                f'|{man.get("birth", "") :^12}'
                f'|{man.get("zodiac_sign", "") :^15}|'
            )
            print(line)
    else:
        print("Список пуст.")


def select_zz(people_list, zz):
    # Инициализировать счетчик.
    count = 0
    result = []

    # Таблица с людьми
    for p in people_list:
        if zz == p.get('zodiac_sign'):
            count += 1
            result.append(p)

    # Если счетчик равен 0, то люди не найдены.
    if count == 0:
        print("Люди с заданным ЗЗ не найдены")

    return result

def save_people(file_name, people_list):
    """
    Сохранить всех людей в файл JSON.
    """
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установим ensure_ascii=False
        json.dump(people_list, fout, ensure_ascii=False, indent=4)


def load_people(file_name):
    """
    Загрузить всех людей из файла JSON.
    """
    # Открыть файл с заданным именем для чтения.
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


def main(command_line=None):
    # Создать родительский парсер для определения имени файла.
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "-d",
        "--data",
        action="store",
        required=False,
        help="The data file name"
    )

    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser("people")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )
    subparsers = parser.add_subparsers(dest="command")

    # Создать субпарсер для добавления людей.
    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add a new person"
    )
    add.add_argument(
        "-n",
        "--name",
        action="store",
        required=True,
        help="The person's name"
    )
    add.add_argument(
        "-z",
        "--zodiac_sign",
        action="store",
        help="The person's zodiac_sign"
    )
    add.add_argument(
        "-b",
        "--birth",
        action="store",
        required=True,
        help="The person's birth"
    )

    # Создать субпарсер для отображения всех людей.
    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Display all people"
    )

    # Создать субпарсер для выбора знака зодиака.
    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Select person"
    )

    select.add_argument(
        "-S",
        "--zodiac_sign",
        action="store",
        required=True,
        help="The required zodiac_sign"
    )

    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    # Выполнить разбор аргументов командной строки.
    args = parser.parse_args(command_line)
    # Получить имя файла.
    data_file = args.data
    if not data_file:
        data_file = os.environ.get("ind2_DATA")
    if not data_file:
        print("The data file name is absent", file=sys.stderr)
        sys.exit(1)

    # Загрузить всех людей из файла, если файл существует.
    is_dirty = False
    if os.path.exists(data_file):
        people = load_people(data_file)
    else:
        people = []
    # Добавить работника.
    if args.command == "add":
        people = add_human(
            people,
            args.name,
            args.zodiac_sign,
            args.birth
        )
        is_dirty = True

    # Отобразить всех людей.
    elif args.command == "display":
        display_people(people)

    # Выбрать требуемых людей.
    elif args.command == "select":
        selected = select_zz(people, args.zodiac_sign)
        display_people(selected)
    # Сохранить данные в файл, если список работников был изменен.
    if is_dirty:
        save_people(data_file, people)
        os.environ.setdefault('WORKERS_DATA', data_file)


if __name__ == '__main__':
    main()
