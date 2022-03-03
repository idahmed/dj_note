from rest_framework.parsers import JSONParser


class PlainTextWithJSONParser(JSONParser):
    """ Plain text with JSON Body
    """

    media_type = "text/plain"
