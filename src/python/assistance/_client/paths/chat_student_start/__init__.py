# do not import all endpoints into this module because that uses a lot of memory and stack frames
# if you need the ability to import all endpoints from this module, import them with
# from assistance._client.paths.chat_student_start import Api

from assistance._client.paths import PathValues

path = PathValues.CHAT_STUDENT_START
