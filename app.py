import streamlit as st
import requests
import pandas as pd
import streamlit_authenticator as stauth

users = {
    "virginia": {"name": "Virginia Dumbrava", "password": "$2b$12$..."},
    "jana": {"name": "Jana Brüggemann", "password": "$2b$12$..."},
    "stefanie": {"name": "Stefanie Lasthaus", "password": "$2b$12$..."},
    "marisa": {"name": "Marisa Becker", "password": "$2b$12$..."},
    "anna": {"name": "Anna Brökelmeier", "password": "$2b$12$..."},
    "denise": {"name": "Denise Kohlhoff", "password": "$2b$12$..."},
}

usernames = list(users.keys())
names = [users[u]["name"] for u in usernames]
passwords = [users[u]["password"] for u in usernames]

authenticator = stauth.Authenticate(
    names,
    usernames,
    passwords,
    "teilnehmerliste_cookie",
    "some_random_signature_key",
    cookie_expiry_days=1
)

name, authentication_status, username = authenticator.login("Login", location="main")

if authentication_status:
    st.sidebar.title(f"Willkommen {name}!")
    authenticator.logout("Logout", location="sidebar")

    st.title("Pipedrive Deal Teilnehmerliste")

    API_TOKEN = st.text_input("API Token eingeben", type="password")
    BASE_URL = "https://api.pipedrive.com/v1"

    deal_id = st.text_input("Deal-ID eingeben")

    if st.button("Teilnehmer laden") and API_TOKEN and deal_id:
        url = f"{BASE_URL}/deals/{deal_id}?api_token={API_TOKEN}"
        response = requests.get(url)
        if response.status_code == 200:
            deal_data = response.json().get("data", {})
            participants = deal_data.get("participants", [])

            if not participants:
                st.warning("Keine Teilnehmer direkt im Deal gefunden.")
            else:
                teilnehmer_liste = []
                for i, p in enumerate(participants, start=1):
                    person = p.get("person", {})
                    org = p.get("org", {})
                    teilnehmer_liste.append({
                        "Teilnehmer": f"Teilnehmer {i}",
                        "Name": person.get("name", ""),
                        "E-Mail": person.get("email", [{}])[0].get("value", "") if person.get("email") else "",
                        "Organisation": org.get("name", "") if org else ""
                    })

                df = pd.DataFrame(teilnehmer_liste)
                st.dataframe(df)
        else:
            st.error(f"Fehler beim Laden der Daten: {response.status_code}")

elif authentication_status is False:
    st.error("Benutzername oder Passwort ist falsch")
elif authentication_status is None:
    st.info("Bitte logge dich ein")

