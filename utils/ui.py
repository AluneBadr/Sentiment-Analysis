import streamlit  as st
import datetime
from utils.fonctions import (
    local_css,
    img_to_bytes,
)

def side():
    local_css('./css/styles.css')
    st.markdown("---")
    st.markdown(
    """<div id="img-container">
        <img src='data:image/png;base64,{}' class='img-fluid' width=200 height=200>
        <h1>KA Alioune</h1>
        <div class="images">
            <a href="https://github.com/AluneBadr" target="_blank"><img src="data:image/png;base64,{}"/></a>
            <a href="https://www.linkedin.com/in/alioune-ka-017351171/" target="_blank"><img src="data:image/png;base64,{}"/></a>
        </div>
    </div>""".format(img_to_bytes("./image/Image1.png"),
                     img_to_bytes("./image/github.png"),
                     img_to_bytes("./image/linkedin.png")
                     ),unsafe_allow_html=True)

    st.markdown(
        """<div id="bio-info">
        <h3> Data Scientist / Engineer </h3>
    </div>""", unsafe_allow_html=True)

    st.markdown(
        """<div id="bio-contact">
        <p>
            📧 : aliouneka95@outlook.fr <br/>
            📞 : 0658262149 <br/>
            🏠 : 12 Rue Nicolas Copernic 27000, Evreux
        </p>
         <br/>
    </div>""", unsafe_allow_html=True)


def header():
    st.markdown(
        """<div>
        <h3> About Me  💕</h3>
        <h4> ══════════ </h4>
        <div style="background-color:#EAF2F8;padding:1px;border-radius:5px;margin:2px; border:3px solid #3498DB;">
        <p> {}</p>
        </div>
        </div>
        """.format(about_me), unsafe_allow_html=True)
    st.markdown('---')
