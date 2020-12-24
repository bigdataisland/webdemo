from streamlit.report_thread import get_report_ctx
import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

from streamlit.server.server import Server

import ipinfo
import json
from urllib import request


def get_headers():
    # Hack to get the session object from Streamlit.

    current_server = Server.get_current()
    if hasattr(current_server, '_session_infos'):
        # Streamlit < 0.56
        session_infos = Server.get_current()._session_infos.values()
    else:
        session_infos = Server.get_current()._session_info_by_id.values()

    st.write('test')


    # Multiple Session Objects?
    for session_info in session_infos:
        headers = session_info.ws.request.headers
        st.write(headers)
#    return headers

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
        "First page": page_first,
        "Second page": page_second,
    }

    st.sidebar.title("App with pages")

    # Widget to select your page, you can choose between radio buttons or a selectbox
    page = st.sidebar.selectbox("Select your page", tuple(pages.keys()))
    #page = st.sidebar.radio("Select your page", tuple(pages.keys()))

    #ip = st.request.remote_ip
    # url = 'http://ipinfo.io/json'
    # response = request.urlopen(url)
    # data = json.load(response)
    #
    # st.write(data)

    # ctx = get_report_ctx()
    # id = ctx.session_id
    # st.write(ctx.session_id)
    # for key, val in ctx.items():
    #     st.write(key)
    #     st.write(key)


    st.write(Server)


    session_state = get(remote_ip='', favorite_color='black')

    st.write(session_state.remote_ip)

    sessions = Server.get_current()._session_info_by_id
    session_id_key = list(sessions.keys())[0]
    session = sessions[session_id_key]
    st.write(session.ws.request.remote_ip)

    st.write(session.ws.request.headers)
    st.write([session.ws.request.headers['X-Forwarded-For']][0])
    st.write(session.ws.request.uri)
    st.write(session.ws.request.host_name)
    st.write(session.ws.request.host)
    st.write(session.ws.request.host)

    if session.ws.request.remote_ip == '127.0.0.1':
        ip = '69.158.134.166'
    else:
        ip = [session.ws.request.headers['X-Forwarded-For']][0]

    st.write(ip)

    #st.write("URL PARAM:" + str(urlpara))
    #get_headers()

    # Display the selected page with the session state
    pages[page]()


def page_first():
    st.title("This is my first page")
    # ...
    street = st.sidebar.text_input("Street", "75 Bay Street")
    city = st.sidebar.text_input("City", "Toronto")
    province = st.sidebar.text_input("Province", "Ontario")
    country = st.sidebar.text_input("Country", "Canada")

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


def page_second():
    st.title("This is my second page")
    # ...


if __name__ == "__main__":
    main()

# Streamlit - Settings page with session state
# https://gist.github.com/okld/0aba4869ba6fdc8d49132e6974e2e662

# https://gist.github.com/tvst/036da038ab3e999a64497f42de966a92
# https://github.com/streamlit/streamlit/blob/844691d0b15e0f3622a1fb97b34e4eae4161fe3f/lib/streamlit/ReportSession.py#L54

# import streamlit as st
# from streamlit.hashing import _CodeHasher
#
# try:
#     # Before Streamlit 0.65
#     from streamlit.ReportThread import get_report_ctx
#     from streamlit.server.Server import Server
# except ModuleNotFoundError:
#     # After Streamlit 0.65
#     from streamlit.report_thread import get_report_ctx
#     from streamlit.server.server import Server
#
#
# def main():
#     state = _get_state()
#     pages = {
#         "Dashboard": page_dashboard,
#         "Settings": page_settings,
#     }
#
#     st.sidebar.title(":floppy_disk: Page states")
#     page = st.sidebar.radio("Select your page", tuple(pages.keys()))
#
#     # Display the selected page with the session state
#     pages[page](state)
#
#     # Mandatory to avoid rollbacks with widgets, must be called at the end of your app
#     state.sync()
#
#
# def page_dashboard(state):
#     st.title(":chart_with_upwards_trend: Dashboard page")
#     display_state_values(state)
#
#
# def page_settings(state):
#     st.title(":wrench: Settings")
#     display_state_values(state)
#
#     st.write("---")
#     options = ["Hello", "World", "Goodbye"]
#     state.input = st.text_input("Set input value.", state.input or "")
#     state.slider = st.slider("Set slider value.", 1, 10, state.slider)
#     state.radio = st.radio("Set radio value.", options, options.index(state.radio) if state.radio else 0)
#     state.checkbox = st.checkbox("Set checkbox value.", state.checkbox)
#     state.selectbox = st.selectbox("Select value.", options, options.index(state.selectbox) if state.selectbox else 0)
#     state.multiselect = st.multiselect("Select value(s).", options, state.multiselect)
#
#     # Dynamic state assignments
#     for i in range(3):
#         key = f"State value {i}"
#         state[key] = st.slider(f"Set value {i}", 1, 10, state[key])
#
#
# def display_state_values(state):
#     st.write("Input state:", state.input)
#     st.write("Slider state:", state.slider)
#     st.write("Radio state:", state.radio)
#     st.write("Checkbox state:", state.checkbox)
#     st.write("Selectbox state:", state.selectbox)
#     st.write("Multiselect state:", state.multiselect)
#
#     for i in range(3):
#         st.write(f"Value {i}:", state[f"State value {i}"])
#
#     if st.button("Clear state"):
#         state.clear()
#
#
# class _SessionState:
#
#     def __init__(self, session, hash_funcs):
#         """Initialize SessionState instance."""
#         self.__dict__["_state"] = {
#             "data": {},
#             "hash": None,
#             "hasher": _CodeHasher(hash_funcs),
#             "is_rerun": False,
#             "session": session,
#         }
#
#     def __call__(self, **kwargs):
#         """Initialize state data once."""
#         for item, value in kwargs.items():
#             if item not in self._state["data"]:
#                 self._state["data"][item] = value
#
#     def __getitem__(self, item):
#         """Return a saved state value, None if item is undefined."""
#         return self._state["data"].get(item, None)
#
#     def __getattr__(self, item):
#         """Return a saved state value, None if item is undefined."""
#         return self._state["data"].get(item, None)
#
#     def __setitem__(self, item, value):
#         """Set state value."""
#         self._state["data"][item] = value
#
#     def __setattr__(self, item, value):
#         """Set state value."""
#         self._state["data"][item] = value
#
#     def clear(self):
#         """Clear session state and request a rerun."""
#         self._state["data"].clear()
#         self._state["session"].request_rerun()
#
#     def sync(self):
#         """Rerun the app with all state values up to date from the beginning to fix rollbacks."""
#
#         # Ensure to rerun only once to avoid infinite loops
#         # caused by a constantly changing state value at each run.
#         #
#         # Example: state.value += 1
#         if self._state["is_rerun"]:
#             self._state["is_rerun"] = False
#
#         elif self._state["hash"] is not None:
#             if self._state["hash"] != self._state["hasher"].to_bytes(self._state["data"], None):
#                 self._state["is_rerun"] = True
#                 self._state["session"].request_rerun()
#
#         self._state["hash"] = self._state["hasher"].to_bytes(self._state["data"], None)
#
#
# def _get_session():
#     session_id = get_report_ctx().session_id
#     session_info = Server.get_current()._get_session_info(session_id)
#
#     if session_info is None:
#         raise RuntimeError("Couldn't get your Streamlit Session object.")
#
#     return session_info.session
#
#
# def _get_state(hash_funcs=None):
#     session = _get_session()
#
#     if not hasattr(session, "_custom_session_state"):
#         session._custom_session_state = _SessionState(session, hash_funcs)
#
#     return session._custom_session_state
#
#
# if __name__ == "__main__":
#     main()

