#Librerie
#Impostazioni pagina
import streamlit as st
st.set_page_config(layout="wide")
st.set_option('deprecation.showPyplotGlobalUse', False)
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;margin:0;}
    .css-18e3th9 { 
        flex: 1 1 0%; 
        width: 100%;
        padding: 1rem!important;
    }
    @media (min-width: 576px)
        .css-18e3th9 {
        padding: 0.5rem!important;
    }

    .st-c5 {
        font-weight: 300;
        font-size: medium;
    }

    .st-c5:hover {
        font-weight: 800;
        color: rgb(46, 170, 0);
    }

    .menu-title .icon[data-v-4323f8ce], .menu-title[data-v-4323f8ce] {
        font-size: 1.7rem;
        font-weight: 500;
    }

    .css-1cpxqw2{
        width: 100%;
        font-weight: 700;
    }
    .css-1cpxqw2:hover {
        font-weight: 800;
        border-color: rgb(46, 170, 0);
        color: rgb(46, 170, 0);
    }

    .css-1cpxqw2:active {
        color: rgb(255, 255, 255);
        border-color: rgb(46, 170, 0);
        background-color: rgb(46, 170, 0);
    }

    .css-1cpxqw2:focus {
        box-shadow: rgb(46 170 0 / 50%) 0px 0px 0px 0.2rem;
        outline: none;
    }

    .css-1cpxqw2:focus:not(:active) {
        border-color: rgb(46, 170, 0);
        color: rgb(46, 170, 0);
    }

    </style>

    """
st.markdown(hide_st_style, unsafe_allow_html=True)

import base64
import io
import json
import random
from time import sleep
from matplotlib import pyplot as plt
from openpyxl import Workbook
import pandas as pd
import seaborn as sns
from wordcloud import WordCloud
from streamlit_option_menu import option_menu
import streamlit.components.v1 as html
import people_also_ask_it
import urllib
import requests
from datetime import date
from pytrends.request import TrendReq
from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder, JsCode
import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

pid = 0
if 'pid' not in st.session_state:
    #generate random id
    pid = random.randint(1, 9999999)
    st.session_state['pid'] = pid
else:
    pid = st.session_state['pid']
    
try:

    ## GESTIONE UTENTI PREMIUM


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

    

    if 'primaVolta' not in st.session_state:
        st.session_state['primavolta'] = TrendReq()
        nltk.download('punkt')
        pytrends = st.session_state.primavolta
    else:
        pytrends = st.session_state.primavolta



    #####MENU
    if 'index' not in st.session_state:
        st.session_state['index'] =  0

    choose = option_menu("Intelligenza Artificiale e SEO 🤖", ["Analisi" , "Ricerca", "Domande" , "Competitor", "Testi", "Contenuti"],
                    icons=[ 'body-text', 'keyboard', 'patch-question' , 'exclamation-triangle', 'journal-bookmark'],
                    menu_icon="app-indicator", default_index=st.session_state.index ,orientation='horizontal',
                    styles={
    "container": {"color": "blak","padding": "0!important", "background-color": "transparent", "width": "100%"},
    "icon": {"color": "blak", "font-size": "13px", "margin":"0px"}, 
    "nav-link": {"color": "blak!important","font-size": "15px", "text-align": "left", "padding": "5px!important", "margin":"0px", "--hover-color": "#eee"},
    "nav-link-selected": {"color": "blak","background-color": "#02ab21"},
    }
    )

    if 'premium' not in st.session_state:
        #set session premium key to false
        st.session_state['premium'] =  False
    st.markdown("<div id='MainMenu'>", unsafe_allow_html=True)
    if st.session_state.premium == False:
        with st.expander("👑 Sei un UTENTE PREMIUM ? 👑"):
                st.markdown("<center><h5>Login Utenti Premium 👑</h5>", unsafe_allow_html=True)
                #define tree streamlit columns
                cc1, cc2= st.columns(2)
                user = cc1.text_input("Inserisci il tuo nome utente 👤")
                codice = cc2.text_input("Inserisci il tuo codice di accesso 🔑")
                dd1, dd2, dd3 = st.columns(3)
                if dd2.button("Accedi ora e sblocca funzionalità PREMIUM 🔐"):
                    if premium_check(user,codice):
                        st.success("Benvenuto "+user+" 👑 Tra poco questa sezione scomparirà 🤓") 
                    else:
                        st.error("Codice o Nome Utente errati ❌")
                st.write(" ")    
                st.markdown("<center><h4>Vuoi Diventare un Utente Premium 👑 ?</h4>", unsafe_allow_html=True)
                st.write(" ")
                st.markdown("<center><h5><a href='https://www.intelligenzaartificialeitalia.net/la-seo-con-intelligenza-artificiale-tool-gratuito' >Passa ORA a PREMIUM 👑 per SOLI 5€ , non te ne pentirai 🤓</a><h5>", unsafe_allow_html=True)
    else:
        st.success("Benvenuto "+st.session_state.nome+" 👑")
    st.markdown("</div>", unsafe_allow_html=True)


    if 'nome' not in st.session_state:
        st.session_state['nome'] =  ""
    
    #Funzioni di uso genrale

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
        st.session_state['index'] =  0
        with st.expander("Cos'è e come funziona la sezione Analisi 🤔"):
            text2 = st.markdown("<h4><b>Cosa puoi fare nella sezione Analisi ?</b></h4>In questa sezione potrai analizzare l'interesse nel tempo delle keyword e in quali regiorni del mercato selezionato ci sono più ricerche e quindi più interesse.<br> La sezione di <b>Analisi Keyword</b> per ogni keyword inserita il tool genererà:<br>🔹Il trend di ricerca nel tempo<br> 🔹Il trend di ricerca nelle regioni <br>🔹Top Trend correlati alla Keyword<br>🔹Tendenze in aumento correlate alla Keyword<br>🔹I competitor più forti sulla keyword<br>🔹Le domande più frequenti fatte sulla keyword <br>", unsafe_allow_html=True)
            st.markdown("<h4><b>Questa sezione ti permetterà di : </b></h4>🔸Confrontare interessi dei consumatori nel tempo di keyword, prodotti o servizi<br> \
                        🔸Sapere in quali regioni o città c'è più interesse<br>\
                        🔸Scoprire quali sono i trend più consolidati<br>\
                        🔸Trovare nuove tendenze più o meno correlate<br>\
                        🔸Scovare competitor e capire se il mercato è saturo<br>\
                        🔸Portare alla luce i dubbi dei consumatori<br>", unsafe_allow_html=True)
            text3 = st.markdown("<h4><b>Come funziona la seziona Analisi ? </b></h4>Per iniziare ti basterà :<br>1️⃣ Incollare le keywords, una per riga<br> 2️⃣ Scegliere il paese<br>3️⃣ Scegli il periodo di tempo<br>4️⃣Premere <b>'Scopri le tendenze🤘'</b> ", unsafe_allow_html=True)
            st.write("  ")
            st.write("  ")

        with st.form("my_form_analisi", clear_on_submit=False):
            #Inserimento Keyword    
            text = st.text_area("Inserisci le keywords, una per riga", height=150, key=1, help="""
            All'interno di questo campo puoi inserire le keywords mi raccomando una per riga.  
            ⚠️Gli utenti FREE possono inserire al massimo 3 Keywords.  
            👑Gli utenti PREMIUM possono inserire anche 10 Keywords.""")

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

            if st.session_state.premium == True:
                from parseCountries import parse
                country_names, country_codes = parse()
                country_names, country_codes = country_names[:243], country_codes[:243]
                country = st.selectbox("Scegli il paese", country_names, help="""Scegli in che paese/mercato vuoi analizzare le keywords inserite🤖.
                👑Gli utenti PREMIUM possono scegliere tra oltre 250 paesi.""" )
                st.write(f"Hai selezionato " + country)
                idx = country_names.index(country)
                country_code = country_codes[idx],
                #carico i periodi di tempo
                selected_timeframe = ""
                period_list = ["Ultimi 12 Mesi", "Ultima Ora", "Ultime 4 Ore", "Ultime 24 Ore", "Ultimi 7 Giorni", "Ultimi 30 Giorni", "Ultimi 90 Giorni", "Ultimi 5 Anni", "2004 - Oggi", "CUSTOM"]
                tf = ["today 12-m", "now 1-H", "now 4-H", "now 1-d", "now 7-d", "today 1-m", "today 3-m", "today 5-y", "all", "custom"]
                timeframe_selectbox = st.selectbox("Scegli il periodo", period_list, help="""Inserisci il periodo di tempo in cui vuoi analizzare le keywords inserite🤖.
                👑Gli utenti PREMIUM possono scegliere periodi CUSTOM per analisi impeccabili.""" )
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
                country_names, country_codes,idx = None, None, None
            else:
                country_code = ["IT", "EN"]
                country = st.selectbox("Scegli tra oltre 250 paesi con Premium 👑" , ["Italia", "Inglese"], disabled=True, help="""Scegli in che paese/mercato vuoi analizzare le keywords inserite🤖.  
                ⚠️Gli utenti FREE non possono scegliere.  
                👑Gli utenti PREMIUM possono scegliere tra oltre 250 paesi.""" )
                selected_timeframe = ""
                period_list = ["Ultimi 12 Mesi", "Ultima Ora", "Ultime 4 Ore", "Ultime 24 Ore", "Ultimi 7 Giorni", "Ultimi 30 Giorni", "Ultimi 90 Giorni", "Ultimi 5 Anni", "2004 - Oggi"]
                tf = ["today 12-m", "now 1-H", "now 4-H", "now 1-d", "now 7-d", "today 1-m", "today 3-m", "today 5-y", "all"]
                timeframe_selectbox = st.selectbox("Scegli periodi CUSTOM con Premium 👑", period_list, help="""Inserisci il periodo di tempo in cui vuoi analizzare le keywords inserite 🤖.  
                ⚠️Gli utenti FREE possono scegliere tra i periodi a disposizione.  
                👑Gli utenti PREMIUM possono scegliere periodi CUSTOM per analisi impeccabili.""" )
                idx = period_list.index(timeframe_selectbox)
                selected_timeframe = tf[idx]

            okVai = st.form_submit_button("🤘 ANALIZZAMI le TENDENZE 🤘")


        if okVai and len(linesList) > 0:

            
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
                try:
                    st.line_chart(temp)
                except:
                    st.warning("⚠️ Attenzione, riprova con altre keyword ⚠️")
                citta = pytrends.interest_by_region(resolution='CITY', inc_low_vol=False, inc_geo_code=False)
                
            
            for i in range(len(linesList)):
                keykey = linesList[i]
                st.header("Analisi della keyword {} : {}".format(i+1, str(linesList[i])))
                try:
                    st.line_chart(temp[str(linesList[i])])
                    st.bar_chart(citta[str(linesList[i])])
                except:
                    st.warning("Non ci sono dati per questa keyword 😢")
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
                            topTrendFree = None             
                    except:
                        st.warning("Non ci sono dati per questa keyword 😢")

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
                            topTrendenzeFree = None

                        
                    except:
                        st.warning("Non ci sono dati per questa keyword 😢")

                from ecommercetools import seo
                st.subheader("Competitor principali 🏈")

                query = {
                    "q": str(keykey),
                    "num" : 10,
                    "lr": "lang_" + country_code[0].lower()

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
                resp, results = None, None

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
                    concorrenti = None
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
                    concorrentiFree = None

                    
                st.write("")
                st.subheader("Domande principali ❓")
                with st.spinner('Stiamo HACKERANDO Google e Bing 🕐 Potrebbe volerci qualche minuto 🙏'):
                    domande = people_also_ask_it.get_related_questions(str(keykey), 10)
                if st.session_state.premium == True:
                    domandePremium = pd.DataFrame(columns=['Domanda'])
                    for dom in domande:
                        domanda = dom.split("Cerca: ")
                        domandePremium.loc[len(domandePremium)] = [domanda[1]]
                    with st.spinner('Stiamo HACKERANDO Google e Bing 🕐 Potrebbe volerci qualche minuto 🙏'):
                        response = AgGrid(
                            domandePremium,
                            fit_columns_on_grid_load=True,
                            allow_unsafe_jscode=True,
                            enable_enterprise_modules=True
                        )
                        st.write("Per esportare i dati, usa il tasto desto del mouse 🚀")
                    domandePremium = None
                else:
                    domandeFree = pd.DataFrame(columns=['Domanda'])
                    for dom in domande:
                        domanda = dom.split("Cerca: ")
                        domandeFree.loc[len(domandeFree)] = [domanda[1]]
                    #iterate domandeFree and write on "Domanda" column "Solo per PREMIUM" tranne per le prime 3 righe
                    for index, row in domandeFree.iterrows():
                        if index > 2:
                            domandeFree.at[index, "Domanda"] = "Solo per PREMIUM 👑"
                    with st.spinner('Stiamo HACKERANDO Google e Bing 🕐 Potrebbe volerci qualche minuto 🙏'):
                        response = AgGrid(
                            domandeFree,
                            fit_columns_on_grid_load=True,
                            allow_unsafe_jscode=True
                        )
                        st.write("Per esportare i dati, passa a Premium 🚀")
                    domandeFree = None

                domande = None
                st.markdown("""<hr/><br>""", unsafe_allow_html=True)
                
            st.balloons()
            st.stop()

    #2 Ricerca
    if choose=="Ricerca":
        st.session_state['index'] =  1
        MAX_LINES = 1
        with st.expander("Cos'è e come funziona la sezione Ricerca 🤔"):
            text2 = st.markdown("<h4><b>Cosa puoi fare nella sezione Ricerca ?</b></h4>La ricerca di parole chiave o Keyword Research è il primo passo di una qualunque strategia SEO ed è essenziale per capire quali e quanti contenuti ha senso creare, per cercare di posizionarti sugli argomenti di maggior interesse per il tuo business online. Sì, perché prima di lavorare sui contenuti del tuo sito web devi scoprire quali termini di ricerca vengono utilizzati dal tuo pubblico. Questi termini sono le tue parole chiave e, sulla base di quest’ultime, puoi iniziare a creare e pubblicare contenuti utili e di alta qualità.<br> La sezione di <b>Ricerca Keyword</b> per la keyword inserita genererà:<br>🔹Tantissime nuove keywords <br>🔹La ramificazione delle nuove keywords<br>🔹I 10 competitor più forti sulle keywords generate<br>", unsafe_allow_html=True)
            st.markdown("<h4><b>Questa sezione ti permetterà di : </b></h4>🔸Capire le nicchie della keyword, prodotto o servizo<br> \
                        🔸Saper identificare le tematiche più inerenti<br>\
                        🔸Scoprire i livelli difficoltà di posizionamento<br>\
                        🔸Trovare nuove tendenze più o meno correlate<br>\
                        🔸Creare piani editorali in 2 minuti<br>\
                        🔸Sviluppare una Content Strategy basata su dati", unsafe_allow_html=True)
            text3 = st.markdown("<h4><b>Come funziona la seziona Ricerca ? </b></h4>Per iniziare ti basterà :<br>1️⃣ Inserire la keyword <br>2️⃣ Scegliere il motore di ricerca<br>3️⃣Scegliere il <b>grado di profondità</b><br>4️⃣Premere <b>'Scopri le tendenze🤘'</b> ", unsafe_allow_html=True)
            st.markdown("<br><h5>🔧 Grado di profondità</h5>🧐 Livello 1 🧐 Genera dalle 50 alle 250 keywords<br>🤓 Livello 2 🤓 Genera dalle 250 alle 500 keywords<br><b>🤩 Livello 3 🤩 Genera dalle 500 alle 5000 Keywords</b>", unsafe_allow_html=True)
            st.write("  ")
            st.write("  ")
        st.write("  ")
        st.write("  ")


        from suggests import (
            add_parent_nodes,
            suggests,
            to_edgelist,
            get_suggests_tree,
            add_metanodes,
        )
        
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

        with st.form("my_form_Ricerca", clear_on_submit=False):
            c1, c2, c3 = st.columns(3)
            SearchEngineLowerCase = ""
            with c1:
                keyword = st.text_input("Inserisci la Keyword", help="Inserisci UNA SOLA keyword per scoprire Tutte le Keyword correlate")

            with c2:
                if st.session_state.premium == True:
                    SearchEngine = st.selectbox("Motore di Ricerca", ("Google", "Bing"),help="""Scegli quale motore di ricerca usare 🤖.  
                👑Gli utenti PREMIUM possono scegliere tra Google e Bing.""" )
                    if SearchEngine == "Bing":
                        SearchEngineLowerCase="bing"
                    else:
                        SearchEngineLowerCase="google"
                else:
                    SearchEngine = st.selectbox("Google o Bing ? (PREMIUM 👑) ", ("Google", "Bing"), disabled=True, help="""Scegli quale motore di ricerca usare 🤖.  
                ⚠️Gli utenti FREE non possono scegliere.  
                👑Gli utenti PREMIUM possono scegliere tra Google e Bing.""" )
                    SearchEngineLowerCase="google"

        
            with c3:
                if st.session_state.premium == True:
                    maxDepth = st.slider(
                        "Scegli la profondità massima di ricerca",
                        1,
                        3,
                        1,
                        1,
                        key=None,
                        help="""Scegli quale motore di ricerca usare 🤖.  
                ⚠️Gli utenti FREE non possono scegliere.  
                👑Gli utenti PREMIUM possono scegliere tra Google e Bing.""" )
                    
                else:
                    maxDepth = st.slider(
                        "Scegli la profondità di ricerca (PREMIUM 👑)",
                        1,
                        3,
                        1,
                        1,
                        key=None,
                        disabled=True,
                        help="""Scegli il livello di ricorsività da usare 🤖.  
                👑Gli utenti PREMIUM possono scegliere per ottenere fino a 5000 nuove keyword.""" )
                    
                    maxDepth = 1

            IniziaRicerca = st.form_submit_button("🤘 CERCAMI NUOVI SUGGERIMENTI 🤘")


        if IniziaRicerca  and len(keyword)>=1:
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

            with st.spinner("Stiamo HACKERANDO Google e Bing 🤘 Potrebbero volerci diversi minuti 🙏"):
                # tree = suggests_tree("français", source="google", max_depth=1)
                tree = suggests_tree(keyword, source=SearchEngineLowerCase, max_depth=maxDepth)

                if maxDepth < 6:

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
                                "bottom": "1%",
                                "left": "30%",
                                "right": "40%",
                                "padding": "0",
                                "symbolSize": 10,
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

                    st_echarts(opts, height=1000)
                    edges = edges.reset_index(drop=True)
                    cm = sns.light_palette("green", as_cmap=True)
                    edgescoloured = edges.style.background_gradient(cmap="Blues")

                    st.markdown("---")


                try:

                    if st.session_state.premium == True:
                        st.markdown("##  Scarica ora i risultati 🎁 ")
                        csv = edges.to_csv(index=False)
                        #create href to download csv file
                        b64 = base64.b64encode(csv.encode()).decode()
                        filename = f"{keyword}_{SearchEngineLowerCase}_suggestions.csv"
                        href = f'<a href="data:file/csv;base64,{b64}" download="{filename}">Scarica ora i risultati 🎁</a>'
                        st.markdown(href, unsafe_allow_html=True)

                    else:
                        st.markdown("###  🎁 Scarica i risultati (PREMIUM 👑) ")


                except NameError:
                    st.warning("Non ci sono risultati da scaricare 😞")

                st.markdown("---")
                st.markdown("## **👇 Ecco i suggerimenti generati**")
                st.subheader("")
                st.table(edgescoloured)
                tree, edges, edgescoloured, jsonString, jsonJSON, opts = None, None, None, None, None, None

            
            st.subheader("Competitor principali 🏈")

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
            resp, results = None, None

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
                concorrenti = None
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
                concorrentiFree = None

            st.balloons()
            st.stop()
        
            

    #3 Competitor principali 🏈
    if choose=="Competitor":
        st.session_state['index'] =  3
        MAX_LINES = 1
        with st.expander("Cos'è e come funziona la sezione Competitor 🤔"):
            text2 = st.markdown("<h4><b>Cosa puoi fare nella sezione Competitor ?</b></h4> La sezione <b>Competitor</b> ti aiuterà a identificare e rispondere alla domanda del tuo potenziale cliente su ogni pagina di prodotto in modo che possa posizionarsi più in alto nei motori di ricerca e fornire informazioni utili ai visitatori. Con questo strumento sarai in grado di creare una strategia di contenuti pertinente alle esigenze dei tuoi clienti. Avrai anche accesso a modelli con domande pre-scritte su prodotti o categorie specifici che possono far risparmiare tempo durante la creazione di nuove pagine.<br> La sezione di <b>Ricerca Keyword</b> per la keyword inserita genererà:<br>🔹Le domande più cercate su Google<br>🔹I competitor per ogni domanda generata<br>🔹Statistiche e informazioni per ogni domanda<br>", unsafe_allow_html=True)
            st.markdown("<h4><b>Questa sezione ti permetterà di : </b></h4>🔸Individuare le parole chiave che non sono state prese di mira dai concorrenti<br> \
                        🔸Ottenere intenzioni di ricerca long tail che non pensavi di utilizzare prima<br>\
                        🔸Scoprire nuove opportunità dai risultati dei tuoi concorrenti<br>\
                        🔸Scovare le strategie SEO dei tuoi concorrenti<br>\
                        🔸Trovare potenziali affiliati<br>\
                        🔸Aumentare il tuo traffico organico richiedendo backlink", unsafe_allow_html=True)
            text3 = st.markdown("<h4><b>Come funziona la seziona Competitor ? </b></h4>Per iniziare ti basterà :<br>1️⃣ Inserire le keywords, una per riga <br>2️⃣ Scegliere il mercato di riferimento<br>3️⃣ Premere <b>'Svelami Competitors🤘'</b> ", unsafe_allow_html=True)
            
        st.write("  ")
        st.write("  ")
        with st.form("my_form_Competitor", clear_on_submit=False):
            text = st.text_area("Inserisci la keyword, una per riga ", height=150, key=1 , help="""Inserisci le Keyword/Prodotti/Servizi uno per Riga di cui vuoi scovare i Competitor 🤖.  
                    ⚠️Gli utenti FREE possono inserire una keyword per volta .  
                    👑Gli utenti PREMIUM possono inserire anche 10 Keyword per volta""" )
            selected_lang = ""

            if st.session_state.premium == True:
                listLang = ["Italiano", "English", "German", "Spanish", "French", "Portuguese", "Russian", "Japanese", "Chinese", "Korean", "Arabic", "Polish", "Turkish", "Thai", "Vietnamese", "Indonesian", "Czech", "Dutch", "Greek", "Hindi", "Hungarian", "Norwegian", "Swedish", "Ukrainian", "Afrikaans", "Bengali", "Bulgarian", "Danish", "Finnish", "Filipino", "Georgian", "Hebrew", "Hmong", "Hungarian", "Kazakh", "Kyrgyz", "Latvian", "Lithuanian", "Malay", "Mongolian", "Myanmar", "Nepali", "Norwegian", "Pashto", "Persian", "Punjabi", "Romanian", "Serbian", "Somali", "Sotho", "Sundanese", "Tajik", "Tagalog", "Tamil", "Telugu", "Thai", "Turkish", "Uzbek", "Urdu", "Uighur", "Yiddish"]
                tfLang = ["lang_it", "lang_en", "lang_de", "lang_es", "lang_fr", "lang_pt", "lang_ru", "lang_ja", "lang_zh", "lang_ko", "lang_ar", "lang_pl", "lang_tr", "lang_th", "lang_vi", "lang_id", "lang_cs", "lang_nl", "lang_el", "lang_hi", "lang_hu", "lang_no", "lang_sv", "lang_uk", "lang_af", "lang_bn", "lang_bg", "lang_da", "lang_fi", "lang_fil", "lang_ka", "lang_gu", "lang_ht", "lang_ha", "lang_kn", "lang_kk", "lang_lv", "lang_lt", "lang_ms", "lang_mn", "lang_ne", "lang_ps", "lang_fa", "lang_pa", "lang_ro", "lang_sr", "lang_so", "lang_su", "lang_sd", "lang_tg", "lang_tl", "lang_ta", "lang_te", "lang_th", "lang_uz", "lang_ur", "lang_yi"]
                Lang_selectbox = st.selectbox("In che mercato vuoi cercare", listLang, help="""Inserisci in che Paese o Mercato vuoi cercare competitor 🤖.  
                    👑Gli utenti PREMIUM possono scegliere tra oltre 50 mercati""" )
                idxL = listLang.index(Lang_selectbox)
                selected_lang = tfLang[idxL]
            else:
                listLang = ["Italiano", "Inglese", "Spagnolo", "Francese", "Tedesco", "Portoghese", "Russo"]
                Lang_selectbox = st.selectbox("In che mercato vuoi cercare (PREMIUM 👑)", listLang, disabled=True , help="""Inserisci in che Paese o Mercato vuoi cercare competitor 🤖  
                    ⚠️Gli utenti FREE possono scegliere .  
                    👑Gli utenti PREMIUM possono scegliere tra oltre 50 mercati""" )
                selected_lang = "lang_it"

            IniziaCompetitor = st.form_submit_button("🤘 CERCAMI i COMPETIOR 🤘")

        if IniziaCompetitor and len(text) >= 1:
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

            
            for keyword in linesList:
                with st.spinner(f"Aspetta un attimo ... 🕐 Potrebbe volerci qualche minuto 🙏"):
                    st.subheader(f"Competitor principali {keyword}🏈 nel mercato {Lang_selectbox}")

                    query = {
                        "q": keyword,
                        "num" : 50,
                        "lr": selected_lang
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
                    resp, results = None, None

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
                        concorrenti = None
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
                        #write "Solo per PREMIUM 👑" only on 'Dominio', 'Pagina indicizzata' ,'Titolo' columns for last 10 rows
                        for index, row in concorrentiFree.tail(10).iterrows():
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
                        concorrentiFree = None

                    st.markdown("""<hr/><br>""", unsafe_allow_html=True)
            
            st.balloons()
            st.stop()

    #4 Domande
    if choose=="Domande":
        st.session_state['index'] =  2
        MAX_LINES = 1
        with st.expander("Cos'è e come funziona la sezione Domande 🤔"):
            text2 = st.markdown("<h4><b>Cosa puoi fare nella sezione Domande ?</b></h4> La sezione <b>Domande</b> ti aiuterà a identificare e rispondere alla domanda del tuo potenziale cliente su ogni pagina di prodotto in modo che possa posizionarsi più in alto nei motori di ricerca e fornire informazioni utili ai visitatori. Con questo strumento sarai in grado di creare una strategia di contenuti pertinente alle esigenze dei tuoi clienti. Avrai anche accesso a modelli con domande pre-scritte su prodotti o categorie specifici che possono far risparmiare tempo durante la creazione di nuove pagine.<br> La sezione di <b>Ricerca Keyword</b> per la keyword inserita genererà:<br>🔹Le domande più cercate su Google<br>🔹I competitor per ogni domanda generata<br>🔹Statistiche e informazioni per ogni domanda<br>", unsafe_allow_html=True)
            st.markdown("<h4><b>Questa sezione ti permetterà di : </b></h4>🔸Capire le principali domande e preoccupazioni dei tuoi clienti<br> \
                        🔸Ottenere intenzioni di ricerca long tail<br>\
                        🔸Scoprire nuovi argomenti secondari che contano<br>\
                        🔸Trovare migliaia di intenzioni di ricerca<br>\
                        🔸Trovare potenziali affiliati<br>\
                        🔸Sviluppare una Content Strategy basata su dati", unsafe_allow_html=True)
            text3 = st.markdown("<h4><b>Come funziona la seziona Ricerca ? </b></h4>Per iniziare ti basterà :<br>1️⃣ Inserire la keyword <br>2️⃣ Scegliere il numero di domande<br>3️⃣ Premere <b>'Svelami i Dubbi🤘'</b><br><br>", unsafe_allow_html=True)
            
        st.write("  ")
        with st.form("my_form_Domande", clear_on_submit=False):
            v1,v2 = st.columns(2)
            text = v1.text_input("Inserisci la keyword", help="""Inserisci la Keyword/Prodotto/Servizo di cui vuoi conoscere i dubbi dei clienti 🤖.  
                        ⚠️Gli utenti FREE NON possono ricevere più di 8 domande.  
                        ⚠️Gli utenti FREE NON possono ricevere le informazioni sulla domanda.  
                        👑Gli utenti PREMIUM possono ricevere fino a 25 domande per keyword.  
                        👑Gli utenti PREMIUM possono ricevere le informazioni sulla domanda.  """ )
            numeroDomande= 0
            if st.session_state.premium == True:
                numeroDomande = v2.slider("Quante domande vuoi che cerchiamo 🤔 ", 1, 25, 10, 1, help="Scegli il numero di domande che vuoi che cerchiamo 🤔.")
            else:
                numeroDomande = v2.slider("Cerca fino a 25 domande con PREMIUM 👑", 1, 8, 5, 1, help="Scegli il numero di domande che vuoi che cerchiamo 🤔.")
                numeroDomande+=2
            IniziaDomande = st.form_submit_button("🤘 CERCAMI DUBBI e DOMANDE 🤘")


        if IniziaDomande and len(text)>0:
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
            with st.spinner("Stiamo intervistando personalmente Google e Bing❓ Potrebbero volerci diversi minuti 🙏"):
                domande = people_also_ask_it.get_related_questions(str(linesList),numeroDomande)
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

                    domande, informazioni, domandePulite = None, None, None

                st.balloons()
                st.stop()


    #5 Contenuti
    if choose=="Contenuti":
        st.session_state['index'] =  5

        with st.expander("Cos'è e come funziona la sezione Contenuti 🤔"):

            text2 = st.markdown("<h4><b>Cosa puoi fare nella sezione Contenuti ?</b></h4>Non sai cosa dire nella didascalia di Instagram o nell'introduzione del post sul blog? Genera testi di marketing, annunci social, scrittura di blog, slogan, contenuti di siti Web e altro in pochi secondi con uno strumento gratuito per la scrittura di intelligenza artificiale. Accedi gratuitamente a un generatore di scrittura IA istantaneo, all'espansore di frasi e a un generatore di testo IA con il nostro scrittore di contenuti AI all-in-one. Non perdere un secondo a fissare uno schermo vuoto. Un'intelligenza artificiale efficace, sul pezzo e gratis è a portata di clic.<br> La sezione di <b>Genera Contenuti</b> per il paragrafo genererà:<br>🔹Diversi testi scritti da un I.A.<br>", unsafe_allow_html=True)
            st.markdown("<h4><b>Questa sezione ti permetterà di : </b></h4>🔸Non perdere un secondo quando ti manca l'ispirazione<br> \
                        🔸Generare titoli efficaci per il tuo blog post<br>\
                        🔸Generare indici e sommari per il tuo post<br>\
                        🔸Riempi facilmente le lacune nei tuoi contenuti<br>\
                        🔸Non pensare alla grammatica ma solo alla semantica<br>\
                        🔸Aumentare il tuo traffico producendo più contenuti rispetto ai competitor", unsafe_allow_html=True)
            text3 = st.markdown("<h4><b>Come funziona la seziona Contenuti ? </b></h4>Per iniziare ti basterà :<br>1️⃣ Inserire una frase o un paragrafo<br>2️⃣Scegliere lunghezza desiderata del testo generato<br>3️⃣Cliccare su <bold>'Genera testo🤘'</bold> ", unsafe_allow_html=True)

        if st.session_state.premium == True:
            st.markdown("### [Clicca qui per accedere alla sezione Genera Contenuti](https://www.intelligenzaartificialeitalia.net/generatesticonia)")
        else:
            st.markdown("### Questa sezione è disponibile solo per utenti PREMIUM 🤗")
        
        

    if choose == "Testi":
        st.session_state['index'] =  4
        from keybert import KeyBERT
        # For Flair (Keybert)
        from flair.embeddings import TransformerDocumentEmbeddings
        with st.expander("Cos'è e come funziona la sezione Testi 🤔", expanded=False):

            st.write(
                """   
            In questa sezione potrai controllare i tuoi testi per verificare che contengano le giuste parole chiave. 
            Una cosa è sicura, questo è l'inico tool che ti permetterà di riuscire a scrivere articoli per indicizzarti primo nei motori di ricerca. 
    
        Per sfruttare al meglio questa sezione, dovrai :
        - 1️⃣ Decidere delle parole chiave per cui ti vuoi indicizzare
        - 2️⃣ Scrivere un Testo o generarlo automaticamente nella sezione *Contenuti*
        - 3️⃣ Incollare all'interno di questa sezione il testo che vuoi indicizzare
        - 4️⃣ Cliccare su *'Analizza il mio testo 🤖'*
        - 5️⃣ Controllare che la keyword per cui ti vuoi indicizzare abbia un alta *Rilevanza*
                """
            )

            st.markdown("")

        st.markdown("")

        st.markdown("#### 📌 Incolla qui sotto il testo che vuoi indicizzare 📌")


        with st.form(key="my_form", clear_on_submit=False):

            c1, c2= st.columns([2,3])
            with c1:
                # Model type
                if st.session_state.premium == True:
                    ModelType = st.radio(
                        "Scegli il modello che vuoi usare",
                        ["DistilBERT (Default)", "Flair"]
                    )
                else:
                    ModelType = st.radio(
                        "Passa a PREMIUM 👑 per usare il modello più potente",
                        ["DistilBERT (Default)", "Flair"],
                        disabled=True
                    )
                    ModelType = "DistilBERT (Default)"


                if ModelType == "Default (DistilBERT)":

                    @st.cache(allow_output_mutation=True)
                    def load_model():
                        return KeyBERT(model=roberta)

                    kw_model = load_model()

                else:

                    @st.cache(allow_output_mutation=True)
                    def load_model():
                        return KeyBERT("distilbert-base-nli-mean-tokens")

                    kw_model = load_model()

                if st.session_state.premium == True:
                    top_N = st.slider(
                        "Numero di keywords da visualizzare",
                        min_value=1,
                        max_value=30,
                        value=10,
                        help="Puoi scegliere il numero di parole chiave/frasi chiave da visualizzare. Tra 1 e 30, il numero predefinito è 10.",
                    )
                    min_Ngrams = st.number_input(
                        "Numero minimo di parole chiave",
                        min_value=1,
                        max_value=4,
                        help="""Il valore minimo per l'intervallo di ngram.  
            Se vuoi indicizzarti sulla parola ' marketing ' dovrai impostare il valore minimo e il massimo a 1.""",
                    )

                    max_Ngrams = st.number_input(
                        "Numero massimo di parole chiave",
                        value=2,
                        min_value=1,
                        max_value=4,
                        help="""Il valore massimo per keyphrase_ngram_range.  
            Se vuoi indicizzarti sulla parola 'strategie marketing ' dovrai impostare il valore minimo e il massimo a 2.  
            Se vuoi indicizzarti sulla parola 'strategie marketing digitale' dovrai impostare il valore minimo e il massimo a 3.""",
                    )

                    StopWordsCheckbox = st.checkbox(
                        "Rimuovi le stop words",
                        help="Spunta questa casella per rimuovere le parole non significative dal documento (attualmente solo in italiano)",
                    )

                    use_MMR = st.checkbox(
                        "Usa MMR",
                        value=True,
                        help="È possibile utilizzare la rilevanza del margine massimo (MMR) per diversificare i risultati.  Crea parole chiave/frasi chiave basate sulla somiglianza del coseno.  Prova le impostazioni 'Diversità' alta/bassa di seguito per variazioni interessanti."
                    )

                    Diversity = 0.5
                    if use_MMR == True:
                        Diversity = st.slider(
                            "Diversità keyword",
                            value=0.5,
                            min_value=0.0,
                            max_value=1.0,
                            step=0.1,
                            help="""Maggiore è il valore MMR, più diverse saranno le parole chiave."""
                        )
                else:
                    top_N = st.slider(
                        "Numero di keywords da visualizzare disponibile in PREMIUM 👑",
                        min_value=1,
                        max_value=30,
                        value=10,
                        help="Puoi scegliere il numero di parole chiave/frasi chiave da visualizzare. Tra 1 e 30, il numero predefinito è 10.",
                        disabled=True
                    )
                    top_N = 10
                    min_Ngrams = st.number_input(
                        "Minimum Ngram disponibile in PREMIUM 👑",
                        min_value=1,
                        max_value=4,
                        help="""Il valore minimo per l'intervallo di ngram.  
            Se vuoi indicizzarti sulla parola ' marketing ' dovrai impostare il valore minimo e il massimo a 1.""",
                        disabled=True
                    )
                    min_Ngrams = 1
                    max_Ngrams = st.number_input(
                        "Maximum Ngram disponibile in PREMIUM 👑",
                        value=2,
                        min_value=1,
                        max_value=4,
                        help="""Il valore massimo per keyphrase_ngram_range.  
            Se vuoi indicizzarti sulla parola 'strategie marketing ' dovrai impostare il valore minimo e il massimo a 2.  
            Se vuoi indicizzarti sulla parola 'strategie marketing digitale' dovrai impostare il valore minimo e il massimo a 3.""",
                        disabled=True
                    )
                    max_Ngrams = 2
                    StopWordsCheckbox = st.checkbox(
                        "Rimuovi le stop words disponibile in PREMIUM 👑",
                        help="Spunta questa casella per rimuovere le parole non significative dal documento (attualmente solo in italiano)",
                        disabled=True
                    )
                    StopWordsCheckbox = False
                    use_MMR = st.checkbox(
                        "Usa MMR disponibile in PREMIUM 👑",
                        value=True,
                        help="È possibile utilizzare la rilevanza del margine massimo (MMR) per diversificare i risultati.  Crea parole chiave/frasi chiave basate sulla somiglianza del coseno.  Prova le impostazioni 'Diversità' alta/bassa di seguito per variazioni interessanti.",
                        disabled=True
                    )
                    use_MMR = True

                    Diversity = st.slider(
                        "Diversità keyword disponibile in PREMIUM 👑",
                        value=0.5,
                        min_value=0.0,
                        max_value=1.0,
                        step=0.1,
                        help="""Maggiore è il valore MMR, più diverse saranno le parole chiave.""",
                        disabled=True
                    )
                    Diversity = 0.5

            with c2:
                MAX_WORDS = 500
                if st.session_state.premium == True:
                    testoDaIncollare = "Incolla quì il testo da analizza (max 2000 words)"
                    MAX_WORDS = 2000
                else:
                    testoDaIncollare = "Passa a PREMIUM 👑 per incollare testii da oltre 2000 parole (max 500 words)"

                doc = st.text_area(
                    testoDaIncollare,
                    height=510,
                )
                import re
                res = len(re.findall(r"\w+", doc))
                if res > MAX_WORDS:
                    st.warning(
                        "⚠️ Attenzione il testo contiene più di "
                        + str(res)
                        + " parole."
                        + " Sole una parte sarà analizzata! 😊"
                    )

                    doc = doc[:MAX_WORDS]
            streamlit_button = st.form_submit_button(label="🤖 ANALIZZAMI IL TESTO 🤖")

            if use_MMR:
                mmr = True
            else:
                mmr = False

            if StopWordsCheckbox:
                StopWords = None
            else:
                StopWords = None

        if min_Ngrams > max_Ngrams:
            st.warning("min_Ngrams non può essere maggiore di max_Ngrams")


        if  streamlit_button is True and doc is not None and len(doc)> 3:
            keywords = kw_model.extract_keywords(
                doc,
                keyphrase_ngram_range=(min_Ngrams, max_Ngrams),
                use_mmr=mmr,
                stop_words=StopWords,
                top_n=top_N,
                diversity=Diversity,
            )

            st.markdown("## 🎈 Ecco la rilevanza delle parole chiave e frasi:")
            st.header("")

            df = (
                pd.DataFrame(keywords, columns=["Keyword/Frase", "Rilevanza"])
                .sort_values(by="Rilevanza", ascending=False)
                .reset_index(drop=True)
            )
            if st.session_state.premium == True:
                dfTemKey = df.copy()
                csv = df.to_csv(index=False)
                b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
                href = f'<a href="data:file/csv;base64,{b64} download="keywords.csv">Scarica il file CSV </a>'
                st.markdown(href, unsafe_allow_html=True)
            else:
                st.markdown("#### Passa a PREMIUM 👑 per scaricare il file CSV")

            df.index += 1

            # Add Styling to the table columns and rows

            cmGreen = sns.light_palette("green", as_cmap=True)
            cmRed = sns.light_palette("red", as_cmap=True)
            df = df.style.background_gradient(
                cmap=cmGreen,
                subset=[
                    "Rilevanza",
                ],
            )

            format_dictionary = {
                "Rilevanza": "{:.1%}",
            }

            df = df.format(format_dictionary)

            st.table(df)  
            

            #create wordcloud of df["Keyword/Frase"]
            st.subheader("🎈 Ecco la wordcloud delle parole chiave:")
            st.markdown("")
            wordcloud = WordCloud(
                width=800,
                height=400,
                background_color="white",
                max_words=100,
                stopwords=StopWords,
                max_font_size=200,
                random_state=42,
                colormap="RdBu_r",
            ).generate(" ".join(dfTemKey["Keyword/Frase"]))
            #plot wordcloud use fig
            fig = plt.figure(figsize=(10, 10))
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.axis("off")
            st.pyplot(fig)

            st.balloons()
            st.stop()

except Exception as e:
    st.warning(e)
    st.warning("⚠️ Attenzione, qualcosa è andato storto. 😱 chiudi e riapri il programma 😊")
    


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
st.success("Questo è un tool gratuito sviluppato per Marketers, Esperti SEO e Coprywriters💣 .")
st.error("Al momento è basato sullo scraping dei dati da Google, NON ABUSARNE solo perchè è gratis, PASSA ORA A PREMIUM PER SBLOCCARE TUTTE LE FUNZIONI ! 🕹️ ")
st.markdown('<b> Se ti è stato di aiuto condividi il nostro sito per supportarci </b>\
       <ul> \
      <li><a href="https://www.facebook.com/sharer.php?u=http%3A%2F%2Fintelligenzaartificialeitalia.net%2F" target="blank" rel="noopener noreferrer">Condividi su Facebook</a></li> \
      <li><a href="https://twitter.com/intent/tweet?url=http%3A%2F%2Fintelligenzaartificialeitalia.net%2F&text=Blog%2C+Forum%2C+Progetti%2C+e+Servizi+Gratuiti+completamente+dedicati+all%27+Intelligenza+Artificiale." target="blank" rel="noopener noreferrer">Condividi su Twitter</a></li> \
      <li><a href="https://www.linkedin.com/shareArticle?mini=true&url=https%3A%2F%2Fwww.intelligenzaartificialeitalia.net%2F&title=IntelligenzaArtificialeItalia=Blog%2C+Forum%2C+Progetti%2C+e+Servizi+Gratuiti+completamente+dedicati+all%27+Intelligenza+Artificiale.&source=IntelligenzaArtificialeItalia" target="blank" rel="noopener noreferrer">Condividi su Linkedin</a></li>\
    </ul>', unsafe_allow_html=True)

