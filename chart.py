# Генератор графиков

import io
import seaborn

mock = {
    "historicalDates": [
        "2023-04-25",
        "2023-04-26",
        "2023-04-27",
        "2023-04-28",
        "2023-04-29",
        "2023-04-30",
    ],
    "historicalValues": [17, 17, 10, 17, 18.7, 17.5],
    "currentValue": 17.5,
}

def generate(data: dict) -> bytes:
    # Превращаем даты в данных из 2023-04-25 в 25.04.2023
    data["historicalDates"] = [
        date.split("-")[2] + "." + date.split("-")[1]
        for date in data["historicalDates"]
    ]
    # Генерируем график за последние 7 дней
    data["historicalDates"] = data["historicalDates"][-7:]
    data["historicalValues"] = data["historicalValues"][-7:]
    seaborn.set_theme(style="darkgrid")
    c = seaborn.lineplot(
        data=data,
        x="historicalDates",
        y="historicalValues",
    )
    # Настраиваем график
    c.set_title("График флора КриптоСпотти на Rarible", fontsize=16)
    c.set_xlabel("")
    c.set_ylabel("Цена в MATIC")
    # Делаем график более широким
    c.figure.set_figwidth(8)
    # Сохраняем график в буфер
    buf = io.BytesIO()
    c.figure.savefig(buf, format="png")
    # Возвращаем буфер
    buf.seek(0)
    return buf.read()
