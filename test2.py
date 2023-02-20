# importer la librairie pour faire du scraping : BeautifulSoup
import requests
from bs4 import BeautifulSoup
import csv


def scrape_page(soup, quotes):
    # récupérer tous les éléments HTML quote <div> sur la page
    expand = soup.find_all('div', class_='info')

    # itérer sur la liste des éléments
    # pour extraire les données d'intérêt et les stocker
    for expand in expand:
        # extraire le nom, le tag, l'adresse et le téléphone et les avis de chaque restaurant à NY
        nom = expand.find('a', class_='business-name').text
        cat = expand.find('div', class_='categories').text
        tel = expand.find('div', class_='phones phone primary')
        com = expand.find('p', class_='body with-avatar')
        if com is not None:
            avis = com.text
        if tel is not None:
            a = tel.text
        adre = expand.find('div', class_='adr')
        if adre is not None:
            b = adre.text
        # link = expand.find('div', class_='links')
        # if link is not None:
        #     c = link.text

        # ajouter un dictionnaire contenant les données
        # dans un nouveau format dans la liste
        quotes.append(
            {
                'business-name': nom,
                'categories': cat,
                'phones phone primary': a,
                'adr': b,
                'body with-avatar': avis
                # 'links': c
            }
        )


# l'url de la page d'accueil du site cible
base_url = 'https://www.yellowpages.com/new-york-ny/restaurants'

# définir l'en-tête User-Agent à utiliser dans la requête GET ci-dessous
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

# récupération de la page Web cible
page = requests.get(base_url, headers=headers)

# analyser la page Web cible avec Beautiful Soup
soup = BeautifulSoup(page.text, 'html.parser')

# initialisation de la variable qui contiendra
# la liste de toutes les données
quotes = []

# Scraping sur la page d'accueil
scrape_page(soup, quotes)

# lire le fichier "RestaurantNY.csv" et le créer
csv_file = open('ListeRestaurantsNY.csv', 'w', encoding='utf-8', newline='')

# initialisation de l'objet writer pour insérer des données
# Dans le fichier CSV
writer = csv.writer(csv_file)

# écrire l'en-tête du fichier CSV
writer.writerow(['Nom du Restaurant:', 'Tags:', 'Numéro de téléphone:', 'Adresse:', 'Avis:'])

# écrire chaque ligne du CSV
for quote in quotes:
    writer.writerow(quote.values())

# mettre fin à l'opération et libérer les ressources
csv_file.close()
