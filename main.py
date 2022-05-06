import streamlit as st
from dalle import create_and_show_images

st.title("DALL-E Mini")

text = st.text_input("Scrivi una parola o frase e l'I.A. crearà delle immagini?")

num_images = st.slider("Quante immagini vuoi?", 1, 6)

ok = st.button("Crea!")

if ok:
    create_and_show_images(text, num_images)
