import requests
from bs4 import BeautifulSoup
import sys
import os
import time
import urllib.parse

# === Couleurs Matrix ===
R = "\033[1;31m"
G = "\033[1;32m"
Y = "\033[1;33m"
B = "\033[1;34m"
C = "\033[1;36m"
RESET = "\033[0m"

# === Bannière ===
def banner():
    os.system("clear")
    print(f"""{G}
 ██████╗  ██████╗ ███████╗██╗███╗   ██╗███████╗███████╗
██╔═══██╗██╔════╝ ██╔════╝██║████╗  ██║██╔════╝██╔════╝
██║   ██║██║  ███╗█████╗  ██║██╔██╗ ██║███████╗█████╗  
██║   ██║██║   ██║██╔══╝  ██║██║╚██╗██║╚════██║██╔══╝  
╚██████╔╝╚██████╔╝███████╗██║██║ ╚████║███████║███████╗
 ╚═════╝  ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝
{Y}       OSINT Real Info Finder | By WHITE 404 GHz{RESET}
""")

# === Recherche DuckDuckGo avec parsing corrigé ===
def search_duckduckgo(query, max_results=20):
    headers = {"User-Agent": "Mozilla/5.0"}
    params = {"q": query, "kl": "fr-fr"}  # recherche FR
    url = "https://html.duckduckgo.com/html/"
    r = requests.post(url, headers=headers, data=params)
    soup = BeautifulSoup(r.text, "html.parser")

    results = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        if href.startswith("http") and "duckduckgo.com" not in href:
            results.append(href)
            if len(results) >= max_results:
                break
    return results

# === Recherche illimitée ===
def infinite_search(name):
    all_results = set()
    page = 1
    while True:
        print(f"{Y}[PAGE {page}] Recherche en cours...{RESET}")
        results = search_duckduckgo(name, max_results=10)
        if not results:
            print(f"{R}[!] Aucun résultat trouvé à cette page.{RESET}")
            break
        for url in results:
            if url not in all_results:
                print(f"{G}[+] {url}{RESET}")
                all_results.add(url)
        page += 1
        time.sleep(2)
        cont = input(f"{B}Continuer la recherche ? (o/n) : {RESET}").lower()
        if cont != "o":
            break

    # Sauvegarde
    if all_results:
        filename = f"{name}_osint_results.txt"
        with open(filename, "w") as f:
            for url in all_results:
                f.write(url + "\n")
        print(f"{G}[✔] Résultats sauvegardés dans {filename}{RESET}")

# === Main ===
try:
    banner()
    target = input(f"{B}Entrez le nom ou pseudo : {RESET}").strip()
    if target:
        infinite_search(target)
    else:
        print(f"{R}[ERREUR] Vous devez entrer un nom/pseudo !{RESET}")
except KeyboardInterrupt:
    print(f"\n{Y}[INFO] Recherche arrêtée. À bientôt, camarade hacker.{RESET}")
    sys.exit()
