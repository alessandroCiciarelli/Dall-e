#Librerie
import base64
import io
import json
import random
from time import sleep
from matplotlib import pyplot as plt
from openpyxl import Workbook
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
import people_also_ask_it
import urllib
import requests
from datetime import date
from pytrends.request import TrendReq
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder, JsCode
pytrends = TrendReq()
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from deep_translator import GoogleTranslator
from aitextgen import aitextgen

#Impostazioni pagina
st.set_page_config(layout="wide")

hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.markdown("<center><h1> Italian Intelligence Seo Suite </h1>", unsafe_allow_html=True)
st.markdown('<center><b>Tutti i tool di Analisi, Ricrca e Generazione Keyword e Contenuti in unico Posto ⚡</b><br><small> Powered by INTELLIGENZAARTIFICIALEITALIA.NET </small></center> ', unsafe_allow_html=True)

st.write(" ")
st.write(" ")

choose = option_menu("La miglior Suite di SEO gratis 🐍🔥", ["Analisi" , "Ricerca", "Competitor", "Domande" , "Contenuti"],
                 icons=[ 'body-text', 'keyboard', 'exclamation-triangle', 'patch-question' ,'journal-bookmark'],
                 menu_icon="app-indicator", default_index=0,orientation='horizontal',
                 styles={
"container": {"color": "blak","padding": "4!important", "background-color": "#dedede", "width": "100%"},
"icon": {"color": "blak", "font-size": "12px"}, 
"nav-link": {"color": "blak","font-size": "13px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
"nav-link-selected": {"color": "blak","background-color": "#02ab21"},
}
)


## GESTIONE UTENTI PREMIUM

if 'premium' not in st.session_state:
    #set session premium key to false
    st.session_state['premium'] =  False

if 'nome' not in st.session_state:
    st.session_state['nome'] =  ""

if 'scelta' not in st.session_state:
    st.session_state['scelta'] =  choose


def premium_check(user,codice):
    #test if codice is in Secrets Management of streamlit
    #LitsaKey = st.secrets["KEY"]
    ListaKey = "ale:123/babbo:1234"
    #split ListaKey in list of keys for "/"
    ListaKey = ListaKey.split("/")
    ListaUser = []
    ListaChiavi = []
    #for each key in ListaKey
    for key in ListaKey:
        #split key in list of keys for ":"
        ListaUser.append(key.split(":")[0])
        ListaChiavi.append(key.split(":")[1])
    #test if user is in ListaUser and if codice is in ListaChiavi
    if user in ListaUser and codice in ListaChiavi:
        #set session premium key to true
        st.session_state.premium = True
        st.session_state.nome = user
        return True
    else:
        #set session premium key to false
        st.session_state.premium = False
        return False


        
if st.session_state.premium == False:
    with st.expander(" Sei un UTENTE PREMIUM 👑 ? "):
            st.markdown("<center><h1>Benvenuto Utente Premium 👑</h1>", unsafe_allow_html=True)
            #define tree streamlit columns
            cc1, cc2= st.columns(2)
            user = cc1.text_input("Inserisci il tuo nome utente 👤")
            codice = cc2.text_input("Inserisci il tuo codice di accesso 🔑")
            dd1, dd2, dd3 = st.columns(3)
            if dd2.button("Accedi ora e sblocca tutte le funzionalità PREMIUM, nulla sarà come prima 🔐"):
                if premium_check(user,codice):
                    st.success("Benvenuto "+user+" 👑 Tra poco questa sezione scomparirà 🤓") 
                else:
                    st.error("Codice o Nome Utente errati ❌")
                
            st.markdown("<center><h1>Vuoi Diventare un Utente Premium 👑 ?</h1>", unsafe_allow_html=True)
            text2 = st.markdown(" ", unsafe_allow_html=True)
            st.markdown("<center><b> 1️⃣ Sezione Analisi COMPARAZIONE PIANI FREE👤 VS PREMIUM👑 </b> ", unsafe_allow_html=True)
            sezioneAnalisi = pd.read_csv("Analisi.csv")
            gb = GridOptionsBuilder.from_dataframe(sezioneAnalisi)
            gb.configure_default_column(editable=True)
            gb.configure_grid_options(enableRangeSelection=True)
            response = AgGrid(
                sezioneAnalisi,
                height="200px",
                gridOptions=gb.build(),
                fit_columns_on_grid_load=True,
                allow_unsafe_jscode=True,
                enable_enterprise_modules=True
            )


            st.write(" ")
            st.write(" ")
            st.markdown("<center><b>2️⃣ Sezione Ricerca COMPARAZIONE PIANI FREE👤 VS PREMIUM👑 </b>", unsafe_allow_html=True)
            sezioneRicerca = pd.read_csv("Ricerca.csv")
            gb = GridOptionsBuilder.from_dataframe(sezioneRicerca)
            gb.configure_default_column(editable=True)
            gb.configure_grid_options(enableRangeSelection=True)
            response = AgGrid(
                sezioneRicerca,
                height="200px",
                gridOptions=gb.build(),
                fit_columns_on_grid_load=True,
                allow_unsafe_jscode=True,
                enable_enterprise_modules=True
            )
            st.write(" ")
            st.write(" ")
            st.markdown("<center><b>3️⃣ Sezione Competitor COMPARAZIONE PIANI FREE👤 VS PREMIUM👑 </b>", unsafe_allow_html=True)
            sezioneCompetitor = pd.read_csv("Competitor.csv")
            gb = GridOptionsBuilder.from_dataframe(sezioneCompetitor)
            gb.configure_default_column(editable=True)
            gb.configure_grid_options(enableRangeSelection=True)
            response = AgGrid(
                sezioneCompetitor,
                height="200px",
                gridOptions=gb.build(),
                fit_columns_on_grid_load=True,
                allow_unsafe_jscode=True,
                enable_enterprise_modules=True
            )
            st.write(" ")
            st.write(" ")
            st.markdown("<center><b>4️⃣ Sezione Domande COMPARAZIONE PIANI FREE👤 VS PREMIUM👑 </b>", unsafe_allow_html=True)
            sezioneDomande = pd.read_csv("Domande.csv")
            gb = GridOptionsBuilder.from_dataframe(sezioneDomande)
            gb.configure_default_column(editable=True)
            gb.configure_grid_options(enableRangeSelection=True)
            response = AgGrid(
                sezioneDomande,
                height="200px",
                gridOptions=gb.build(),
                fit_columns_on_grid_load=True,
                allow_unsafe_jscode=True,
                enable_enterprise_modules=True
            )
            st.write(" ")
            st.write(" ")
            st.markdown("<center><b>5️⃣ Sezione Contenuti COMPARAZIONE PIANI FREE👤 VS PREMIUM👑 </b>", unsafe_allow_html=True)
            sezioneContenuti = pd.read_csv("Testo.csv")
            gb = GridOptionsBuilder.from_dataframe(sezioneContenuti)
            gb.configure_default_column(editable=True)
            gb.configure_grid_options(enableRangeSelection=True)
            response = AgGrid(
                sezioneContenuti,
                height="200px",
                gridOptions=gb.build(),
                fit_columns_on_grid_load=True,
                allow_unsafe_jscode=True,
                enable_enterprise_modules=True
            )
            st.write(" ")
            st.write(" ")
            st.markdown("<center><h3><a href='https://www.intelligenzaartificialeitalia.net/compra-seoia' >Passa ORA a PREMIUM 👑 per SOLI 5€ al mese, non te ne pentirai 🤓</a><h3>", unsafe_allow_html=True)
else:
    st.success("Benvenuto "+st.session_state.nome+" 👑")


#Funzioni di uso genrale

#def function to generate multiple texts with ai.generate_samples()
def ai_text(inp,lunghezza, temp, num):
    listaTesti = []
    ai = aitextgen()
    for i in range(num):
        generated_text = ai.generate_one(max_length = lunghezza, prompt = inp, no_repeat_ngram_size = random.randint(3, 5) , temperature = temp)
        listaTesti.append(entoit(generated_text))
    return listaTesti

def ittoen(testo):
    return GoogleTranslator(source='auto', target='en').translate(testo)

def entoit(testo):
    return GoogleTranslator(source='auto', target='it').translate(testo)


def removeRestrictedCharactersAndWhiteSpaces(keywords):

    restricted_characters = ['-', ',', '\'', ')', '(', '[', ']', '{', '}', '.', '*', '?', '_', '@', '!', '$']

    preprocessed_list = []
    
    for keyword in keywords:
    
        clean_keyword = ""
        for char in keyword:
            if char not in restricted_characters:
                clean_keyword += char
        
        white_space_counter = 0
        
        for char in clean_keyword:
            if char == ' ':
                white_space_counter += 1
            else:
                break
        
        clean_keyword = clean_keyword[white_space_counter:]
        
        white_space_counter = 0
        
        for i in range(len(clean_keyword) - 1, 0, -1):
            if clean_keyword[i] == ' ':
                white_space_counter += 1
            else:
                break
        
        if white_space_counter != 0:
            clean_keyword = clean_keyword[:-white_space_counter]
        
        preprocessed_list.append(clean_keyword)
    
    return preprocessed_list


def gSuggest(kw):
    ua = get_random_useragent()
    headers = {"user-agent": ua}
    client = get_random_client()
    #st.text(ua)
    googleSuggestURL="https://suggestqueries.google.com/complete/search?hl=it&gl=it&lr=lang_it&client="+ client +"&q="
    response = requests.get(googleSuggestURL+kw, headers=headers)

    #create while loop to check if response is ok
    #if not set headers again and try again with new headers
    #counter
    counter = 0
    while response.status_code != 200 and counter < 15:
        ua = get_random_useragent(ua)
        client = get_random_client(client)
        #st.text(ua)
        googleSuggestURL="https://suggestqueries.google.com/complete/search?hl=it&gl=it&lr=lang_it&client="+ client +"&q="
        sleep(1)
        headers = {"user-agent": ua}
        response = requests.get(googleSuggestURL+kw, headers=headers)
        sleep(2)
        counter += 1

    if counter == 15:
        return None

    #st.write(response)
    result = json.loads(response.content.decode('utf-8'))
    result = result[1]
    return result

#make function to use fake_useragent library
# the scope of function is to return a random useragent from the list of useragents
# input current useragent
# output random useragent not equal to current useragent
def get_random_useragent(useragent=None):
    from fake_useragent import UserAgent
    if useragent is None:
        ua = UserAgent()
        return ua.random
    else:
        ua = UserAgent()
        newUA = ua.random
        while newUA == useragent:
            newUA = ua.random
        return newUA

def get_random_client(client=None):
    if client is None:
        return "Chrome"
    elif client == "Chrome":
        return "Firefox"
    elif client == "Firefox":
        return "Safari"
    else:
        return "Opera"
    

    



def suggest(keyword, depth):
    data = gSuggest(keyword)
    if data is None:
        return None
    data.remove(data[0])
    for i in range(0, depth):
        for suggestion in data:
            #st.write(suggestion)
            sleep(0.5)
            data = data+gSuggest(suggestion)
    return data

def distribution(suggests, nbResult=40, kwToRemove=''):
    tokenized_sentence=sent_tokenize(' '.join(suggests))
    tokenized_word=word_tokenize(', '.join(tokenized_sentence).replace(kwToRemove+' ', ''))
    fdist = FreqDist(tokenized_word)
    return fdist    #plt.show()

def df_suggest(df, _type='liste', kwToRemove=[]):
    data = {}
    liste = list(df.unique())
    #print(liste)
    for expression in liste:
        data[expression] = suggest(expression, 1)
   # print(data)


    
#1 Analisi
if choose=="Analisi":
    
    with st.expander("Cos'è e come funziona la sezione Analisi 🤔"):
        text2 = st.markdown("In questa sezione potrai analizzare l'interesse nel tempo delle keyword e in quali regiorni d'Italia ci sono più ricerche.<br> La sezione di <bold>Analisi Keyword</bold> per ogni keyword inserita il tool genererà:<br>🔹Il trend di ricerca nel tempo<br>🔹Il trend di ricerca nelle regioni in Italia<br>🔹Top Trend correlati alla Keyword<br>🔹Tendenze in aumento correlate alla Keyword<br>🔹I competitor più forti sulla keyword<br>🔹Le domande più frequenti fatte sulla keyword", unsafe_allow_html=True)
        text3 = st.markdown("Per iniziare ti basterà :<br>1️⃣ Incollare le keywords (una per riga) [MAX FREE 3 keywords]<br> 2️⃣ Scegliere il paese<br>3️⃣ Scegli il periodo di tempo<br>4️⃣ Premi <bold>'Scopri le tendenze🤘'</bold> ", unsafe_allow_html=True)
        st.write("  ")
        st.write("  ")

    #Inserimento Keyword    
    text = st.text_area("Powered by IntelligenzaArtificialeItalia.net", height=150, key=1)

    #pulisco il teso in input
    linesDeduped2 = []
    MAX_LINES = 5

    if st.session_state.premium == True:
        MAX_LINES = 10
    else:
        MAX_LINES = 3

    lines = text.split("\n")  # A list of lines
    linesList = []
    for x in lines:
        linesList.append(x)
    linesList = list(dict.fromkeys(linesList))  # Remove dupes
    linesList = list(filter(None, linesList))  # Remove empty

    if len(linesList) > MAX_LINES:
        if st.session_state.premium == True:
            st.warning(f"⚠️ Attenzione, Puoi inserire al massima 10 keywords. ⚠️")
            linesList = linesList[:MAX_LINES]
        else:
            st.warning(f"⚠️ Attenzione, Puoi inserire al massima 3 keywords. ⚠️")
            linesList = linesList[:MAX_LINES]

    from parseCountries import parse
    country_names, country_codes = parse()
    country_names, country_codes = country_names[:243], country_codes[:243]
    country = st.selectbox("Scegli il paese", country_names)
    st.write(f"Hai selezionato " + country)
    idx = country_names.index(country)
    country_code = country_codes[idx],

    #carico i periodi di tempo
    selected_timeframe = ""
    period_list = ["Ultimi 12 Mesi", "Ultima Ora", "Ultime 4 Ore", "Ultime 24 Ore", "Ultimi 7 Giorni", "Ultimi 30 Giorni", "Ultimi 90 Giorni", "Ultimi 5 Anni", "2004 - Oggi", "CUSTOM"]
    tf = ["today 12-m", "now 1-H", "now 4-H", "now 1-d", "now 7-d", "today 1-m", "today 3-m", "today 5-y", "all", "custom"]
    timeframe_selectbox = st.selectbox("Scegli il periodo", period_list)
    idx = period_list.index(timeframe_selectbox)
    selected_timeframe = tf[idx]
    todays_date = date.today()
    current_year = todays_date.year

    years = list(range(2005, current_year + 1))
    months = list(range(1, 13))
    days = list(range(1, 32))

    if selected_timeframe == "custom":
        
        st.write(f"Da")

        col11, col12, col13 = st.columns(3)
        year_from = col11.selectbox("Anno", years, key="0")
        month_from = col12.selectbox("Mese", months, key="1")
        day_from = col13.selectbox("Giorno", days, key="2")
        
        st.write(f"a")

        col21, col22, col23 = st.columns(3)
        year_to = col21.selectbox("Anno", years, key="3")
        month_to = col22.selectbox("Mese", months, key="4")
        day_to = col23.selectbox("Giorno", days, key="5")
        
        selected_timeframe = str(year_from) + "-" + str(month_from) + "-" + str(day_from) + " " + str(year_to) + "-" + str(month_to) + "-" + str(day_to)
        

    #bottone per scoprire le tendenze
    start_execution = st.button("Scopri le tendenze🤘")



    if start_execution:


        if len(linesList) == 0:
        
            st.warning("Perfavore inserisci almeno una keyword.  ⚠️") # ⚠️
        
        if len(linesList) == 1:
            linesList = removeRestrictedCharactersAndWhiteSpaces(linesList)
            pytrends.build_payload(linesList, timeframe=selected_timeframe, geo=country_code[0])
            related_queries = pytrends.related_queries()
            temp = pytrends.interest_over_time().drop('isPartial', axis=1)
            citta = pytrends.interest_by_region(resolution='CITY', inc_low_vol=False, inc_geo_code=False)
        
        else:
            linesList = removeRestrictedCharactersAndWhiteSpaces(linesList)
            pytrends.build_payload(linesList, timeframe=selected_timeframe, geo=country_code[0])
            related_queries = pytrends.related_queries()
            temp = pytrends.interest_over_time().drop('isPartial', axis=1)
            st.line_chart(temp)
            citta = pytrends.interest_by_region(resolution='CITY', inc_low_vol=False, inc_geo_code=False)
            
        
        for i in range(len(linesList)):
            keykey = linesList[i]
            st.header("Analisi della keyword {} : {}".format(i+1, str(linesList[i])))
            st.line_chart(temp[str(linesList[i])])
            st.bar_chart(citta[str(linesList[i])])
            c29, c31 = st.columns(2)

            with c29:

                st.subheader("Top Trends🏆")
                try:
                    if st.session_state.premium == True:
                        gb = GridOptionsBuilder.from_dataframe(related_queries.get(linesList[i]).get("top"))
                        gb.configure_default_column(editable=True)
                        gb.configure_grid_options(enableRangeSelection=True)
                        with st.spinner('Stiamo hackerando GOOGLE per analizzare le keywords ... 🕐 Potrebbe volerci qualche minuto 🙏'):
                            response = AgGrid(
                                related_queries.get(linesList[i]).get("top"),
                                gridOptions=gb.build(),
                                fit_columns_on_grid_load=True,
                                allow_unsafe_jscode=True,
                                enable_enterprise_modules=True
                            )
                            st.write("Per esportare i dati, usa il tasto desto del mouse 🚀")
                    else:
                        topTrendFree = related_queries.get(linesList[i]).get("top")
                        #write on frist row on "query" column "Solo per PREMIUM"
                        topTrendFree.loc[0, "query"] = "Solo per PREMIUM 👑"
                        #iterate topTrendFree and remove write on "query" column "Solo per PREMIUM 👑" tranne per le 6 righe e per le ultime 5 righe
                        for i in range(len(topTrendFree)):
                            if i > 5 and i < len(topTrendFree)-5:
                                topTrendFree.loc[i, "query"] = topTrendFree.loc[i, "query"]
                            else:
                                topTrendFree.loc[i, "query"] = "Solo per PREMIUM 👑"
                        

                        gb = GridOptionsBuilder.from_dataframe(topTrendFree)
                        gb.configure_default_column(editable=True)
                        gb.configure_grid_options(enableRangeSelection=True)
                        with st.spinner('Stiamo hackerando GOOGLE per analizzare le keywords ... 🕐 Potrebbe volerci qualche minuto 🙏'):
                            response = AgGrid(
                                topTrendFree,
                                gridOptions=gb.build(),
                                fit_columns_on_grid_load=True,
                                allow_unsafe_jscode=True
                            )
                            st.write("Per esportare i dati, passa a Premium 🚀")

                    
                except:
                    st.write("Nessuna query in tendenza")

            with c31:
                st.subheader("Tendenze in aumento⚡")
                try:
                    if st.session_state.premium == True:
                        gb = GridOptionsBuilder.from_dataframe(related_queries.get(keykey).get("rising"))
                        gb.configure_default_column(editable=True)
                        gb.configure_grid_options(enableRangeSelection=True)
                        with st.spinner('Stiamo hackerando GOOGLE per analizzare le keywords ... 🕐 Potrebbe volerci qualche minuto 🙏'):
                            response = AgGrid(
                                related_queries.get(linesList[i]).get("rising"),
                                gridOptions=gb.build(),
                                fit_columns_on_grid_load=True,
                                allow_unsafe_jscode=True,
                                enable_enterprise_modules=True
                            )
                            st.write("Per esportare i dati, usa il tasto desto del mouse 🚀")
                    else:
                        topTrendenzeFree = related_queries.get(keykey).get("rising")
                        #write on frist row on "query" column "Solo per PREMIUM"
                        topTrendenzeFree.loc[0, "query"] = "Solo per PREMIUM 👑"
                        #iterate topTrendenzeFree and remove write on "query" column "Solo per PREMIUM 👑" tranne per le 6 righe e per le ultime 5 righe
                        for i in range(len(topTrendenzeFree)):
                            if i > 5 and i < len(topTrendenzeFree)-5:
                                topTrendenzeFree.loc[i, "query"] = topTrendenzeFree.loc[i, "query"]
                            else:
                                topTrendenzeFree.loc[i, "query"] = "Solo per PREMIUM 👑"
                            
                        gb = GridOptionsBuilder.from_dataframe(topTrendenzeFree)
                        gb.configure_default_column(editable=True)
                        gb.configure_grid_options(enableRangeSelection=True)
                        with st.spinner('Stiamo hackerando GOOGLE per analizzare le keywords ... 🕐 Potrebbe volerci qualche minuto 🙏'):
                            response = AgGrid(
                                topTrendenzeFree,
                                gridOptions=gb.build(),
                                fit_columns_on_grid_load=True,
                                allow_unsafe_jscode=True
                            )
                            st.write("Per esportare i dati, passa a Premium 🚀")

                    
                except:
                    st.write("Nessuna query in tendenza")

            from ecommercetools import seo
            st.subheader("Competitor principali 🏈")

            query = {
                "q": str(keykey),
                "num" : 10,
                "lr": "lang_it"

            }

            headers = {
                "X-User-Agent": "desktop",
                "X-Proxy-Location": "EU",
                "X-RapidAPI-Host": "google-search3.p.rapidapi.com",
                "X-RapidAPI-Key": "9aa97656a1msh1eed14c02210a68p1edf50jsn5443f0381996"
            }
            resp = requests.get("https://rapidapi.p.rapidapi.com/api/v1/search/" + urllib.parse.urlencode(query), headers=headers)

            results = resp.json()
            #create dataframe
            concorrenti =  pd.DataFrame(columns=['Posizionamento su Google','Dominio', 'Titolo'])
            #st.write(results)
            h=1
            for result in results["results"]:
                title = result['title']
                link = result['link']

                subdomain= link.split("/")[2]
                #st.write(title,link)
                concorrenti.loc[h] = [h] + [subdomain] + [title] 
                h=h+1
            
            if st.session_state.premium == True:
                gb = GridOptionsBuilder.from_dataframe(concorrenti)
                gb.configure_default_column(editable=True)
                gb.configure_grid_options(enableRangeSelection=True)
                with st.spinner('Aspetta un attimo... 🕐 Potrebbe volerci qualche minuto 🙏'):
                    response = AgGrid(
                        concorrenti,
                        fit_columns_on_grid_load=True,
                        allow_unsafe_jscode=True,
                        enable_enterprise_modules=True
                    )
                    st.write("Per esportare i dati, usa il tasto desto del mouse 🚀")
            else:
                concorrentiFree = concorrenti
                #iterate concorrentiFree and write on "Dominio" and "Titolo" column "Solo per PREMIUM" per le prime 4 righe
                for index, row in concorrentiFree.iterrows():
                    if index < 6:
                        concorrentiFree.at[index, "Dominio"] = "Solo per PREMIUM 👑"
                        concorrentiFree.at[index, "Titolo"] = "Solo per PREMIUM 👑"
  
                with st.spinner('Aspetta un attimo... 🕐 Potrebbe volerci qualche minuto 🙏'):
                    response = AgGrid(
                        concorrentiFree,
                        fit_columns_on_grid_load=True,
                        allow_unsafe_jscode=True
                    )
                    st.write("Per esportare i dati, passa a Premium 🚀")

                
            st.write("")
            st.subheader("Domande principali ❓")
            with st.spinner('Stiamo HACKERANDO google e bing dacci qualche minuto (non è uno scherzo!) ... 🕐 Potrebbe volerci qualche minuto 🙏'):
                domande = people_also_ask_it.get_related_questions(str(keykey), 10)
            if st.session_state.premium == True:
                domandePremium = pd.DataFrame(columns=['Domanda'])
                for dom in domande:
                    domanda = dom.split("Cerca: ")
                    domandePremium.loc[len(domandePremium)] = [domanda[1]]
                with st.spinner('Stiamo HACKERANDO google e bing dacci qualche minuto (non è uno scherzo!) ... 🕐 Potrebbe volerci qualche minuto 🙏'):
                    response = AgGrid(
                        domandePremium,
                        fit_columns_on_grid_load=True,
                        allow_unsafe_jscode=True,
                        enable_enterprise_modules=True
                    )
                    st.write("Per esportare i dati, usa il tasto desto del mouse 🚀")
            else:
                domandeFree = pd.DataFrame(columns=['Domanda'])
                for dom in domande:
                    domanda = dom.split("Cerca: ")
                    domandeFree.loc[len(domandeFree)] = [domanda[1]]
                #iterate domandeFree and write on "Domanda" column "Solo per PREMIUM" tranne per le prime 3 righe
                for index, row in domandeFree.iterrows():
                    if index > 2:
                        domandeFree.at[index, "Domanda"] = "Solo per PREMIUM 👑"
                with st.spinner('Stiamo HACKERANDO google e bing dacci qualche minuto (non è uno scherzo!) ... 🕐 Potrebbe volerci qualche minuto 🙏'):
                    response = AgGrid(
                        domandeFree,
                        fit_columns_on_grid_load=True,
                        allow_unsafe_jscode=True
                    )
                    st.write("Per esportare i dati, passa a Premium 🚀")

            st.markdown("""<hr/><br>""", unsafe_allow_html=True)
            
        st.balloons()

#2 Ricerca
if choose=="Ricerca":
    MAX_LINES = 1
    with st.expander("Cos'è e come funziona la sezione Ricerca 🤔"):
        text2 = st.markdown("In questa sezione potrai scoprire quali sono le keyword correlate più cercate su google<br> La sezione di <bold>Ricerca Keyword</bold> per la keyword inserita (MAX 1) genererà:<br>🔹Dalle tantissime keywords inerenti a quella data<br>🔹La distribuzione delle nuove keywords<br>🔹I 10 competitor più forti sulle keywords generate<br>", unsafe_allow_html=True)
        text3 = st.markdown("Per iniziare ti basterà :<br>1️⃣ Inserire la keyword (MAX 1)<br> 2️⃣ Clicca su <bold>'Svelami nuove keyword🤘'</bold> ", unsafe_allow_html=True)
    st.write("  ")
    st.write("  ")


    from suggests import (
        add_parent_nodes,
        suggests,
        to_edgelist,
        get_suggests_tree,
        add_metanodes,
    )

    import matplotlib as plt
    import seaborn as sns

    from pyecharts import options as opts
    from pyecharts.charts import Tree
    from streamlit_echarts import st_echarts


    def custom_get_google_url():
        # Retrieve language from session state, or set lang to 'en' by default
        lang = st.session_state.get("google_url_language", "it")
        # return f"https://www.google.com/complete/search?sclient=psy-ab&hl={lang}&q="
        return f"https://www.google.com/complete/search?sclient=psy-ab&gl={lang}&q="

    suggests.get_google_url = custom_get_google_url

    # region Top area ############################################################

    # endregion Top area ############################################################


    c1, c2, c3 = st.columns(3)
    SearchEngineLowerCase = ""
    with c1:
        keyword = st.text_input("Keyword", value="Marketing")

    with c2:
        if st.session_state.premium == True:
            SearchEngine = st.selectbox("Motore di Ricerca", ("Google", "Bing"))
            if SearchEngine == "Bing":
                SearchEngineLowerCase="bing"
            else:
                SearchEngineLowerCase="google"
        else:
            SearchEngine = st.selectbox("Google o Bing ? (PREMIUM 👑) ", ("Google", "Bing"), disabled=True)
            SearchEngineLowerCase="google"

   
    with c3:
        if st.session_state.premium == True:
            maxDepth = st.number_input(
                "Scegli la profondità massima di ricerca",
                min_value=1,
                max_value=3,
                value=1,
                step=1,
                key=None,
            )
        else:
            maxDepth = st.number_input(
                "Scegli la profondità di ricerca (PREMIUM 👑)",
                min_value=1,
                max_value=1,
                value=1,
                step=1,
                key=None,
                disabled=True,
            )
            maxDepth = 1


    c10, c11, c12 = st.columns(3)

    c = st.container()

    button1 = st.button("Cerca nuove suggerimenti 🤘") 

    if not keyword:
        c.success("🔼 Scrivi una keyword per iniziare")
        st.stop()

    if keyword and not button1:
        c.success("🔽 Clicca sul pulsante per cercare nuove suggerimenti")
        st.stop()

    # Patch suggests to support latin1 decoding
    def suggests_tree(*args, **kwargs):
        try:
            old_loads = json.loads

            def new_loads(s, *args, **kwargs):
                if isinstance(s, bytes):
                    s = s.decode("latin1")
                return old_loads(s, *args, **kwargs)

            json.loads = new_loads

            return get_suggests_tree(*args, **kwargs)

        finally:
            json.loads = old_loads

    with st.spinner("Stiamo HACKERANDO google e bing dacci qualche minuto ... 🤘 Potrebbero volerci diversi minuti 🙏"):
        # tree = suggests_tree("français", source="google", max_depth=1)
        tree = suggests_tree(keyword, source=SearchEngineLowerCase, max_depth=maxDepth)

        if maxDepth != 3:

            edges = to_edgelist(tree)
            edges = add_parent_nodes(edges)
            edges = edges.apply(add_metanodes, axis=1)
            show_restricted_colsFullDF = [
                "root",
                "edge",
                "rank",
                "depth",
                "search_engine",
                "datetime",
                "parent",
                "source_add",
                "target_add",
            ]
            edges = edges[show_restricted_colsFullDF]
            edges = edges.dropna()
            show_restricted_cols1level = ["source_add", "target_add"]
            show_restricted_cols2levels = ["parent", "source_add", "target_add"]

            if maxDepth == 2:
                dflimitedcolumns = edges[show_restricted_cols2levels]
                dfNoneRemoved = dflimitedcolumns.dropna()
            else:
                dflimitedcolumns = edges[show_restricted_cols1level]
                dfNoneRemoved = dflimitedcolumns.dropna()

            edges["datetime"] = pd.to_datetime(edges["datetime"])

            edges = edges.rename(
                {
                    "root": "Root Keyword",
                    "rank": "Rank",
                    #'depth': 'Depth',
                    "search_engine": "Search Engine",
                    "datetime": "Date & Time scraped",
                    "parent": "Level 01",
                    "source_add": "Level 02",
                    "target_add": "Level 03",
                },
                axis=1,
            )

            edges = edges[
                [
                    "Root Keyword",
                    "Level 01",
                    "Level 02",
                    "Level 03",
                    "Rank",
                    #'Depth',
                    "Search Engine",
                    "Date & Time scraped",
                ]
            ]


            class Node(object):
                def __init__(self, name, size=None):
                    self.name = name
                    self.children = []
                    self.size = size

                def child(self, cname, size=None):
                    child_found = [c for c in self.children if c.name == cname]
                    if not child_found:
                        _child = Node(cname, size)
                        self.children.append(_child)
                    else:
                        _child = child_found[0]
                    return _child

                def as_dict(self):
                    res = {"name": self.name}
                    if self.size is None:
                        res["children"] = [c.as_dict() for c in self.children]
                    else:
                        res["size"] = self.size
                    return res


            root = Node(keyword)

            if maxDepth == 2:
                for index, row in dfNoneRemoved.iterrows():
                    grp1, grp3, size = row
                    root.child(grp1).child(grp3, size)
            else:
                for index, row in dfNoneRemoved.iterrows():
                    grp3, size = row
                    root.child(grp3, size)

            jsonString = json.dumps(root.as_dict(), indent=4)
            jsonJSON = json.loads(jsonString)

            opts = {
                "tooltip": {"trigger": "item", "triggerOn": "mousemove"},
                "series": [
                    {
                        "type": "tree",
                        "data": [jsonJSON],
                        "top": "1%",
                        "left": "7%",
                        "bottom": "1%",
                        "right": "20%",
                        "symbolSize": 9,
                        "label": {
                            "position": "left",
                            "verticalAlign": "middle",
                            "align": "right",
                            "fontSize": 12,
                        },
                        "toolbox": {
                            "show": True,
                            "feature": {
                                "dataZoom": {"yAxisIndex": "none"},
                                "restore": {},
                                "saveAsImage": {},
                            },
                        },
                        "leaves": {
                            "label": {
                                "position": "right",
                                "verticalAlign": "middle",
                                "align": "left",
                            }
                        },
                        "expandAndCollapse": True,
                        "animationDuration": 550,
                        "animationDurationUpdate": 750,
                    }
                ],
            }

            st.markdown("---")

            st.markdown("## **🌳 Grafico ad albero INTERATTIVO**")

            with st.expander("ℹ️ - Come uso questo grafico ? "):

                st.write(
                    """       
            -  Clicca sul nodo per visualizzare i suggerimenti che lo contengono.
            -  Usa il tasto desto per savare il grafico come foto 📷
                    """
                )

            st.markdown("")

            st_echarts(opts, height=1000, width=1000)
            edges = edges.reset_index(drop=True)
            cm = sns.light_palette("green", as_cmap=True)
            edgescoloured = edges.style.background_gradient(cmap="Blues")

            st.markdown("---")


        try:

            if st.session_state.premium == True:
                st.markdown("##  Scarica ora i risultati 🎁 ")
                csv = edges.to_csv(index=False)
                st.download_button("Scarica ora i dati in formato csv", csv, "keyword_suggestions.csv")
            else:
                st.markdown("##  🎁 Scarica i risultati ")
                st.markdown("** Scarica ora i dati in formato csv (PREMIUM 👑) **")

        except NameError:
            print("Aspetta")

        st.markdown("---")
        st.markdown("## **👇 Ecco i suggerimenti generati**")
        st.subheader("")
        st.table(edgescoloured)

    c.success("✅ Complimenti! I suggerimenti sono pronti!")
    
    st.subheader("Competitor principali 🏈")
    import urllib
    import requests

    query = {
        "q": keyword,
        "cr": "IT",
        "num" : 10,
        "lr": "lang_it"

    }

    headers = {
        "X-User-Agent": "desktop",
        "X-Proxy-Location": "EU",
        "X-RapidAPI-Host": "google-search3.p.rapidapi.com",
        "X-RapidAPI-Key": "f889417d30msh0879bcc629fc0b3p1ff6ddjsnc676de2ea528"
    }
    resp = requests.get("https://rapidapi.p.rapidapi.com/api/v1/search/" + urllib.parse.urlencode(query), headers=headers)

    results = resp.json()
    #create dataframe
    concorrenti =  pd.DataFrame(columns=['Posizionamento su Google','Dominio', 'Titolo Indicizzato'])
    #st.write(results)
    i=1
    for result in results["results"]:
        title = result['title']
        link = result['link']
        
        subdomain= link.split("/")[2]
        #st.write(title,link)
        concorrenti.loc[i] = [i] + [subdomain] + [title] 
        i=i+1

    if st.session_state.premium == True:
        gb = GridOptionsBuilder.from_dataframe(concorrenti)
        gb.configure_default_column(editable=True)
        gb.configure_grid_options(enableRangeSelection=True)
        with st.spinner('Aspetta un attimo ... 🕐 Potrebbe volerci qualche minuto 🙏'):
            response = AgGrid(
                concorrenti,
                gridOptions=gb.build(),
                fit_columns_on_grid_load=True,
                allow_unsafe_jscode=True,
                enable_enterprise_modules=True
            )    
            st.write("Per esportare i dati, usa il tasto desto del mouse 🚀")
    else:
        concorrentiFree = pd.DataFrame(columns=['Posizionamento su Google','Dominio', 'Titolo Indicizzato'])
        concorrentiFree = concorrenti
        for index, row in concorrentiFree.iterrows():
            if index % 2 != 0:
                # write "Solo per PREMIUM 👑" only on "Dominio" column
                concorrentiFree.at[index, 'Dominio'] = "Solo per PREMIUM 👑"
                # write "Solo per PREMIUM 👑" only on "Titolo idicizzato" column
                concorrentiFree.at[index, 'Titolo Indicizzato'] = "Solo per PREMIUM 👑"

        gb = GridOptionsBuilder.from_dataframe(concorrentiFree)
        gb.configure_default_column(editable=True)
        gb.configure_grid_options(enableRangeSelection=True)
        with st.spinner('Aspetta un attimo ... 🕐 Potrebbe volerci qualche minuto 🙏'):
            response = AgGrid(
                concorrentiFree,
                gridOptions=gb.build(),
                fit_columns_on_grid_load=True,
                allow_unsafe_jscode=True
            )
            st.write("Per esportare i dati, passa a PREMIUM 🚀")
        

#3 Competitor principali 🏈
if choose=="Competitor":
    MAX_LINES = 1
    with st.expander("Cos'è e come funziona la sezione Competitor 🤔"):
        text2 = st.markdown("In questa sezione potrai scoprire quali sono i tuoi competitor più forti sulla seo<br> La sezione di <bold>Competitor</bold> per la keyword inserita (MAX 1) genererà:<br>🔹Lista dei competitor più forti<br>🔹Posizionamento per ogni competitor<br>🔹Link pagina indicizzata su Google<br>🔹Statistiche sul titolo e descrizione pagina indicizzata", unsafe_allow_html=True)
        text3 = st.markdown("Per iniziare ti basterà :<br>1️⃣ Inserire le keywords, una per riga<br> 2️⃣ Clicca su <bold>'Svelami i Competitor🤘'</bold> ", unsafe_allow_html=True)
    st.write("  ")
    st.write("  ")
    text = st.text_area("Powered by IntelligenzaArtificialeItalia.net", height=150, key=1)
    if st.button("Svelami i Competitor🤘"):
        if st.session_state.premium == True:
            MAX_LINES = 10
        else:
            MAX_LINES = 1

        lines = text.split("\n")  # A list of lines
        linesList = []
        for x in lines:
            linesList.append(x)
        linesList = list(dict.fromkeys(linesList))  # Remove dupes
        linesList = list(filter(None, linesList))  # Remove empty

        if len(linesList) > MAX_LINES:
            if st.session_state.premium == True:
                st.warning(f"⚠️ Attenzione, Puoi inserire al massima 10 keywords. ⚠️")
                linesList = linesList[:MAX_LINES]
            else:
                st.warning(f"⚠️ Attenzione, Puoi inserire al massima 1 keywords. ⚠️")
                linesList = linesList[:MAX_LINES]

            
        st.subheader("Competitor principali 🏈")
        import urllib
        import requests

        query = {
            "q": str(linesList),
            "num" : 25,
            "lr": "lang_it"
        }

        headers = {
            "X-User-Agent": "desktop",
            "X-Proxy-Location": "EU",
            "X-RapidAPI-Host": "google-search3.p.rapidapi.com",
            "X-RapidAPI-Key": "420c6c02f5msh1ef4b18dc0eb0fcp117e71jsn6fb5cadbc81a"
        }
        resp = requests.get("https://rapidapi.p.rapidapi.com/api/v1/search/" + urllib.parse.urlencode(query), headers=headers)

        results = resp.json()
        #create dataframe
        concorrenti =  pd.DataFrame(columns=['Posizionamento su Google','Dominio', 'Pagina indicizzata' ,'Titolo' , 'Lunghezza Titolo', 'Descrizione', 'Lunghezza Descrizione'])
        #st.write(results)
        i=1
        for result in results["results"]:
            title = result['title']
            link = result['link']
            descrizione = result['description']
            subdomain= link.split("/")[2]
            nT = len(title)
            nD = len(descrizione)
            #st.write(title,link)
            concorrenti.loc[i] = [i] + [subdomain] + [link] + [title] + [nT] + [descrizione] + [nD] 
            i=i+1

        if st.session_state.premium == True:
            gb = GridOptionsBuilder.from_dataframe(concorrenti)
            gb.configure_default_column(editable=True)
            gb.configure_grid_options(enableRangeSelection=True)
            with st.spinner('Aspetta un attimo ... 🕐 Potrebbe volerci qualche minuto 🙏 '):
                response = AgGrid(
                    concorrenti,
                    gridOptions=gb.build(),
                    fit_columns_on_grid_load=True,
                    allow_unsafe_jscode=True,
                    enable_enterprise_modules=True
                )   
                st.write("Per esportare i dati, usa il tasto desto del mouse 🚀")
        else:
            concorrentiFree = pd.DataFrame(columns=['Posizionamento su Google','Dominio', 'Pagina indicizzata' ,'Titolo' , 'Lunghezza Titolo', 'Descrizione', 'Lunghezza Descrizione'])
            concorrentiFree = concorrenti
            # write "Solo per PREMIUM 👑" on 'Lunghezza Titolo', 'Descrizione', 'Lunghezza Descrizione' columns 
            concorrentiFree['Lunghezza Titolo'] = "Solo per PREMIUM 👑"
            concorrentiFree['Descrizione'] = "Solo per PREMIUM 👑"
            concorrentiFree['Lunghezza Descrizione'] = "Solo per PREMIUM 👑"
            #write "Solo per PREMIUM 👑" only on 'Dominio', 'Pagina indicizzata' ,'Titolo' columns for frist 5 rows
            for index, row in concorrentiFree.head(5).iterrows():
                concorrentiFree.at[index, 'Dominio'] = "Solo per PREMIUM 👑"
                concorrentiFree.at[index, 'Pagina indicizzata'] = "Solo per PREMIUM 👑"
                concorrentiFree.at[index, 'Titolo'] = "Solo per PREMIUM 👑"

            gb = GridOptionsBuilder.from_dataframe(concorrentiFree)
            gb.configure_default_column(editable=True)
            gb.configure_grid_options(enableRangeSelection=True)
            with st.spinner('Aspetta un attimo ... 🕐 Potrebbe volerci qualche minuto 🙏 '):
                response = AgGrid(
                    concorrentiFree,
                    gridOptions=gb.build(),
                    fit_columns_on_grid_load=True,
                    allow_unsafe_jscode=True
                )   
                st.write("Per esportare i dati, passa a PREIUM 🚀")

        st.markdown("""<hr/><br>""", unsafe_allow_html=True)

#4 Domande
if choose=="Domande":
    MAX_LINES = 1
    with st.expander("Cos'è e come funziona la sezione Domande 🤔"):
        text2 = st.markdown("In questa sezione potrai scoprire quali sono i dubbi dei tuoi potenziali clienti in merito ad una keyword<br> La sezione <bold>Domande</bold> per la keyword inserita (MAX 1) genererà:<br>🔹Le domande più cercate su Google<br>🔹Una risposta semplice per ogni domanda generata<br>🔹Statistiche e informazioni per ogni domanda", unsafe_allow_html=True)
        text3 = st.markdown("Per iniziare ti basterà :<br>1️⃣ Inserire la keyword (MAX 1)<br> 2️⃣ Clicca su <bold>'Svelami i Dubbi🤘'</bold> ", unsafe_allow_html=True)
    
    st.write("  ")
    st.write("  ")
    text = st.text_area("Powered by IntelligenzaArtificialeItalia.net", height=150, key=1)
    if st.button("Svelami i Dubbi🤘"):
        lines = text.split("\n")  # A list of lines
        linesList = []
        for x in lines:
            linesList.append(x)
        linesList = list(dict.fromkeys(linesList))  # Remove dupes
        linesList = list(filter(None, linesList))  # Remove empty

        if len(linesList) > MAX_LINES:
            st.warning(f"⚠️ Attenzione, solo la prima keyword verrà analizzata")
            linesList = linesList[:MAX_LINES]
            
        st.subheader("Damande principali cercate sulla Keyword❓")
        with st.spinner("Stiamo intervistando personalmente Google e Bing per svelarti i sui dubbi dei clienti su questa keyword...❓ Potrebbero volerci diversi minuti 🙏"):
            domande = people_also_ask_it.get_related_questions(str(linesList),25)
            #st.write(domande)
            if(len(domande) <= 0):
                st.error("Nessuna domanda trovata, riprova con un altro termine 🤔 \n") 
            else:
                informazioni = []
                domandePulite = []
                for dom in domande:
                    domanda = dom.split("Cerca: ")
                    risposta = people_also_ask_it.get_answer(domanda[0]) 
                    #append risposta in informazioni
                    informazioni.append(risposta)
                    domandePulite.append(domanda[0])

                for i in range(len(domandePulite)):
                    if st.session_state.premium == True:
                        with st.expander(domandePulite[i]) :
                            st.write(informazioni[i])
                    else:
                        if i == 0:
                            with st.expander(domandePulite[i]) :
                                st.write(informazioni[i])
                        elif i%2 == 0:
                            with st.expander("Solo per PREMIUM 👑") :
                                st.write("Solo per PREMIUM 👑")
                        else:
                            with st.expander(domandePulite[i]) :
                                st.write("Solo per PREMIUM 👑")


#5 Contenuti
if choose=="Contenuti":
    with st.expander("Cos'è e come funziona la sezione Contenuti 🤔"):
        text2 = st.markdown("In questa sezione potrai generare articoli, testi e spiegazioni senza dover scrivere 😯<br> La sezione di <bold>Contenuti</bold> in base ad una frase o un paragrafo dato è in grado di aiutarti a scrivere grazie ad un Intelligenza artificiale che sono anni che apprende dal web🤯", unsafe_allow_html=True)
        text3 = st.markdown("Per iniziare ti basterà :<br>1️⃣ Inserire una frase o un paragrafo<br>2️⃣ Scegliere lunghezza desiderata del testo generato<br>3️⃣ Clicca su <bold>'Genera testo🤘'</bold> ", unsafe_allow_html=True)
    st.write("  ")
    st.write("  ")
    inp = st.text_area('Scrivi una frase o un paragrafo di ispirazione per la nostra I.A.',height=200)
    if st.session_state.premium == True:
        lunghezza = st.slider('Lunghezza massima del testo generato :', 50, 700,200,10)
        follia = st.slider('Numero di follia :', 0.5, 1.0,0.7,0.1)
        numTesti = st.slider('Numero di testi da generare :', 1, 5,1,1)
    else:
        lunghezza = st.slider('Lunghezza massima del testo generato ', 50, 700,200,10)
        follia = st.slider('Numero di follia (PREMIUM 👑)', 0.5, 1.0,0.7,0.1, disabled=True)
        follia = 0.7
        numTesti = st.slider('Numero di testi da generare (PREMIUM 👑)', 1, 5,1,1, disabled=True)
        numTesti = 1

    
    if st.button("Genera testo🤘") :
        nuovo = ittoen(inp)
        with st.spinner('Aspetta mentre rapiamo un COPYWRITER ... 🤖 Potrebbe volerci qualche minuto 🙏'):
            inp = ai_text(nuovo,lunghezza,follia,numTesti)
            for i in range(len(inp)):
                with st.expander(f"Genero il testo {str(i+1)}"):
                    st.write(inp[i])

                        

#Fine
st.text("")
st.text("")
st.text("")
st.text("")
st.text("")
st.text("")
st.text("")
st.text("")
st.write("Proprietà intellettuale di [Intelligenza Artificiale Italia © ](https://intelligenzaartificialeitalia.net)")
st.success("Questo è un tool gratuito sviluppato per Marketers, Esperti SEO, Coprywriters e Gestori di E-commerce 💣 .")
st.error("Al momento è basato sullo scraping dei dati da Google, NON ABUSARNE solo perchè è gratis, PASSA ORA A PREMIUM PER SBLOCCARE TUTTE LE FUNZIONI ! 🕹️ ")
st.markdown('<b> Se ti è stato di aiuto condividi il nostro sito per supportarci </b>\
       <ul> \
      <li><a href="https://www.facebook.com/sharer.php?u=http%3A%2F%2Fintelligenzaartificialeitalia.net%2F" target="blank" rel="noopener noreferrer">Condividi su Facebook</a></li> \
      <li><a href="https://twitter.com/intent/tweet?url=http%3A%2F%2Fintelligenzaartificialeitalia.net%2F&text=Blog%2C+Forum%2C+Progetti%2C+e+Servizi+Gratuiti+completamente+dedicati+all%27+Intelligenza+Artificiale." target="blank" rel="noopener noreferrer">Condividi su Twitter</a></li> \
      <li><a href="https://www.linkedin.com/shareArticle?mini=true&url=https%3A%2F%2Fwww.intelligenzaartificialeitalia.net%2F&title=IntelligenzaArtificialeItalia=Blog%2C+Forum%2C+Progetti%2C+e+Servizi+Gratuiti+completamente+dedicati+all%27+Intelligenza+Artificiale.&source=IntelligenzaArtificialeItalia" target="blank" rel="noopener noreferrer">Condividi su Linkedin</a></li>\
    </ul>', unsafe_allow_html=True)

