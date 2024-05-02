import streamlit as st
from firebase_admin import firestore
from PIL import Image

def app():
    st.title("Welcome to Toll Tax Tracker")

    # Add images from local gallery
    image1 = Image.open(r"D:\SPIT\SEM 4\microproject\Commit 1\home_page.png") 
    # Use raw string (r"") or replace backslashes with forward slashes
    # Add more images as needed
    # image2 = Image.open(r"path/to/your/image2.jpg")

    st.image(image1, caption="Toll System Of India")

    st.write(
        """
        ## Importance of Toll Tax

        Welcome to our website dedicated to exploring the importance of toll taxes in infrastructure development and transportation management.
        Here's why toll taxes are crucial:

        ### 1. Infrastructure Development:
        Toll taxes play a vital role in financing the construction and maintenance of essential infrastructure like highways and bridges. 
        These projects enhance transportation efficiency and safety, fostering economic growth and development.

        ### 2. Revenue Generation
        Toll collection provides a significant source of revenue for government agencies responsible for road maintenance and upgrades. 
        This revenue can be used to cover operating costs, repay loans, and fund future infrastructure projects.

        ### 3. Traffic Management
        Toll imposition allows authorities to regulate traffic flow and alleviate congestion. Through strategies like congestion pricing, 
        tolls incentivize drivers to use less congested routes or travel during off-peak hours, thus enhancing overall traffic management.

        ### 4. User Pays Principle
        Toll taxes adhere to the "user pays" principle, ensuring that those who benefit from using road infrastructure contribute to its upkeep.
        This equitable distribution of maintenance costs among road users prevents an undue burden on taxpayers.

        **Join us as we delve deeper into the significance of toll taxes in shaping our transportation landscape and driving sustainable development.**
        """
    )