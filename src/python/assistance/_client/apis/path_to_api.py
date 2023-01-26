import typing_extensions
from _client.apis.paths.chat_student_continue import ChatStudentContinue
from _client.apis.paths.chat_student_start import ChatStudentStart
from _client.apis.paths.login import Login
from _client.apis.paths.query_from_transcript import QueryFromTranscript
from _client.apis.paths.save_form import SaveForm
from _client.apis.paths.search_alphacrucis import SearchAlphacrucis
from _client.apis.paths.send_signin_link import SendSigninLink
from _client.apis.paths.summarise_with_query_raw import SummariseWithQueryRaw
from _client.apis.paths.summarise_with_query_url import SummariseWithQueryUrl
from _client.apis.paths.temp_account import TempAccount
from _client.paths import PathValues

PathToApi = typing_extensions.TypedDict(
    "PathToApi",
    {
        PathValues.LOGIN: Login,
        PathValues.TEMPACCOUNT: TempAccount,
        PathValues.CHAT_STUDENT_START: ChatStudentStart,
        PathValues.CHAT_STUDENT_CONTINUE: ChatStudentContinue,
        PathValues.SAVE_FORM: SaveForm,
        PathValues.SEARCH_ALPHACRUCIS: SearchAlphacrucis,
        PathValues.SEND_SIGNINLINK: SendSigninLink,
        PathValues.SUMMARISE_WITHQUERY_RAW: SummariseWithQueryRaw,
        PathValues.SUMMARISE_WITHQUERY_URL: SummariseWithQueryUrl,
        PathValues.QUERY_FROMTRANSCRIPT: QueryFromTranscript,
    },
)

path_to_api = PathToApi(
    {
        PathValues.LOGIN: Login,
        PathValues.TEMPACCOUNT: TempAccount,
        PathValues.CHAT_STUDENT_START: ChatStudentStart,
        PathValues.CHAT_STUDENT_CONTINUE: ChatStudentContinue,
        PathValues.SAVE_FORM: SaveForm,
        PathValues.SEARCH_ALPHACRUCIS: SearchAlphacrucis,
        PathValues.SEND_SIGNINLINK: SendSigninLink,
        PathValues.SUMMARISE_WITHQUERY_RAW: SummariseWithQueryRaw,
        PathValues.SUMMARISE_WITHQUERY_URL: SummariseWithQueryUrl,
        PathValues.QUERY_FROMTRANSCRIPT: QueryFromTranscript,
    }
)
