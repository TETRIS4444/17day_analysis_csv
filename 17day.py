import csv

def load_csv(filename):
    with open(filename, newline='', encoding="utf-8") as file:
        loading = csv.DictReader(file)
        return list(loading)


def valid_id(value):
    try:
        i = int(value)
    except(ValueError, TypeError):
        return None
    else:
        if i < 0:
            return None
        return i

def valid_price(value):
    try:
        p = float(value)
    except(ValueError, TypeError):
            return None
    else:
        if p <= 0:
            return None
        return p

def valid_quantity(value):
    try:
        q = int(value)
    except(ValueError, TypeError):
            return None
    else:
        if q <= 0:
            return None
        return q

def empty_check(product, category):
    return not product or not category

    
def clean_order(order):
    id = valid_id(order["id"])
    date = order["date"]
    product = order["product"]
    category = order["category"]
    price = valid_price(order["price"])
    quantity = valid_quantity(order["quantity"])
    status = order["status"]
    city = order["city"]

    if None in (id, price, quantity):
        return None

    if empty_check(product, category):
        return None

    if status != "completed":
        return None

    if city == "":
        city = "unknown"

    return {
        "id": id,
        "date": date,
        "product": product,
        "category": category,
        "price": price,
        "quantity": quantity,
        "status": status,
        "city": city
    }

def clean_orders(raw_orders):
    return [clean_order(order) for order in raw_orders if clean_order(order) is not None]



raw_orders = load_csv("sales.csv")
orders = clean_orders(raw_orders)

def quan_source(raw_orders):
    return len(raw_orders)

def quan_valid(orders):
    return len(orders)

def quan_invalid(raw_orders, orders):
    return quan_source(raw_orders) - quan_valid(orders)

def calc_revenue(valid_order):
    return valid_order["price"] * valid_order["quantity"]

def total_revenue(orders):
    return sum(calc_revenue(order) for order in orders)

def total_quantity(orders):
    return sum(order["quantity"] for order in orders)

def avarage_revenue(orders):
    return total_revenue(orders) / total_quantity(orders)


def calc_revenue_by_product(orders):
    revenue_by_product = {}
    for order in orders:
        product = order["product"]
        revenue_by_product[product] = revenue_by_product.get(product, 0) + calc_revenue(order)
    return revenue_by_product


def calc_revenue_by_category(orders):
    revenue_by_category = {}
    for order in orders:
        category = order["category"]
        revenue_by_category[category] = revenue_by_category.get(category, 0) + calc_revenue(order)
    return revenue_by_category


def calc_revenue_by_city(orders):
    revenue_by_city = {}
    for order in orders:
        city = order["city"]
        revenue_by_city[city] = revenue_by_city.get(city, 0) + calc_revenue(order)
    return revenue_by_city

def show_revenue_by_product(orders):
    revenue_by = calc_revenue_by_product(orders)
    print(f"№1 {max(revenue_by, key=revenue_by.get)}")
    for key, value in revenue_by.items():
        print(f'{key}: {value}')

def show_revenue_by_category(orders):
    revenue_by = calc_revenue_by_category(orders)
    print(f"№1 {max(revenue_by, key=revenue_by.get)}")
    for key, value in revenue_by.items():
        print(f'{key}: {value}')

def show_revenue_by_city(orders):
    revenue_by = calc_revenue_by_city(orders)
    print(f"№1 {max(revenue_by, key=revenue_by.get)}")
    for key, value in revenue_by.items():
        print(f'{key}: {value}')

def expensive_sale(orders):
    sales = []
    for order in orders:
        id = order["id"]
        product = order["product"]
        revenue = calc_revenue(order)
        if revenue > 5000:
            sales.append({"id": id, "product": product, "revenue": revenue})
    return sales


def calc_ranking_by_product(orders):
    ranks = calc_revenue_by_product(orders)
    return sorted(ranks, key=ranks.get, reverse=True)


    
def build_report(raw_orders, orders):
    lines = []
    lines.append("SALES REPORT")
    lines.append("")
    lines.append(f"Raw sales: {quan_source(raw_orders)}")
    lines.append(f"Valid sales: {quan_valid(orders)}")
    lines.append(f"Invalid sales: {quan_invalid(raw_orders, orders)}")
    lines.append("")
    lines.append(f"Total revenue: {total_revenue(orders)}")
    lines.append(f"Total units: {total_quantity(orders)}")
    lines.append(f"Average revenue: {avarage_revenue(orders)}")
    lines.append("")

    revenue_by_product = calc_revenue_by_product(orders)
    top_product = max(revenue_by_product, key=revenue_by_product.get)
    lines.append("PRODUCTS")
    lines.append(f"№1: {top_product}")
    for product, revenue in revenue_by_product.items():
        lines.append(f"{product}: {revenue:}")
    lines.append("")

    revenue_by_category = calc_revenue_by_category(orders)
    top_category = max(revenue_by_category, key=revenue_by_category.get)
    lines.append("CATEGORIES")
    lines.append(f"№1: {top_category}")
    for category, revenue in revenue_by_category.items():
        lines.append(f"{category}: {revenue}")
    lines.append("")

    lines.append("CITIES")
    for city, revenue in calc_revenue_by_city(orders).items():
        lines.append(f"{city}: {revenue}")
    lines.append("")

    lines.append("EXPENSIVE SALES")
    for sale in expensive_sale(orders):
        lines.append(f'{sale["id"]} | {sale["product"]} | {sale["revenue"]}')
    lines.append("")

    lines.append("PRODUCT RANKING")
    for i, product in enumerate(calc_ranking_by_product(orders), start=1):
        lines.append(f"{i}. {product}")

    return "\n".join(lines)

def save_report(raw_orders, orders, filename="sales_report.txt"):
    report = build_report(raw_orders, orders)
    with open(filename, "w", encoding="utf-8") as file:
        file.write(report)


save_report(raw_orders, orders)


# только в выводе так есть quan_source(raw_orders) quan_invali(raw_orders, orders)
# все кроме quan_source(raw_orders) quan_invali(raw_orders, orders) lean_orders(raw_orders)
# да
# нет
# сделал бы более утонченный build report