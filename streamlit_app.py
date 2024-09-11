import streamlit as st
import pandas as pd
import json
from io import BytesIO
import os
from openai import OpenAI
from prompt_functions import generate_prompt
from dotenv import load_dotenv

# Lade die Umgebungsvariablen aus der .env-Datei
load_dotenv()

# Setze den OpenAI API-Schlüssel
OPENAI_API_KEY=st.secrets['OPENAI_API_KEY']

# App Titel und Logo
st.image("logo.png", width=150)  # Füge dein Logo ein

# Standardmäßig wird Deutsch als Sprache angenommen, bevor der Benutzer eine Auswahl trifft
default_language = "Deutsch"

# Sprachauswahl zuerst definieren (bevor die anderen Texte dynamisch angepasst werden)
language_label = "Sprache wählen" if default_language == "Deutsch" else "Choose Language"
language = st.sidebar.radio(language_label, ("Deutsch", "Englisch"))



if language == "Deutsch":
    st.title("🎨 Künstler E-Mail Generator")
else:
    st.title("🎨 Artist Email Generator")

if language == "Deutsch":
    st.write("_Hinweis: Der Prototyp ist auf maximal 20 E-Mails begrenzt._")
else:
    st.write("_Note: The prototype is limited to a maximum of 20 emails._")


# Tabs zur Organisation der App
tab1, tab2 = st.tabs(["Upload & Prozess", "Ergebnisse"])

# Tab 1: Datei-Upload und Prozess
with tab1:
    if language == "Deutsch":
        st.header("Datei-Upload")
        uploaded_file = st.file_uploader("Lade eine Excel-Datei hoch", type=["xlsx"])
    else:
        st.header("File Upload")
        uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])

    if uploaded_file:
        df = pd.read_excel(uploaded_file).head(20)
        
        if language == "Deutsch":
            st.success("Datei erfolgreich hochgeladen!")
        else:
            st.success("File uploaded successfully!")

        # Button zur Generierung der E-Mails
        if st.button('E-Mails generieren' if language == "Deutsch" else 'Generate Emails'):
            st.info("E-Mails werden generiert..." if language == "Deutsch" else "Generating emails...")

            # Check, ob alle erforderlichen Spalten vorhanden sind
            required_columns = ['ID', 'First Name', 'ArtPreference', 'Authenticity', 'Size', 'Story', 'Clicked more than 3', 'Opened more than 3', 'Buyer ', 'language']
            if all(col in df.columns for col in required_columns):
                # Neue Spalten mit dem Datentyp string erstellen
                df['Subject_Text'] = df['Subject_Text'].astype(str)
                df['Text1'] = df['Text1'].astype(str)
                df['Text2'] = df['Text2'].astype(str)
                df['Preview_Text'] = df['Preview_Text'].astype(str)

                # Filtere Zeilen, in denen 'ID' und 'First Name' gefüllt sind
                df = df.dropna(subset=['ID', 'First Name'])

                client = OpenAI(api_key=api_key)
                # Function to generate personalized email text
                def generate_email_text(row):
                    base_prompt = generate_prompt(row)

                    completion = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[{"role": "user", "content": base_prompt}],
                        temperature=1,
                        response_format={"type": "json_object"}
                    )
                    
                    json_content = completion.choices[0].message.content
                    parsed_json = json.loads(json_content)
                    return parsed_json

                # Iteriere durch die Zeilen des DataFrames und generiere E-Mail-Inhalte
                for index, row in df.iterrows():
                    email_content = generate_email_text(row)
                    kunde = email_content['Kunden'][0]

                    # Speichere die Ergebnisse in den entsprechenden DataFrame-Spalten
                    df.at[index, 'Subject_Text'] = kunde['Betreff']
                    df.at[index, 'Text1'] = kunde['Anrede']
                    df.at[index, 'Text2'] = kunde['Email_Text']
                    df.at[index, 'Preview_Text'] = kunde['Pre-Header']

                # Speichere die aktualisierte Datei zur Ausgabe
                output = BytesIO()
                df.to_excel(output, index=False)
                output.seek(0)

                # Button zum Herunterladen der aktualisierten Datei
                st.download_button(
                    label="Download aktualisierte Excel-Datei" if language == "Deutsch" else "Download updated Excel file",
                    data=output,
                    file_name="Survey_updated_with_emails.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.error(
                    f"Die hochgeladene Datei enthält nicht alle erforderlichen Spalten: {', '.join(required_columns)}" 
                    if language == "Deutsch" 
                    else f"The uploaded file does not contain all required columns: {', '.join(required_columns)}"
                )

# Tab 2: Ergebnisse anzeigen und Datei-Download
with tab2:
    if language == "Deutsch":
        st.header("Ergebnisse")
    else:
        st.header("Results")

    if uploaded_file and 'Subject_Text' in df.columns:
        # Zeige den DataFrame mit den generierten E-Mails an
        st.dataframe(df[['ID', 'First Name', 'Subject_Text', 'Text1', 'Text2','Preview_Text']])
    else:
        if language == "Deutsch":
            st.warning("Generiere E-Mails und Ergebnisse, bevor du diese Seite öffnest.")
        else:
            st.warning("Generate emails and results before opening this page.")
