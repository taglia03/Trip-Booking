import bs4
import requests
import pandas as pd
import streamlit as st
import re

base_url = 'https://www.airbnb.it'
link = st.text_input("Link di ricerca")
n_pagine = st.number_input(
    "Per quante pagine vuoi eseguire la ricerca?",
    value=1,
    min_value=1,
    max_value=10,
    )

if link:

    nomi = []
    prezzi = []
    urls = []
    with st.spinner("Scansionando il sito...", show_time=False):
        
        for i in range(n_pagine):

            response = requests.get(link)
            response.raise_for_status()
            soup = bs4.BeautifulSoup(response.text, 'html.parser')
            
            pagina = soup.find('button', class_= 'l1ovpqvx atm_1he2i46_1k8pnbi_10saat9 atm_yxpdqi_1pv6nv4_10saat9 atm_1a0hdzc_w1h1e8_10saat9 atm_2bu6ew_929bqk_10saat9 atm_12oyo1u_73u7pn_10saat9 atm_fiaz40_1etamxe_10saat9 c1ackr0h atm_c8_km0zk7 atm_g3_18khvle atm_fr_1m9t47k atm_cs_10d11i2 atm_9s_1txwivl atm_h_1h6ojuz atm_fc_1h6ojuz atm_bb_idpfg4 atm_3f_glywfm atm_5j_1ssbidh atm_vy_1vi7ecw atm_e2_1vi7ecw atm_gi_idpfg4 atm_gz_1yuitx atm_h0_1yuitx atm_l8_idpfg4 atm_uc_10d7vwn atm_kd_glywfm atm_uc_glywfm__1rrf6b5 atm_tr_kv3y6q_csw3t1 atm_9j_73adwj_1o5j5ji atm_3f_glywfm_jo46a5 atm_l8_idpfg4_jo46a5 atm_gi_idpfg4_jo46a5 atm_3f_glywfm_1icshfk atm_kd_glywfm_19774hq atm_uc_aaiy6o_1w3cfyq atm_uc_glywfm_1w3cfyq_1rrf6b5 atm_uc_aaiy6o_pfnrn2_1oszvuo atm_uc_glywfm_pfnrn2_1o31aam c1bdq4u1 atm_26_18sdevw atm_7l_1v2u014 atm_26_18sdevw_1nos8r_uv4tnr atm_26_18sdevw_csw3t1 atm_26_18sdevw_1w3cfyq atm_70_14fqkim_1w3cfyq atm_26_18sdevw_pfnrn2_1oszvuo atm_70_14fqkim_pfnrn2_1oszvuo dir dir-ltr').string
            st.write("Recupero i dati da pagina " + pagina)

            container = soup.find('div', class_='gsgwcjk atm_10yczz8_kb7nvz atm_10yczz8_cs5v99__1ldigyt atm_10yczz8_11wpgbn__1v156lz atm_10yczz8_egatvm__qky54b atm_10yczz8_qfx8er__1xolj55 atm_10yczz8_ouytup__w5e62l g8ge8f1 atm_1d13e1y_p5ox87 atm_yrukzc_1od0ugv atm_10yczz8_cs5v99_vagkz0_1ldigyt atm_10yczz8_11wpgbn_vagkz0_1h2hqoz g14v8520 atm_9s_11p5wf0 atm_d5_j5tqy atm_d7_1ymvx20 atm_dl_1mvrszh atm_dz_hxz02 dir dir-ltr')
            appartamenti = container.find_all('div', class_='c965t3n atm_9s_11p5wf0 atm_dz_1osqo2v dir dir-ltr')

            for app in appartamenti:

                dati = app.find('div', class_ = 'g1qv1ctd atm_u80d3j_1li1fea atm_c8_o7aogt atm_g3_8jkm7i c1v0rf5q atm_9s_11p5wf0 atm_cx_4wguik atm_dz_7esijk atm_e0_1lo05zz dir dir-ltr')
                prezzoTot = dati.find('div', class_ = '_1qr6aej9').span.string
                link_app = app.find('div', class_ = 'cy5jw6o atm_5j_1ktse57 atm_70_87waog atm_j3_1u6x1zy atm_jb_4shrsx atm_mk_h2mmj6 atm_vy_7abht0 dir dir-ltr').a.get('href')
                nome = app.find('div', class_ = 'cfutgp0 atm_d2_1kqhmmj dir dir-ltr').div.find('meta').get('content')

                link_formatted = base_url + link_app
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

            link = soup.find('div', class_='p1j2gy66 atm_9s_1txwivl dir dir-ltr')
            link = link.find('a', class_= 'l1ovpqvx atm_1he2i46_1k8pnbi_10saat9 atm_yxpdqi_1pv6nv4_10saat9 atm_1a0hdzc_w1h1e8_10saat9 atm_2bu6ew_929bqk_10saat9 atm_12oyo1u_73u7pn_10saat9 atm_fiaz40_1etamxe_10saat9 c1ytbx3a atm_mk_h2mmj6 atm_9s_1txwivl atm_h_1h6ojuz atm_fc_1h6ojuz atm_bb_idpfg4 atm_26_1j28jx2 atm_3f_glywfm atm_7l_hkljqm atm_gi_idpfg4 atm_l8_idpfg4 atm_uc_10d7vwn atm_kd_glywfm atm_gz_8tjzot atm_uc_glywfm__1rrf6b5 atm_26_zbnr2t_1rqz0hn_uv4tnr atm_tr_kv3y6q_csw3t1 atm_26_zbnr2t_1ul2smo atm_3f_glywfm_jo46a5 atm_l8_idpfg4_jo46a5 atm_gi_idpfg4_jo46a5 atm_3f_glywfm_1icshfk atm_kd_glywfm_19774hq atm_70_glywfm_1w3cfyq atm_uc_aaiy6o_9xuho3 atm_70_18bflhl_9xuho3 atm_26_zbnr2t_9xuho3 atm_uc_glywfm_9xuho3_1rrf6b5 atm_70_glywfm_pfnrn2_1oszvuo atm_uc_aaiy6o_1buez3b_1oszvuo atm_70_18bflhl_1buez3b_1oszvuo atm_26_zbnr2t_1buez3b_1oszvuo atm_uc_glywfm_1buez3b_1o31aam atm_7l_1wxwdr3_1o5j5ji atm_9j_13gfvf7_1o5j5ji atm_26_1j28jx2_154oz7f atm_92_1yyfdc7_vmtskl atm_9s_1ulexfb_vmtskl atm_mk_stnw88_vmtskl atm_tk_1ssbidh_vmtskl atm_fq_1ssbidh_vmtskl atm_tr_pryxvc_vmtskl atm_vy_1vi7ecw_vmtskl atm_e2_1vi7ecw_vmtskl atm_5j_1ssbidh_vmtskl atm_mk_h2mmj6_1ko0jae dir dir-ltr')
            link = link.get('href')
            link = base_url + link

            if link == False:
                break
            
    with st.container():

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
                "nome": st.column_config.TextColumn(
                    "Nome App",
                    width='small',
                ),
                "totale": st.column_config.NumberColumn(
                    "Prezzo",
                    format="euro",
                    width='small',
                ),
                "url": st.column_config.LinkColumn(
                    "URL App",
                    width='small',
                ),
            },
            hide_index=True,
        )