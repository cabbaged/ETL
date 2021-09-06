from utils import coroutine


def make_base(row):
    """
    Формирует "основу" словаря film_work
    """
    base = dict(row)
    person_keys = ['id', 'first_name', 'second_name']
    for key in person_keys:
        base.pop(key)
    base['persons'] = []
    base['created'] = base['created'].isoformat()
    base['modified'] = base['modified'].isoformat()
    return base


def make_person(row):
    """
    Формирует из записи бд
    словарь с данными person
    """
    person = {}
    person_keys = ['id', 'first_name', 'second_name']
    for key in person_keys:
        person[key] = row[key]
    return person


@coroutine
def transformer(receiver):
    """
    Получает на вход сгрупированные данные
    по одному конкретному film_work,
    компонует их в словарь, отправляет
    следующему компоненту системы.
    """
    while fw_data := (yield):
        base = make_base(fw_data[0])
        for row in fw_data:
            base['persons'].append(make_person(row))
        receiver.send(base)
