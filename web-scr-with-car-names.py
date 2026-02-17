import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse


def set_page(url, page_number):
    parsed = urlparse(url)
    query_params = parse_qs(parsed.query)

    query_params['page'] = [str(page_number)]

    new_query = urlencode(query_params, doseq=True)
    new_url = urlunparse(parsed._replace(query=new_query))

    return new_url


def urlt(turbo): 
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    response = requests.get(turbo, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    prices = soup.find_all('div', class_='products-i__price products-i__bottom-text')
    years = soup.find_all('div', class_='products-i__attributes products-i__bottom-text')
    car_names = soup.find_all('div', class_='products-i__name products-i__bottom-text')

    total_price = 0
    count = 0

    for price in prices:
        text = price.get_text().strip()
        if '₼' in text:
            try:
                clean_price = text.replace(' ', '').replace('₼', '')
                total_price += int(clean_price)
                count += 1
            except:
                pass

    total_year = 0
    year_count = 0
    for year in years:
        text = year.get_text().strip()
        if text[:4].isdigit():
            total_year += int(text[:4])
            year_count += 1

    carnames = []
    for car in car_names:
        name = car.get_text().strip()
        if name not in carnames:
            carnames.append(name)

    return total_price, count, total_year, year_count, carnames


# ---------------- MAIN ---------------- #

turbo = input('Unvani daxil et: ')
max_page = int(input('Neçə səhifə yoxlansın: '))

grand_total_price = 0
grand_count = 0
grand_total_year = 0
grand_year_count = 0
all_names = []

for page in range(1, max_page + 1):
    new_url = set_page(turbo, page)
    print(f"Yoxlanır: {new_url}")

    result = urlt(new_url)

    grand_total_price += result[0]
    grand_count += result[1]
    grand_total_year += result[2]
    grand_year_count += result[3]
    all_names += result[4]


average_price = grand_total_price / grand_count if grand_count != 0 else 0
average_year = grand_total_year / grand_year_count if grand_year_count != 0 else 0

unique_names = sorted(list(set(all_names)))

print("\n===== NƏTİCƏ =====")
print(f'Orta qiymet: {int(average_price)} AZN')
print(f'Orta buraxilis ili: {int(average_year)}')
print(f'Umumi elan sayi: {grand_count}\n')

for i, name in enumerate(unique_names, 1):
    print(f'{i}) {name}')
