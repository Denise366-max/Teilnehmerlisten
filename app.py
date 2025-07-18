import streamlit as st
import requests
import pandas as pd

API_TOKEN = "dfaec32a80975c26802ef8fcf68bf4cc72990046"
BASE_URL = "https://api.pipedrive.com/v1"

custom_field_keys = [
    "b94970cec0683f8f5cadf4d3fab7079744ac28bb",
    "fd69701c7c53f9854ad1df204cd81da18111a072",
    "179be66b310cfbf4d1767437563e6fc902714c9a",
    "6f9c097dc7bbc95739bebb8c48568b51c32aff26",
    "01377c7c43ae80f19389c65d42efb810b6e8550a",
    "d2fbe7e0ce8cf09700ea21d889c2a916e2ddf998",
    "f23da18af8d33cea710381dc6153fc561cc851f8",
    "bcfe6354dd76859d01e22c7ff091f5e2c072acda",
    "8c1e8e89c4434d868075f21b98367b9cd9a2261c",
    "9cd06a5ed78b5f958f8a7c44d8d4d721cfe406c6",
    "de83542f0b2e38add0642101f11318ff095ddd21",
    "4d64992cc7cae75827de3500849d8845ab48d0e3",
    "309dd96701de50c73cf0cb3f2ba468bec57fa7aa",
    "8d4f95f9410329cc17d4ad055c17310d718f6159",
    "0c5c0e0865e3ae8d982f7cb30aa3c37eff13184b",
    "f9be7b6ab264301204974afd9d8602352e02ce28",
    "3d0a1e3f721f0abbc50843202476318ce4b3258e",
    "214f05f31ed7d6bc7fac9dd51ef893c3a151462b"
]

def get_deal_data(deal_id):
    url = f"{BASE_URL}/deals/{deal_id}?api_token={API_TOKEN}"
    response = requests.get(url)
    return response.json().get('data') if response.status_code == 200 else None

def get_person_details(person_id):
    url = f"{BASE_URL}/persons/{person_id}?api_token={API_TOKEN}"
    response = requests.get(url)
    return response.json().get('data') if response.status_code == 200 else None

st.title("Pipedrive Deal Teilnehmer inkl. Organisation")

deal_id = st.text_input("Bitte Deal-ID eingeben:")

if deal_id:
    with st.spinner("Lade Daten..."):
        deal_data = get_deal_data(deal_id)

    if deal_data:
        teilnehmer_list = []

        for i, field_key in enumerate(custom_field_keys, start=1):
            teilnehmer_info = deal_data.get(field_key)

            if teilnehmer_info and isinstance(teilnehmer_info, dict):
                name = teilnehmer_info.get('name', '')
                emails = teilnehmer_info.get('email', [])
                email = next((e.get('value', '') for e in emails if e.get('value')), '')
                person_id = teilnehmer_info.get('id')

                organisation = ""
                if person_id:
                    person_data = get_person_details(person_id)
                    st.write(f"Debug Person {person_id} → {person_data}")  # DEBUG-Ausgabe
                    if person_data:
                        org_data = person_data.get('org_id')
                        if org_data:
                            organisation = org_data.get('name', '')

            else:
                name = ""
                email = ""
                organisation = ""

            teilnehmer_list.append({
                'Teilnehmer': f'Teilnehmer {i}',
                'Name': name,
                'E-Mail': email,
                'Organisation': organisation
            })

        df = pd.DataFrame(teilnehmer_list)

        st.dataframe(df)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("CSV herunterladen", csv, file_name=f"deal_{deal_id}_teilnehmer.csv", mime='text/csv')

    else:
        st.error("Deal nicht gefunden oder Fehler beim Abruf.")

