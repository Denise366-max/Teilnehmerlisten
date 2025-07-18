import streamlit as st
import streamlit_authenticator as stauth
import requests
import pandas as pd

# 1. User-Daten mit Klartext-Passwörtern
users = {
    "virginia": {"name": "Virginia Dumbrava", "password": "DeinPasswort1!"},
    "jana": {"name": "Jana Brüggemann", "password": "DeinPasswort2!"},
    "stefanie": {"name": "Stefanie Lasthaus", "password": "DeinPasswort3!"},
    "marisa": {"name": "Marisa Becker", "password": "DeinPasswort4!"},
    "anna": {"name": "Anna Brökelmeier", "password": "DeinPasswort5!"},
    "denise": {"name": "Denise Kohlhoff", "password": "DeinPasswort6!"},
}

usernames = list(users.keys())
names = [users[u]["name"] for u in usernames]
clear_passwords = [users[u]["password"] for u in usernames]

# 2. Hash die Klartext-Passwörter
hashed_passwords = stauth.Hasher(clear_passwords).generate()

# 3. Authenticator mit Schlüsselwortargumenten aufrufen!
authenticator = stauth.Authenticate(
    names=names,
    usernames=usernames,
    passwords=hashed_passwords,
    cookie_name="teilnehmerliste_cookie",
    key="random_signature_key_123",
    cookie_expiry_days=1
)

# 4. Login UI
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    st.sidebar.title(f"Willkommen {name}!")
    authenticator.logout("Logout", "sidebar")

    st.title("Pipedrive Deal Teilnehmerliste")

    API_TOKEN = st.text_input("API Token eingeben", type="password")
    BASE_URL = "https://api.pipedrive.com/v1"
    deal_id = st.text_input("Deal-ID eingeben")

    if st.button("Teilnehmer laden") and API_TOKEN and deal_id:
        url = f"{BASE_URL}/deals/{deal_id}/participants?api_token={API_TOKEN}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json().get("data", [])
            teilnehmer_liste = []
            for i, p in enumerate(data, start=1):
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
else:
    st.info("Bitte logge dich ein")


