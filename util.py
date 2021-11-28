from urllib import parse

def get_current_page_num(uri):
    """
    return: int
    """
    try:
        parsed_uri = parse.parse_qs(parse.urlparse(uri).query)
        if parsed_uri["page"] is not None:
            return int(parsed_uri["page"][0]) - 1
    except:
        raise Exception("Invalid URI")