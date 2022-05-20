#Librerie
#Impostazioni pagina
import random
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
        st.session_state.premium = False
        st.session_state.nome = user
        return True
    else:
        #set session premium key to false
        st.session_state.premium = True
        return False


try:
    from deep_translator import GoogleTranslator
    from aitextgen import aitextgen
    from streamlit_option_menu import option_menu

    @st.cache(allow_output_mutation=True, show_spinner=False)
    def traduttore(testo, lingua_traduzione):
        try:
            testo_tradotto = GoogleTranslator(source='auto', target=lingua_traduzione).translate(testo)
            return testo_tradotto
        except:
            return 'Traduction Error :('

    #Funzioni di uso genrale
    @st.cache(allow_output_mutation=True, show_spinner=False)
    def load_text_gen_model():
        a = aitextgen()
        return a

    @st.cache(show_spinner=False)
    def ai_text(inp,lunghezza, temp, num):
        listaTesti = []
        try:
            ai = load_text_gen_model()
            for i in range(num):
                generated_text = ai.generate_one(max_length = lunghezza, prompt = inp, no_repeat_ngram_size = random.randint(3, 5) , temperature = temp)
                listaTesti.append(generated_text)
            ai = None
            return listaTesti
        except:
            return ["Error","Try again"]
    

    listLang = ["Italiano", "English", "German", "Spanish", "French", "Portuguese", "Russian", "Japanese", "Chinese", "Korean", "Arabic", "Polish", "Turkish", "Thai", "Vietnamese", "Indonesian", "Czech", "Dutch", "Greek", "Hindi", "Hungarian", "Norwegian", "Swedish", "Ukrainian", "Afrikaans", "Bengali", "Bulgarian", "Danish", "Finnish", "Filipino", "Georgian", "Hebrew", "Hmong", "Hungarian", "Kazakh", "Kyrgyz", "Latvian", "Lithuanian", "Malay", "Mongolian", "Myanmar", "Nepali", "Norwegian", "Pashto", "Persian", "Punjabi", "Romanian", "Serbian", "Somali", "Sotho", "Sundanese", "Tajik", "Tagalog", "Tamil", "Telugu", "Thai", "Turkish", "Uzbek", "Urdu", "Uighur", "Yiddish"]
    tfLang = ["it", "en", "de", "es", "fr", "pt", "ru", "ja", "zh", "ko", "ar", "pl", "tr", "th", "vi", "id", "cs", "nl", "el", "hi", "no", "sv", "uk", "af", "bn", "bg", "da", "fi", "fil", "ka", "kk", "lv", "lt", "ms", "mn", "ne", "nb", "ps", "fa", "fa", "ro", "sr", "so", "su", "tg", "tl", "ta", "te", "th", "tk", "uz", "ur", "ug", "yi"]
    Lang_selectbox = st.selectbox("Select your language ✈️", listLang)
    idxL = listLang.index(Lang_selectbox)
    selected_lang = tfLang[idxL]

    choose = option_menu(traduttore("Intelligenza Artificiale e SEO 🤖", selected_lang), [traduttore("Genera Contenuti", selected_lang),traduttore("Esempi e Tutorial", selected_lang)],
                    icons=['keyboard','exclamation-triangle'],
                    menu_icon="app-indicator", default_index=0 ,orientation='horizontal',
                    styles={
    "container": {"color": "blak","padding": "0!important", "background-color": "transparent", "width": "100%"},
    "icon": {"color": "blak", "font-size": "13px", "margin":"0px"}, 
    "nav-link": {"color": "blak!important","font-size": "15px", "text-align": "left", "padding": "5px!important", "margin":"0px", "--hover-color": "#eee"},
    "nav-link-selected": {"color": "blak","background-color": "#02ab21"},
    }
    )

    if 'premium' not in st.session_state:
        #set session premium key to false
        st.session_state['premium'] =  True

    if 'nome' not in st.session_state:
            st.session_state['nome'] =  ""
            
    if st.session_state.premium == True:
        with st.expander(traduttore("👑 Accedi con le credenziali premium per sbloccare il generatore di testi 👑", selected_lang)):
                st.markdown("<center><h5>"+traduttore("Login Utenti Premium 👑",selected_lang)+"</h5>", unsafe_allow_html=True)
                #define tree streamlit columns
                cc1, cc2= st.columns(2)
                user = cc1.text_input(traduttore("Inserisci il tuo nome utente 👤",selected_lang))
                codice = cc2.text_input(traduttore("Inserisci il tuo codice di accesso 🔑",selected_lang))
                dd1, dd2, dd3 = st.columns(3)
                if dd2.button(traduttore("Accedi ora e sblocca funzionalità PREMIUM 🔐",selected_lang)):
                    if premium_check(user,codice):
                        st.success(traduttore("Benvenuto "+user+" 👑 Tra poco questa sezione scomparirà 🤓",selected_lang)) 
                    else:
                        st.error(traduttore("Codice o Nome Utente errati ❌",selected_lang))
                st.write(" ")    
                st.markdown("<center><h4>"+traduttore("Vuoi Diventare un Utente Premium 👑 ?",selected_lang)+"</h4>", unsafe_allow_html=True)
                st.write(" ")
                st.markdown("<center><h5><a href='https://www.intelligenzaartificialeitalia.net/la-seo-con-intelligenza-artificiale-tool-gratuito' >"+traduttore("Passa ORA a PREMIUM 👑 per SOLI 5€ , non te ne pentirai 🤓", selected_lang)+"</a><h5>", unsafe_allow_html=True)
    else:
        st.success(traduttore("Benvenuto  ",selected_lang)+st.session_state.nome+" 👑")

    if choose == "Genera Contenuti":
        with st.form("Genera Contenuti", clear_on_submit=False):
            inp = st.text_area(traduttore('Scrivi una frase o un paragrafo di ispirazione per la nostra Inteligenza Artificiale', selected_lang),height=200,disabled=st.session_state.premium)
            c1, c2, c3 = st.columns(3)
            lunghezza = c1.slider(traduttore('Lunghezza massima del testo generato :', selected_lang), 50, 700,200,10,disabled=st.session_state.premium)
            follia = c2.slider(traduttore('Imposta la "follia" del testo  :', selected_lang), 0.5, 1.0,0.6,0.1,disabled=st.session_state.premium)
            numTesti = c3.slider(traduttore('Numero di testi da generare :', selected_lang), 1, 5,1,1,disabled=st.session_state.premium)
            VaiGenera= st.form_submit_button(traduttore("🤘 GENERAMI i TESTI 🤘", selected_lang)) 

        try:
            if VaiGenera and len(inp)>3:
                nuovo = traduttore(inp,"en")
                try:
                    ai = load_text_gen_model()
                    with st.spinner(traduttore('Aspetta mentre rapiamo un COPYWRITER ... 🤖 Potrebbe volerci qualche minuto 🙏', selected_lang)):
                        inp = ai_text(nuovo,lunghezza,follia,numTesti)
                        ai = None
                        for i in range(len(inp)):
                            with st.expander(f"Genero il testo {str(i+1)}"):
                                st.write(traduttore(inp[i],selected_lang))
                        inp = None  
                except:
                    st.error(traduttore("Il COPYWRITER è riuscito a scappare, riprova 🤔", selected_lang))
        except Exception as e:
            st.error(e)
        finally:
            st.stop()
    else:
        st.markdown("<center><h4>" + traduttore("🤖 Esempi e Tutorial 🤖", selected_lang) +"</h4>", unsafe_allow_html=True)
        st.markdown(traduttore("All'interno di questa sezione troverai tutte le guide necessarie per generare Contenuti sfruttando al meglio la nostra Inteligenza Artificiale 🤖", selected_lang), unsafe_allow_html=False)
        
        with st.expander(traduttore("1🤖 Come generare Titoli efficaci per i post del tuo Blog 🚀", selected_lang)):
            st.subheader(traduttore("Esempio 🚀", selected_lang))
            st.markdown(traduttore(""" Per generare dei titoli efficaci ti basterà fornire all'intelligenza Artificiale un paio di esempi, lasciando poi a lei il compito di consigliarti altri titoli.<br>
            Ad esempio se copi e incolli questo testo : <br><br><b>
            titoli di articoli che parla di digital marketing : <br>
                1) Cosa è il digital Marketing la guida completa <br>
                2) Introduzione al Digital Marketing <br>
                3) <br>
            </b><br>
            e poi premi il bottone <b> '🤘 GENERAMI i TESTI 🤘' <br>
            Vedrai che l'Inteligenza Artificiale ti consiglierà una serie di titoli che potrebbero essere utili per il tuo Blog, Ebook o Libro📚.</b><br>
            ⚙️ IMPOSTAZIONI CONSIGLIATE :<br>
            ⚙️⚙️ Lunghezza massima del testo generato : 200<br>
            ⚙️⚙️ Imposta la "follia" del testo : 0.50 / 0.60<br>""", selected_lang), unsafe_allow_html=True)
        
        with st.expander(traduttore("3🤖 Come generare l'introduzione al tuo Blog post, Ebook o Libro📚  🚀", selected_lang)):
            st.subheader(traduttore("Esempio 🚀", selected_lang))
            st.markdown(traduttore(""" Supponiamo che dopo aver generato il titolo del tuo Articolo ti serva un Introduzione<br>
            Facciamo finta che prima l'intelligenza artificiale ti ha suggerito come titolo <b>'Che cos'è la pubblicità digitale?'</b> : <br>
            A questo punto ti basterà incollare un testo simile a questo per generare l'intruzione :<br><b><br>
            Che cos'è la pubblicità digitale?<br>
            <br>
            In questo articolo vedremmo nel dettaglio cosa è la pubblicità digitale.<br>
            Introduzione sulla pubblicità digitale:<br>
            </b><br>
            e poi premi il bottone <b> '🤘 GENERAMI i TESTI 🤘' <br>
            Vedrai che l'Inteligenza Artificiale ti consiglierà le migliori Introduzioni che potrebbero essere utili per il tuo Blog, Ebook o Libro📚.</b><br>
            ⚙️ IMPOSTAZIONI CONSIGLIATE :<br>
            ⚙️⚙️ Lunghezza massima del testo generato : 300 / 400 <br>
            ⚙️⚙️ Imposta la "follia" del testo : 0.50 / 0.70<br>""", selected_lang), unsafe_allow_html=True)

        with st.expander(traduttore("3🤖 Come generare l'indice o sommario del tuo Blog post, Ebook o Libro📚  🚀", selected_lang)):
            st.subheader(traduttore("Esempio 🚀", selected_lang))
            st.markdown(traduttore(""" Supponiamo che dopo aver generato una breve descrizione del nostro Articolo non abbiamo più idee. Quindi chiederemo all'intelligenza artificiale di generare un sommario per il nostro articolo<br>
            A questo punto ti basterà incollare un testo simile a questo per generare un sommario o indice : <br><br><b>
            Che cos'è la pubblicità digitale?<br>
            In questo articolo vedremmo nel dettaglio cosa è la pubblicità digitale.<br>
            <br>
            Introduzione sulla pubblicità digitale:
            La pubblicità digitale è l'uso di contenuti digitali, notizie, immagini o altri contenuti su Internet per promuovere la tua attività. Il contenuto digitale è ciò che è disponibile sul web. Il concetto di pubblicità digitale deriva dal concetto di "scarsità digitale". Questo concetto è il modo in cui la pubblicità digitale può essere utilizzata per vendere i tuoi prodotti e servizi. <br>
            <br>   
            INDICE:<br>
            1) Come funziona la pubblicità digitale?<br>
            2) Perchè usare la pubblicità digitale ?<br>
            3) <br>
            </b><br>
            e poi premi il bottone <b> '🤘 GENERAMI i TESTI 🤘' <br>
            Vedrai che l'Inteligenza Artificiale ti consiglierà di cosa parlare nel post del tuo Blog e nel capitolo del tuo Ebook o Libro📚.</b><br>
            ⚙️ IMPOSTAZIONI CONSIGLIATE :<br>
            ⚙️⚙️ Lunghezza massima del testo generato : 200 <br>
            ⚙️⚙️ Imposta la "follia" del testo : 0.50 / 0.60<br>""", selected_lang), unsafe_allow_html=True)

        with st.expander(traduttore("4🤖 Come generare testi liberi tuo Blog post, Ebook o Libro📚  🚀", selected_lang)):
            st.subheader(traduttore("Esempio 🚀", selected_lang))
            st.markdown(traduttore(""" Per generare dei testi liberi efficaci ti basterà fornire all'intelligenza Artificiale delle domande mirate e precise, lasciando poi a lei il compito rispondere.<br>
            Ad esempio se copi e incolli questo testo : <br><br><b>
            In un mercato caratterizzato da cambiamenti estremi e repentini, il Marketing Manager è una figura fondamentale all’interno delle aziende di qualunque dimensione.
            Egli coordina tutte quelle attività che precedono e costituiscono il lancio, nonché la successiva vendita, di un prodotto/servizio o un’intera gamma di prodotti/servizi.<br>
            Cosa fa il Marketing Manager?<br>
            </b><br>
            e poi premi il bottone <b> '🤘 GENERAMI i TESTI 🤘' <br>
            Vedrai che l'Inteligenza Artificiale ti genererà contenuti da copiare e incollare nel post del tuo Blog o nel capitolo del tuo Ebook o Libro📚.</b><br>
            ⚙️ IMPOSTAZIONI CONSIGLIATE :<br>
            ⚙️⚙️ Lunghezza massima del testo generato : 200 <br>
            ⚙️⚙️ Imposta la "follia" del testo : 0.50 / 0.60<br>""", selected_lang), unsafe_allow_html=True)


except Exception as e:
    st.error("Errore: {}".format(e))

