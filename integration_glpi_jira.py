import requests
import re

# Configuration des API et authentifications
#glpi_url = "https://votre_instance_glpi.com/apirest.php"
jira_url = "https://alidrissiakram.atlassian.net/rest/api/3/issue"
jira_token = "ATATT3xFfGF0wJLOkLgRwp_EGWLbO6Fa1VLXRFwgX3qze7PMBd5-jSeX3L4SMlTPlmR8E9cb1rzOdpBhqwjQCDYHG1KqYM-dZlRBvcVkSTRGS4sTF5i_jrSRy8tKvC2eLcaGJNCbLwdbZFD7E7ecsGbjZU9Qq81xmjpbuq8UYI1Zv221K2l6XPE=BBAF9903"
jira_auth = ("alidrissi.akram@gmail.com", jira_token)


# Récupérer les tickets GLPI clôturés
response_glpi = requests.get(f"https://caktech.with23.glpi-network.cloud/apirest.php/Ticket?status=solved&app_token=baSoqyq4ukGqhMYjCgOlPa0RPxAH6voQ9yMsYPa9&session_token=bg3ovcfpl9or1o6dreg62iparr")
closed_tickets = response_glpi.json()


# check appel GLPI
#print(f"valeur glpi: {closed_tickets}")



for ticket in closed_tickets:
    # Création du ticket dans Jira
    # Structure de la description au format Atlassian Document Format (ADF)
    description_adf = {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": re.sub(r'&#60;p&#62;|&#60;/p&#62;', '', ticket["content"])
                    }
                ]
            }
        ]
    }
    payload_jira = {
        "fields": {
            "project": {"key": "PFS"},
            "summary": ticket["name"],
            "description": description_adf,
            "issuetype": {"name": "Task"}  # Assurez-vous d'utiliser le bon type de tâche
        }
    }
    response_jira = requests.post(jira_url, json=payload_jira, auth=jira_auth)
    
    if response_jira.status_code == 201:
        print(f"Ticket créé dans JIRA")
    else:
        print(f"Erreur lors de la création du ticket Jira : {response_jira.text}")
