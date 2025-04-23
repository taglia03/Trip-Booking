import bs4
import requests
import webbrowser
import openpyxl
from openpyxl import Workbook, load_workbook, worksheet
import pandas as pd
import streamlit as st
import re

link = st.text_input("Link di ricerca")

if link:
    st.write("You entered: ", link)
    response = requests.get(link)
    response.raise_for_status()
    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    with st.container():
        
        body = soup.find('body')
        print(body.prettify())
        
        container = soup.find('div', class_='gsgwcjk atm_10yczz8_kb7nvz atm_10yczz8_cs5v99__1ldigyt atm_10yczz8_11wpgbn__1v156lz atm_10yczz8_egatvm__qky54b atm_10yczz8_qfx8er__1xolj55 atm_10yczz8_ouytup__w5e62l g8ge8f1 atm_1d13e1y_p5ox87 atm_yrukzc_1od0ugv atm_10yczz8_cs5v99_vagkz0_1ldigyt atm_10yczz8_11wpgbn_vagkz0_1h2hqoz g14v8520 atm_9s_11p5wf0 atm_d5_j5tqy atm_d7_1ymvx20 atm_dl_1mvrszh atm_dz_hxz02 dir dir-ltr')
        appartamenti = container.find_all('div', class_='c965t3n atm_9s_11p5wf0 atm_dz_1osqo2v dir dir-ltr')

        nomi = []
        prezzi = []
        urls = []

        for app in appartamenti:

            dati = app.find('div', class_ = 'g1qv1ctd atm_u80d3j_1li1fea atm_c8_o7aogt atm_g3_8jkm7i c1v0rf5q atm_9s_11p5wf0 atm_cx_4wguik atm_dz_7esijk atm_e0_1lo05zz dir dir-ltr')
            nome = dati.find('div', class_ = 't1jojoys atm_g3_1kw7nm4 atm_ks_15vqwwr atm_sq_1l2sidv atm_9s_cj1kg8 atm_6w_1e54zos atm_fy_1vgr820 atm_7l_jt7fhx atm_cs_10d11i2 atm_w4_1eetg7c atm_ks_zryt35__1rgatj2 dir dir-ltr').string
            prezzoTot = dati.find('div', class_ = '_1qr6aej9').span.string
            link_app = app.find('div', class_ = 'cy5jw6o atm_5j_1ktse57 atm_70_87waog atm_j3_1u6x1zy atm_jb_4shrsx atm_mk_h2mmj6 atm_vy_7abht0 dir dir-ltr').a.get('href')
            
            link_formatted = 'https://www.airbnb.it' + link_app
            # Rimuove lo spazio non separabile e altri caratteri non numerici
            testo = prezzoTot.replace('\xa0', '')  # Rimuove spazio speciale
            match = re.search(r'[\d.]+', testo)
            if match:
                numero = match.group().replace('.', '')  # Rimuove i separatori di migliaia
                numero = int(numero)
            else:
                numero = "non trovato"
            
            nomi.append(nome)
            prezzi.append(numero)
            urls.append(link_formatted)
        
        df = pd.DataFrame(
            {
                "nome": nomi,
                "totale": prezzi,
                "url": urls,
            }
        )

        st.dataframe(
            df,
            column_config={
                "nome": "Nome App",
                "totale": st.column_config.NumberColumn(
                    "Prezzo",
                    format="euro",
                ),
                "url": st.column_config.LinkColumn("URL App"),
            },
            hide_index=True,
        )