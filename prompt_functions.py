
import os
from dotenv import load_dotenv
# Load the environment variables from the .env file
load_dotenv()

# Lade den API-Schlüssel aus der .env Datei
# Setze den OpenAI API-Schlüssel
api_key=st.secrets['OPENAI_API_KEY']


def generate_prompt(row):
    base_prompt = f"""
    
    Du bist ein junger Künstler und möchtest den Besuchern Deiner Online-Galerie Skizzen Deiner Werke verkaufen. Skizzen sind Vorstudien zu dem eigentlichen Kunstwerk. Sie sind Originale (also Auflage 1), aber mit ca. 750 – 950 Euro wesentlich günstiger als die Original-Kunstwerke, die Du für 5.000 bis 7.500 Euro verkaufst. Sie sind damit eine Art „mittlere Alternative“ zwischen Artprints (Auflage um die 200 Stück), die mit ca. € 100 relativ günstig verkauft werden, und den Originalen.

    Um die Verkäufe zu steigern, schickst Du Deinen Kunden eine E-Mail.  Damit die Kaufrate (= Conversion) möglichst hoch ist, schreibst Du jeden Kunden ganz individuell nach seinen Interessen an. 

    Was diese Interessen sind, hast Du in einer Umfrage herausgefunden. 
    Die Fragen waren wie folgt: 
    1. do you prefer classical art such as paintings and sculptures or do you find modern art forms such as installations and digital art more exciting?  
    Antwortmöglichkeiten zur Frage 1: Classical works of art are more my thing. - classical I am totally fascinated by modern art forms. - modern I can get something out of both styles of art. - both For me, it's the artwork itself that counts, regardless of the style. - no care   

    2. does the size of a work of art make a difference to you or are you open to everything, no matter how big or small?   
    Antwortmöglichkeiten zur Frage 2: Large works of art blow me away more. - large Small artworks often have that certain something. - small Size doesn't matter to me, I like any shape and any scale. - both I like to experience art in different sizes. -  no care   

    3. how important is the story behind a work of art or the artist to you if you were to buy it?   Antwortmöglichkeiten zur Frage 3: The story is super important to me. - important The background story is interesting, but not crucial. - interesting I'm mainly interested in the feeling and the aesthetics of the artwork. - aesthetic The story doesn't matter to me, it's the artwork that counts. - no care   
    4. how important is it to you that a work of art is an original compared to limited editions or reproductions?    Antwortmöglichkeiten zur Frage 4: An original is much cooler for me. - original I find limited editions just as exciting. - limited Reproductions are a good and affordable alternative. - reproduction For me, it's the artwork that counts, whether it's an original or not, it doesn't matter - no care 

    Außerdem verfügst Du über folgende Informationen: Hat der Empfänger schon einmal ein Kunstwerk gekauft (dann Spalte „Buyer“ = yes) Reagiert der Empfänger viel auf E-Mails (dann Spalte „clicked more than 3“ = yes) 
    
    Weitere Hinweise: In der Spalte language steht ein „en“ für englischen Empfänger und ein „de“ für deutschen Empfänger. Liefere entsprechend deutsche bzw. englische texte die Empfänger sollen nicht wissen, dass der Künstler weiss, ob die E-Mails geöffnet werden. Nutze in diesem Fall eine neutralere Formulierung wie "Ich habe gemerkt, dass dich meine E-Mails interessieren". 
    
    Der Text soll immer etwas unterschiedlich sein. 
    Wenn jemand gekauft hat, solltest du das besonders erwähnen (nochmal ganz herzlich bedanken, …) Wenn jemand gekauft hat, obwohl er nur weniger als 3x geklickt hat, ist er ein schnell entscheidender Käufer. Buyers should be thanked for purchasing before 
    
    Du duzt Deine Gesprächspartner.
    Deine Aufgabe: Schreibe einen Text von maximal 1.000 Zeichen, um für Skizzen zu promoten und nutze dabei die Antworten des Interessenten und die weiteren Infos wie Buyer oder clicked more than 3. Schreibe außer dem eigentlichen Text auch einen Betreff (maximal um die 45 Zeichen) und einen Pre-Header (maximal um die 70 Zeichen).
    Gib die Antworten in einem JSON aus, wobei die erste Spalte die ID, die zweite der Betreff, dritte die Anrede, die vierte der Pre-Header und die fünfte Spalte der eigentliche Text sind. Schreib auf Deutsch. Erwähnen und bedanken Sie sich im Text bei Personen, die oft geklickt und geöffnet oder vor allem etwas gekauft haben. Wenn die Person etwas gekauft hat, bedanken Sie sich für den vorherigen Kauf. Schreiben Sie meine Kollektion, nicht unsere. Bedanken Sie sich für großes Interesse nur, wenn sowohl das Öffnen als auch das Anklicken YES ist.


    Hier sind die Daten des Kunden, auf deren Basis der Text erstellt werden soll:

    - ID: {row['ID']}
    - Vorname: {row['First Name']}
    - Kunstpräferenz: {row['ArtPreference']}
    - Authentizität: {row['Authenticity']}
    - Größe der Kunstwerke: {row['Size']}
    - Bedeutung der Story: {row['Story']}
    - Klickt oft auf E-Mails: {row['Clicked more than 3']}
    - Öffnet oft E-Mails: {row['Opened more than 3']}
    - Käufer: {row['Buyer ']}
    - Sprache: {row['language']}  (schreibe den kompletten Text auf Englisch, wenn {row['language']}: 'en' oder Deutsch wenn {row['language']}:'de'

    Am Ende soll das Ergebnis immer im selben JSON Format geliefert werden, welches folgendermaßen beginnt:
    
    Beispiel-JSON:

    'Kunden': [
            'ID': '...',
            'Betreff': '...',
            'Anrede': '...,',
            'Pre-Header': '...',
            'Email_Text': '...'
        
    ]
    """
    return base_prompt

