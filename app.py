import streamlit as st
import requests
import pandas as pd

# Deine Pipedrive API-Konfiguration
API_TOKEN = "dfaec32a80975c26802ef8fcf68bf4cc72990046"
BASE_URL = "https://api.pipedrive.com/v1"

def get_deal_participants(deal_id):
    url = f"{BASE_URL}/deals/{deal_id}/participants?api_token={API_TOKEN}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        st.error(f"Fehler beim Laden der Teilnehmer: {response.status_code}")
        return []

st.title("Teilnehmerliste aus Pipedrive Deal")

deal_id = st.text_input("Bitte Deal-ID eingeben:")

if deal_id:
    with st.spinner("Teilnehmer werden geladen..."):
        participants = get_deal_participants(deal_id)

    if participants:
        rows = []
        for idx, participant in enumerate(participants, start=1):
            person = participant.get("person", {})
            name = person.get("name", "")

            email = ""
            emails = person.get("email", [])
            if emails:
                email = next((e.get("value") for e in emails if e.get("value")), "")

            organisation = ""
            org_id = person.get("org_id")
            if org_id and isinstance(org_id, dict):
                organisation = org_id.get("name", "")

            rows.append({
                "Teilnehmer": f"Teilnehmer {idx}",
                "Name": name,
                "E-Mail": email,
                "Organisation": organisation
            })

        df = pd.DataFrame(rows)
        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="CSV herunterladen",
            data=csv,
            file_name=f"deal_{deal_id}_teilnehmer.csv",
            mime="text/csv"
        )
    else:
        st.info("Keine Teilnehmer für diesen Deal gefunden.")
