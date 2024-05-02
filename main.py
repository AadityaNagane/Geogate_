import streamlit as st

from streamlit_option_menu import option_menu


import home, account, about, payment_options,map
st.set_page_config(
        page_title="Geogate",
)



class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):

        self.apps.append({
            "title": title,
            "function": func
        })

    def run():
        # app = st.sidebar(
        with st.sidebar:        
            app = option_menu(
                menu_title='Geogate',
                options=['Home','Account','Payment','Location Tracker','about'],
                icons=['house-fill','person-circle','wallet-fill','geo-fill','info-circle-fill'],
                menu_icon='globe',
                default_index=1,
                styles={
                    "container": {"padding": "5!important","background-color":'grey'},
        "icon": {"color": "white", "font-size": "23px"}, 
        "nav-link": {"color":"white","font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "blue"},
        "nav-link-selected": {"background-color": "#02ab21"},}
                
                )

        
        if app == "Home":
            home.app()
        if app == "Account":
            account.app()    
        if app == "Payment":
            payment_options.main()        
        if app == 'Location Tracker':
            map.app()
        if app == 'about':
            about.app()    
             
          
             
    run()            
         
