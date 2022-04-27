import requests
from bs4 import BeautifulSoup
import urllib.parse
import networkx as nx


def get_urls(url):
    # Pobranie strony
    reqs = requests.get(url)

    # Parsowanie strony
    soup = BeautifulSoup(reqs.text, 'html.parser')

    urls = []

    # Iteracja po wszystkich linkach na stronie
    for link in soup.find_all('a'):
        # Parsowanie URL
        parsed_url = urllib.parse.urlparse(link.get('href'))
        # Dodaj tylko jeśli jest netloc
        if parsed_url.netloc:
            urls.append(f"{parsed_url.scheme}://{parsed_url.netloc}")
    # Usuń duplikaty
    return list(set(urls))


start = 'https://przymus.org'
links = [[], [], []]
graph = nx.DiGraph()

# pierwsza iteracja - lvl 0 - linki wychodzace ze strony przymus.org
lvl0 = get_urls(start)

# dodawanie linkow z lvl 0
for link in lvl0:
  if(link != start):
    graph.add_edge(start, link)

# druga iteracja - lvl 1 - linki wychodzace ze stron z lvl 0
for link in lvl0:
  links_from_current_link = get_urls(link)
  for l in links_from_current_link:
    if(link != l):
      graph.add_edge(link, l)

nx.draw(graph, node_size=5)