# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from _client.apis.path_to_api import path_to_api

import enum


class PathValues(str, enum.Enum):
    LOGIN = "/login"
    TEMPACCOUNT = "/temp-account"
    CHAT_STUDENT_START = "/chat/student/start"
    CHAT_STUDENT_CONTINUE = "/chat/student/continue"
    SAVE_FORM = "/save/form"
    SEARCH_ALPHACRUCIS = "/search/alphacrucis"
    SEND_SIGNINLINK = "/send/signin-link"
    SUMMARISE_WITHQUERY_RAW = "/summarise/with-query/raw"
    SUMMARISE_WITHQUERY_URL = "/summarise/with-query/url"
    QUERY_FROMTRANSCRIPT = "/query/from-transcript"
