"""
Parses the matchups page of all champions on League of Graphs to get the win-rates for each matchup.
Works on 1.8.2023 but may be useless after slight changes in League of Graphs.
"""
import pickle

from bs4 import BeautifulSoup
import requests

from champs import top_champs


def extract_matchup(soup):
    champion_name_element = soup.find('span', class_='name')
    winrate_element = soup.find('progressbar')

    # Extract the text content of the elements
    if champion_name_element and winrate_element:
        champion_name = champion_name_element.get_text()
        winrate = winrate_element['data-value']

    return champion_name, winrate


def get_matchup_html(soup, champ):
    # Winning matchups
    matchups_html = []
    table_title_1 = f"{champ} gewinnt vermehrt gegen"
    table_1 = soup.find('h3', string=table_title_1)
    if table_1:
        table_1_parent = table_1.find_next_sibling('table')
        td_elements_1 = table_1_parent.find_all('tr')
        for td in td_elements_1:
            matchups_html.append(td)
    else:
        print(f"Failed to get winning infos for {champ}")

    # Losing matchups
    table_title_2 = f"{champ} verliert vermehrt gegen"
    table_2 = soup.find('h3', string=table_title_2)
    if table_2:
        table_2_parent = table_2.find_next_sibling('table')
        td_elements_2 = table_2_parent.find_all('tr')
        for td in td_elements_2:
            matchups_html.append(td)
    else:
        print(f"Failed to get losing infos for {champ}")

    return matchups_html


def fetch_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup  # Return the prettified HTML content
        else:
            print(f"Failed to fetch the HTML. Status code: {response.status_code} - {response.reason}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the HTML: {e}")

    return None


def download_all_matchups():
    base_url = "https://www.leagueofgraphs.com/de/champions/counters/"
    all_champ_urls = [base_url + c.lower().replace(". ", "").replace("\'", "").replace("wukong", "monkeyking") for c in
                      top_champs]
    full_result = {}
    for i, url in enumerate(all_champ_urls):
        print(f"=={top_champs[i]}==")
        html = fetch_html(url)
        if not html:
            print("Failed to fetch the HTML.")
            break

        matchup_html_elements = get_matchup_html(html, top_champs[i])
        full_result[top_champs[i]] = {}

        for matchup_html in matchup_html_elements:
            try:
                champion_name, winrate_percentage = extract_matchup(matchup_html)
                print(f"Champion Name: {champion_name}")
                print(f"Winrate: {winrate_percentage}")
                full_result[top_champs[i]][champion_name] = winrate_percentage
            except:
                print(f"Skiping extracting matchup for {top_champs[i]}")
    # Save the dictionary to a file
    with open('full_result.pickle', 'wb') as f:
        pickle.dump(full_result, f)


download_all_matchups()
