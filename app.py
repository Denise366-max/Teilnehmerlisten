import streamlit as st
import streamlit_authenticator as stauth
import requests

# --- Ersetze das hier durch deine mit stauth.hasher erzeugten Hashes ---
hashed_passwords = [
    "$2b$12$K1htA50bpDd5FJH6kXa/yO.YwRjTMTx1IkcQpIcm54oHGlj9keuIy",  # Beispiel-Hash für Passwort 1
    "$2b$12$Dui3P7DX6lP1AqVHXoZoyODP8tUzMZPm/MLD22QvtnnUaUpjJQf8W",
    "$2b$12$3zF6xvZk3bcFnybczGHX9Oh9b9i/x2RX8Xra6gJRGKkRFOVGLvlSe",
    "$2b$12$Ld3qmuEy51a9BjGpVjv8Hu2shMEbyVZ2tOn5gZzItD.NyPl4uBJc6",
    "$2b$12$OWxOVX9Oh.7PqK5e9FV9J.NdjzGTtNyFyMz9ETuZt3IxyjF0dN6vW",
    "$2b$12$0c0Hsv0T4fIcKcWIKoMWTudmPmf7iY1lH9lfKxlzK6s07pD1xH0Su",
]

users = {
    "virginia": {"name": "Virginia Dumbrava", "password": hashed_passwords[0]},
    "jana": {"name": "Jana Brüggemann", "password": hashed_passwords[1]},
    "stefanie": {"name": "Stefanie Lasthaus", "password": hashed_passwords[2]},
    "marisa": {"name": "Marisa Becker", "password": hashed_passwords[3]},
    "anna": {"name": "Anna Brökelmeier", "password": hashed_passwords[4]},
    "denise": {"name": "Denise Kohlhoff", "password": hashed_passwords[5]},
}

credentials = {
    "usernames": {
        username: {"name": users[username]["name"], "password": users[username]["password"]}
        for username in users
    }
}

authenticator = stauth.Authenticate(
    credentials,
    "cookie_name",
    "signature_key",
    cookie_expiry_days=1
)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    st.sidebar.write(f"Hallo, {name}!")
    authenticator.logout("Logout", "sidebar")

    st.title("Teilnehmerliste mit Passwortschutz")

    API_TOKEN = st.text_input("API Token", type="password")
    DEAL_ID = st.text_input("Deal ID")

    if API_TOKEN and DEAL_ID:
        BASE_URL = "https://api.pipedrive.com/v1"
        deal_url = f"{BASE_URL}/deals/{DEAL_ID}?api_token={API_TOKEN}"
        r = requests.get(deal_url)

        if r.status_code == 200:
            deal = r.json().get("data", {})
            st.write(f"Deal: **{deal.get('title', 'Unbekannt')}**")

            participants_url = f"{BASE_URL}/deals/{DEAL_ID}/participants?api_token={API_TOKEN}"
            p_resp = requests.get(participants_url)

            if p_resp.status_code == 200:
                participants = p_resp.json().get("data", [])
                if participants:
                    st.write("Teilnehmer:")
                    for i, p in enumerate(participants, start=1):
                        person = p.get("person", {})
                        name_p = person.get("name", "Unbekannt")
                        emails = person.get("email", [])
                        email = emails[0]["value"] if emails else ""
                        org = person.get("org_name", "")
                        st.write(f"Teilnehmer {i}: {name_p} | {email} | {org}")
                else:
                    st.info("Keine Teilnehmer gefunden.")
            else:
                st.error("Teilnehmer konnten nicht geladen werden.")
        else:
            st.error("Deal konnte nicht geladen werden.")

elif authentication_status == False:
    st.error("Benutzername oder Passwort falsch")
else:
    st.warning("Bitte melde dich an")

