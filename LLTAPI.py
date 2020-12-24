import pytz
import ipinfo
import pandas as pd
import streamlit as st
from tzwhere import tzwhere
from datetime import datetime
from geopy.geocoders import Nominatim
from streamlit.server.server import Server
from geopy.extra.rate_limiter import RateLimiter
from streamlit.report_thread import get_report_ctx

class SessionState(object):
    def __init__(self, **kwargs):
        """A new SessionState object.

        Parameters
        ----------
        **kwargs : any
            Default values for the session state.

        Example
        -------
        >>> session_state = SessionState(user_name='', favorite_color='black')
        >>> session_state.user_name = 'Mary'
        ''
        >>> session_state.favorite_color
        'black'

        """

        #self.request.remote_ip

        for key, val in kwargs.items():
            setattr(self, key, val)


@st.cache(allow_output_mutation=True)
def get_session(id, **kwargs):
    return SessionState(**kwargs)


def get(**kwargs):
    """Gets a SessionState object for the current session.

    Creates a new object if necessary.

    Parameters
    ----------
    **kwargs : any
        Default values you want to add to the session state, if we're creating a
        new one.

    Example
    -------
    >>> session_state = get(user_name='', favorite_color='black')
    >>> session_state.user_name
    ''
    >>> session_state.user_name = 'Mary'
    >>> session_state.favorite_color
    'black'

    Since you set user_name above, next time your script runs this will be the
    result:
    >>> session_state = get(user_name='', favorite_color='black')
    >>> session_state.user_name
    'Mary'

    """
    ctx = get_report_ctx()
    id = ctx.session_id
    return get_session(id, **kwargs)



def main():
    # Register your pages
    pages = {
        "Home page": page_first,
        "Update Address": page_second,
    }

    st.title("Pre-interview Code Submission ")

    st.markdown("""
    This app performs simple test for accuenergy.com
    * **Libraries:** base64, pandas, streamlit, Javascript, IPInfo, Markdown 
    * **Source Code:** [Lionel Luo @github.com](https://github.com/bigdataisland/webdemo/blob/main/LLTAPI.py).
    """)

    st.sidebar.title("Search By Address")
    sessions = Server.get_current()._session_info_by_id
    session_id_key = list(sessions.keys())[0]
    session = sessions[session_id_key]

    if session.ws.request.remote_ip == '127.0.0.1':
        ip = session.ws.request.headers['X-Forwarded-For'].split(',')[0]
    else:
        ip = '123.59.195.125'

    access_token = 'cbacbcd0adb278'
    handler = ipinfo.getHandler(access_token)
    ip_address = ip
    details = handler.getDetails(ip_address)

    my_street = ""
    my_city = details.city
    my_province = details.region
    my_country = details.country_name

    street = st.sidebar.text_input("Street", my_street)
    city = st.sidebar.text_input("City", my_city)
    province = st.sidebar.text_input("Province", my_province)
    country = st.sidebar.text_input("Country", my_country)

    if st.sidebar.button('New Search'):
        pass
    else:
        pass

    geolocator = Nominatim(user_agent="GTA Lookup")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    location = geolocator.geocode(street + ", " + city + ", " + province + ", " + country)

    st.markdown(f"**Address Info Details**")
    st.write(location)

    lat = location.latitude
    lon = location.longitude


    tz = tzwhere.tzwhere()
    tz_name = tz.tzNameAt(lat, lon)

    st.markdown(f"**Time Information**")
    utc = pytz.utc

    # 'UTC'
    utc_today = datetime.now(utc)

    timestamp = utc_today.timestamp()

    tz = pytz.timezone(tz_name)
    local_today = datetime.now(tz)

    st.markdown(f"Timezone: ***{tz_name}***")
    st.markdown(f"UTC Timestamp: ***{timestamp}***")
    st.markdown(f"Local Time: ***{local_today}***")

    map_data = pd.DataFrame({'lat': [lat], 'lon': [lon]})

    #st.write('Display the location in map')
    st.markdown(f"**Address Map**")
    st.map(map_data, zoom=12)

def page_first():
    st.title("This is my first page")
    # ...

    session_state = get(remote_ip='', favorite_color='black')
    sessions = Server.get_current()._session_info_by_id
    session_id_key = list(sessions.keys())[0]
    session = sessions[session_id_key]

    # Default IP
    ip = '123.59.195.125'
    access_token = 'cbacbcd0adb278'
    handler = ipinfo.getHandler(access_token)
    ip_address = ip
    details = handler.getDetails(ip_address)
    st.write(details.all)

    street = st.sidebar.text_input("Street", '1')
    city = st.sidebar.text_input("City", details.city)
    province = st.sidebar.text_input("Province", details.region)
    country = st.sidebar.text_input("Country", details.country_name)

    lat = float(details.latitude)
    lon = float(details.longitude)

    st.write('lat: ' + str(lat))
    st.write('lon: ' + str(lon))

    map_data = pd.DataFrame({'lat': [lat], 'lon': [lon]})

    # st.map(map_data)
    st.map(map_data, zoom=12)


def page_second():
    st.title("This is my second page")
    # ...

    street = st.sidebar.text_input("Street", "")
    city = st.sidebar.text_input("City", "")
    province = st.sidebar.text_input("Province", "")
    country = st.sidebar.text_input("Country", "")

    geolocator = Nominatim(user_agent="GTA Lookup")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    location = geolocator.geocode(street + ", " + city + ", " + province + ", " + country)

    st.write(location)

    lat = location.latitude
    lon = location.longitude

    st.write('lat: ' + str(lat))
    st.write('lon: ' + str(lon))

    map_data = pd.DataFrame({'lat': [lat], 'lon': [lon]})

    # st.map(map_data)
    st.map(map_data, zoom=12)

if __name__ == "__main__":
    main()

