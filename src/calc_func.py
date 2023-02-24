from datetime import datetime
from dateutil.relativedelta import relativedelta


def check_dict(data: dict) -> list:
    keys = data.keys()

    if len(keys) == 0:
        return ["No data"]

    errors = []

    for key in ("date", "periods", "amount", "rate"):
        if key not in keys:
            errors.append(key)

    return errors


def get_data(data: dict) -> tuple:
    date = data["date"]
    periods = data["periods"]
    amount = data["amount"]
    rate = data["rate"]
    return date, periods, amount, rate


def check_data(date: str, periods: int, amount: int, rate: float) -> tuple:
    errors = []

    try:
        date = datetime.strptime(date, "%d.%m.%Y").date()
    except Exception:
        errors.append("\"Date\" must has format: dd.mm.yyyy")

    try:
        periods = int(periods)
    except ValueError:
        errors.append("\"Periods\" must has type Integer and must be between 1 and 60")
    if type(periods) is int:
        if periods < 1 or periods > 60:
            errors.append("\"Periods\" must be between 1 and 60")

    try:
        amount = int(amount)
    except ValueError:
        errors.append("\"Amount\" must has type Integer and must be between 10 000 and 3 000 000")
    if type(amount) is int:
        if amount < 10000 or amount > 3000000:
            errors.append("\"Amount\" must be between 10 000 and 3 000 000")

    try:
        rate = float(rate)
    except ValueError:
        errors.append("\"Rate\" must has type Float and must be between 1 and 8")
    if type(rate) is float:
        if rate < 1 or rate > 8:
            errors.append("\"Rate\" must be between 1 and 8")

    return date, periods, amount, rate, errors


def calculate_deposit(date: str, periods: int, amount: int, rate: float) -> dict:
    amount = calc_amount(amount, rate)
    response = {date.strftime("%d.%m.%Y"): amount}

    for period in range(1, periods):
        date = date + relativedelta(months=+1, day=31)
        amount = calc_amount(amount, rate)
        response[date.strftime("%d.%m.%Y")] = amount

    return response


def calc_amount(amount: int, rate: float):
    amount = round(amount * (1 + rate / 12 / 100), 2)

    if amount % 2 > 0:
        return amount
    else:
        return int(amount)
