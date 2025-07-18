import streamlit as st
import requests
import pandas as pd
import streamlit_authenticator as stauth

# Deine User-Daten mit gehashten Passwörtern (Beispiel-Hashes!)
users = {
    "virginia": {"name": "Virginia Dumbrava", "password": "$2b$12$..."},
    "jana": {"name": "Jana Brüggemann", "password": "$2b$12$..."},
    "stefanie": {"name": "Stefanie Lasthaus", "password": "$2b$12$..."},
    "marisa": {"name": "Marisa Becker", "password": "$2b$12$..."},
    "anna": {"name": "Anna Brökelmeier", "password": "$2b$12$..."},
    "denise": {"name": "Denise Kohlhoff", "password": "$2b$12$..."},
}

# Liste der Usernamen und deren Passwörter zum Hasher geben (falls du selber hashst)
usernames = list(users.keys())
names = [users[u]["name"] for u in usernames]
passwords = [users[u]["password"] for u in usernames]  # schon gehasht

# Streamlit Authenticator initialisieren
authenticator = stauth.Authenticate(
    names,
    usernames,
    passwords,
    "teilnehmerliste_cookie",

