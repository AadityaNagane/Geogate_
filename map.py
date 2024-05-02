import openrouteservice
from openrouteservice import convert
import folium
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import streamlit as st
from streamlit_folium import folium_static
import stripe
import uuid  # For generating unique IDs
import os

# Initialize Firebase app with credentials
# cred = credentials.Certificate("D:/SPIT/SEM 4/microproject/miniprojectfrontend/Basic Program/Key.json")
# firebase_admin.initialize_app(cred,{
#     'databaseURL': 'https://sim800l-3bb6f-default-rtdb.asia-southeast1.firebasedatabase.app/'
# })

# # Initialize Firestore client
# db = firestore.client()

# # Specify collection name and document ID
# collection_name = ''
# document_id = 'geopoint'

# # Reference the document
# doc_ref = db.collection(collection_name).document(document_id)

# # Retrieve longitude and latitude from Firestore
# doc_data = doc_ref.get().to_dict()
# longitude = doc_data.get('longitude')
# latitude = doc_data.get('latitude')

import openrouteservice
from openrouteservice import convert
import folium
from shapely.geometry import Point, Polygon
import streamlit as st
import stripe
import uuid  # For generating unique IDs
import os


# Payment interface
# Set your Stripe API keys
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY', 'sk_test_51PBAtSSAg3QgoWNpRHooCBiF4o7hNqr7vanoi4MgiGmCEifslsiFSEo4e8xmdA7CGaG4mt7k3hqagSXDtrLL3ptT009qc9vpD4')

total_amount=1000     
def create_payment_intent(total_amount, session_id):
    """
    Creates a Payment Intent on Stripe.

    Args:
        total_amount (int): The total amount in paisa.
        session_id (str): A unique session ID for reference.

    Returns:
        stripe.PaymentIntent: The created Payment Intent object or None on error.
    """
    try:
        intent = stripe.PaymentIntent.create(
            amount=total_amount,
            currency="inr",
            confirm=False,
            metadata={"session_id": session_id},
        )
        return intent
    except stripe.error.StripeError as e:
        st.error(f"Error creating payment intent: {e}")
        return None

def generate_unique_session_id():
    """
    Generates a unique session ID.

    Returns:
        str: A unique session ID string.
    """
    return str(uuid.uuid4())

def app():
    # Initialize OpenRouteService client with API key
    client = openrouteservice.Client(key='5b3ce3597851110001cf6248d4f4172ccaa242cab65930185ce46059')

    # Define coordinates for routing
    coords = ((72.84170220982669,19.228556018441456), ( 73.79631472329982,18.63753914054138))
    booth1= ( 
    (19.037095, 73.071661),  # Cord 1
    (19.035766, 73.072364),  # Cord 2
    (19.037095, 73.073871),  # Cord 3
    (19.037808, 73.072816)   # Cord 4
    )
    booth2= (
    (19.067184,72.983495),  # Cord 1
    (19.066637, 72.984394),  # Cord 2
    (19.065986, 72.983539),  # Cord 3
    (19.066404, 72.982691)   # Cord 4
    )
    booth3= (
    (19.068778, 72.908793),  # Cord 1
    (19.069581, 72.908113),  # Cord 2
    (19.069921, 72.909322),  # Cord 3
    (19.068670, 72.910021)   # Cord 4
    )
    booth4= ( 
    (18.901764, 73.221674),  # Cord 1
    (18.901740, 73.222335),  # Cord 2
    (18.901245, 73.222309),  # Cord 3
    (18.901254, 73.221638)   # Cord 4
    )
    booth5= ( 
    (18.688872, 73.717556),  # Cord 1
    (18.689320, 73.718157),  # Cord 2
    (18.688679, 73.718769),  # Cord 3
    (18.688283, 73.718339)   # Cord 4
    )
    booth6= ( 
    (19.124613, 72.836575),  # Cord 1
    (19.124598, 72.836579),  # Cord 2
    (19.124603, 72.836601),  # Cord 3
    (19.124618, 72.836582)   # Cord 4
    )
    booth7= ( 
    (19.123070, 72.836503),  # Cord 1
    (19.123084, 72.836575),  # Cord 2
    (19.123013, 72.836578),  # Cord 3
    (19.123015, 72.836506)   # Cord 4
    )
    # Streamlit sidebar input for user's location
    st.sidebar.title("User's Location")
    user_lat = st.sidebar.number_input("Latitude", value=19.123339770515123, step=0.01)
    user_lon = st.sidebar.number_input("Longitude", value=72.83635142888058, step=0.01)
    user_location = (user_lat, user_lon)


    # Get route information
    res = client.directions(coords)
    geometry = res['routes'][0]['geometry']

    # Decode polyline geometry
    decoded = convert.decode_polyline(geometry)

    # Calculate distance and duration
    distance_km = round(res['routes'][0]['summary']['distance'] / 1000, 1)
    duration_min = round(res['routes'][0]['summary']['duration'] / 60, 1)

    # Prepare HTML strings for distance and duration
    distance_txt = "<h4><b>Distance: " + str(distance_km) + " Km</b></h4>"
    duration_txt = "<h4><b>Duration: " + str(duration_min) + " Mins.</b></h4>"

    # Create a folium map
    m = folium.Map(location=[user_lat, user_lon], zoom_start=10, control_scale=True, tiles="cartodbpositron") 

    # Add decoded route to the map with distance and duration popup
    folium.GeoJson(decoded).add_child(folium.Popup(distance_txt + duration_txt, max_width=300)).add_to(m)

    # Add markers for start and end points
    folium.Marker(
        location=list(coords[0][::-1]),
        icon=folium.Icon(color="green"),
    ).add_to(m)

    folium.Marker(
        location=list(coords[1][::-1]),
        icon=folium.Icon(color="red"),
    )   .add_to(m)

   # Create a Shapely Polygon from the geofence coordinates
    geofence_polygon1 = Polygon(booth1)
    geofence_polygon2 = Polygon(booth2)
    geofence_polygon3 = Polygon(booth3)
    geofence_polygon4 = Polygon(booth4)
    geofence_polygon5 = Polygon(booth5)
    geofence_polygon6 = Polygon(booth6)
    geofence_polygon7 = Polygon(booth7)

    # Add marker for the user's location
    folium.Marker(
    location=[user_lat, user_lon],
    popup='User Location',
    icon=folium.Icon(color='blue')
    ).add_to(m)

    # Highlight the geofence polygon on the map
    folium.Polygon(
    locations=booth1,
    color='red',
    fill=True,
    fill_color='red',
    fill_opacity=0.3,
    popup='Geofence Area'
    ).add_to(m)

    folium.Polygon(
    locations=booth2,
    color='red',
    fill=True,
    fill_color='red',
    fill_opacity=0.3,
    popup='Geofence Area'
    ).add_to(m)

    session_id = generate_unique_session_id()

    # Check if the user's location is within the geofence
    user_point = Point(user_location)
    if geofence_polygon1.contains(user_point):
        st.write("The user's location is within the geofence.")
        intent = create_payment_intent(total_amount, session_id)

        if intent:
            # Placeholder for Stripe.js integration (see instructions below)
            st.write(
                """<script>
                // Replace with your Stripe.js code to collect payment method details
                // and send them to your backend server to confirm the Payment Intent.
                </script>""",
                unsafe_allow_html=True,
            )
    elif geofence_polygon2.contains(user_point):
        st.write("The user's location is within the geofence.")
        intent = create_payment_intent(total_amount, session_id)

        if intent:
            # Placeholder for Stripe.js integration (see instructions below)
            st.write(
                """<script>
                // Replace with your Stripe.js code to collect payment method details
                // and send them to your backend server to confirm the Payment Intent.
                </script>""",
                unsafe_allow_html=True,
            )
    elif geofence_polygon3.contains(user_point):
        st.write("The user's location is within the geofence.")
        intent = create_payment_intent(total_amount, session_id)

        if intent:
            # Placeholder for Stripe.js integration (see instructions below)
            st.write(
                """<script>
                // Replace with your Stripe.js code to collect payment method details
                // and send them to your backend server to confirm the Payment Intent.
                </script>""",
                unsafe_allow_html=True,
            )
    elif geofence_polygon4.contains(user_point):
        st.write("The user's location is within the geofence.")
        intent = create_payment_intent(total_amount, session_id)

        if intent:
            # Placeholder for Stripe.js integration (see instructions below)
            st.write(
                """<script>
                // Replace with your Stripe.js code to collect payment method details
                // and send them to your backend server to confirm the Payment Intent.
                </script>""",
                unsafe_allow_html=True,
            )
    elif geofence_polygon5.contains(user_point):
        st.write("The user's location is within the geofence.")
        intent = create_payment_intent(total_amount, session_id)

        if intent:
            # Placeholder for Stripe.js integration (see instructions below)
            st.write(
                """<script>
                // Replace with your Stripe.js code to collect payment method details
                // and send them to your backend server to confirm the Payment Intent.
                </script>""",
                unsafe_allow_html=True,
            )
    elif geofence_polygon6.contains(user_point):
        st.write("The user's location is within the geofence.")
        intent = create_payment_intent(total_amount, session_id)

        if intent:
            # Placeholder for Stripe.js integration (see instructions below)
            st.write(
                """<script>
                // Replace with your Stripe.js code to collect payment method details
                // and send them to your backend server to confirm the Payment Intent.
                </script>""",
                unsafe_allow_html=True,
            )
    elif geofence_polygon7.contains(user_point):
        st.write("The user's location is within the geofence.")
        intent = create_payment_intent(total_amount, session_id)

        if intent:
            # Placeholder for Stripe.js integration (see instructions below)
            st.write(
                """<script>
                // Replace with your Stripe.js code to collect payment method details
                // and send them to your backend server to confirm the Payment Intent.
                </script>""",
                unsafe_allow_html=True,
            )
    else:
        st.write("The user's location is outside the geofence.")
    folium.Marker(
        location=(user_lat, user_lon),
        popup="Car's Location",
        icon=folium.Icon(color="blue"),
    ).add_to(m)

    # Highlight the route geofence
    folium.Polygon(locations=booth1, color='blue', fill=True, fill_color='blue', fill_opacity=0.3).add_to(m)
    folium.Polygon(locations=booth2, color='blue', fill=True, fill_color='blue', fill_opacity=0.3).add_to(m)
    folium.Polygon(locations=booth3, color='blue', fill=True, fill_color='blue', fill_opacity=0.3).add_to(m)
    folium.Polygon(locations=booth4, color='blue', fill=True, fill_color='blue', fill_opacity=0.3).add_to(m)
    folium.Polygon(locations=booth5, color='blue', fill=True, fill_color='blue', fill_opacity=0.3).add_to(m)
    folium.Polygon(locations=booth6, color='blue', fill=True, fill_color='blue', fill_opacity=0.3).add_to(m)
    folium.Polygon(locations=booth7, color='blue', fill=True, fill_color='blue', fill_opacity=0.3).add_to(m)
    # Display the map
    folium_static(m)
