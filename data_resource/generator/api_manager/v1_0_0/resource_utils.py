import math
from collections import OrderedDict


def _compute_offset(page: int, items_per_page: int) -> int:
    """Compute the offset value for pagination.

    Args:
        page (int): The current page to compute the offset from.
        items_per_page (int): Number of items per page.
    Returns:
        int: The offset value.
    """
    return int(int(int(page) - 1) * int(items_per_page))


def _compute_page(offset: int, items_per_page: int) -> int:
    """Compute the current page number based on offset.

    Args:
        offset (int): The offset to use to compute the page.
        items_per_page (int): Nimber of items per page.
    Returns:
        int: The page number.
    """

    return int(math.ceil((int(offset) + 1) / int(items_per_page)))


def build_links(endpoint: str, offset: int, limit: int, rows: int):
    """Build links for a paginated response
    Args:
        endpoint (str): Name of the endpoint to provide in the link.
        offset (int): Database query offset.
        limit (int): Number of items to return in query.
        rows (int): Count of rows in table.

    Returns:
        dict: The links based on the offset and limit
    """
    offset = int(offset)
    limit = int(limit)
    rows = int(rows)

    # URL and pages
    url_link = "/{}?offset={}&limit={}"
    total_pages = int(math.ceil(int(rows) / int(limit)))
    current_page = _compute_page(offset, limit)

    # Links
    current = OrderedDict()
    first = OrderedDict()
    prev = OrderedDict()
    next = OrderedDict()
    last = OrderedDict()
    links = []

    current["rel"] = "self"
    current["href"] = url_link.format(endpoint, offset, limit)
    links.append(current)

    first["rel"] = "first"
    first["href"] = url_link.format(endpoint, _compute_offset(1, limit), limit)
    links.append(first)

    if current_page > 1:
        prev["rel"] = "prev"
        prev["href"] = url_link.format(
            endpoint, _compute_offset(current_page - 1, limit), limit
        )
        links.append(prev)

    if current_page < total_pages:
        next["rel"] = "next"
        next["href"] = url_link.format(
            endpoint, _compute_offset(current_page + 1, limit), limit
        )
        links.append(next)

    last["rel"] = "last"
    last["href"] = url_link.format(endpoint, _compute_offset(total_pages, limit), limit)
    links.append(last)

    return links


def build_json_from_object(obj: object, restricted_fields: list = []):
    resp = {
        key: value if value is not None else ""
        for key, value in obj.__dict__.items()
        if not key.startswith("_")
        and not callable(key)
        and key not in restricted_fields
    }
    return resp


# def validate_email(email_address):
#     """Rudimentary email address validator.

#     Args:
#         email_address (str): Email address string to validate.
#     Return:
#         bool: True if the email address is valid, False if not.
#     """
#     email_regex = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
#     is_valid = False

#     if email_regex.match(email_address):
#         is_valid = True

#     return is_valid
