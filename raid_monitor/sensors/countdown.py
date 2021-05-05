from datetime import date

last_day = date(2021, 6, 27)


def when():
    today = date.today()

    counter = last_day - today

    weekys = counter.days // 7
    days = counter.days % 7

    if weekys >= 0:
        return f'{weekys}.{days}'
    else:
        return ''


if __name__ == '__main__':
    print(when())
