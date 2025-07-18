
import streamlit as st
import streamlit_authenticator as stauth
import requests

# === USER & PASSWORT-SETUP ===
users = {
    "virginia": {"name": "Virginia Dumbrava", "password": "Z7f#9Lp3!xGq"},
    "jana": {"name": "Jana Brüggemann", "password": "M4v@Rt2$kPwZ"},
    "stefanie": {"name": "Stefanie Lasthaus", "password": "X8e&Nd5!rUbL"},
    "marisa": {"name": "Marisa Becker", "password": "Q2y#Ks1@WxYo"},
    "anna": {"name": "Anna Brökelmeier", "password": "J6t$Ks1@WxYo"},
    "denise": {"name": "Denise Kohlhoff", "password": "L9r!Vm4#FpJs"},
}

# Passwörter hashen
hashed_passwords = stauth.Hasher([user["password"] for user in users.values()]).generate()

credentials = {
    "usernames": {
        username: {"name": users[username]["name"], "password": hashed_passwords[i]}
        for i, username in enumerate(users)
    }
}

authenticator = stauth.Authenticate(
    credentials,
    "cookie_name",        # Cookie-Name
    "signature_key",      # Signatur-Schlüssel
    cookie_expiry_days=1
)

# === LOGIN-BEREICH ===
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
