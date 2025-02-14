import pytest

from sqla_wrapper import Paginator, sanitize_page_number


def test_sanitize_page_number():
    assert sanitize_page_number("1") == 1
    assert sanitize_page_number("-1") == 1
    assert sanitize_page_number("0") == 1
    assert sanitize_page_number("3") == 3
    assert sanitize_page_number("asas") == 1
    assert sanitize_page_number(None) == 1


def test_properties():
    """The paginator is a helper class that can be used with any iterable
    object.
    """
    items = range(194)
    p = Paginator(items, page=5, per_page=10)

    assert p.page == 5
    assert p.is_paginated
    assert p.has_prev
    assert p.has_next
    assert p.total == 194
    assert p.num_pages == 20
    assert p.total_pages == 20
    assert p.prev_num == 4
    assert p.next_num == 6
    assert p.start_index == 40
    assert p.end_index == 49
    assert p.get_range() == "41 - 50"
    assert p.items == range(40, 50)


def test_not_paginated():
    items = range(5)
    p = Paginator(items, page="first", per_page=10)
    assert not p.has_prev
    assert not p.has_next
    assert not p.is_paginated


def test_first_page():
    items = range(194)
    p = Paginator(items, page="first", per_page=10)
    assert p.page == 1


def test_last_page():
    items = range(194)
    p = Paginator(items, page="last", per_page=10)
    assert p.page == p.num_pages


def test_prev_next_paginator():
    items = range(194)
    p = Paginator(items, page=5, per_page=10)

    assert p.next_num == 6


@pytest.mark.parametrize("page,expected", [
    (1, [1, 2, 3, 4, 5, 6, None, 10, 11, 12, 13, 14, 15]),
    (2, [1, 2, 3, 4, 5, 6, 7, None, 11, 12, 13, 14, 15]),
    (3, [1, 2, 3, 4, 5, 6, 7, None, 11, 12, 13, 14, 15]),
    (4, [1, 2, 3, 4, 5, 6, 7, 8, None, 12, 13, 14, 15]),
    (5, [1, 2, 3, 4, 5, 6, 7, 8, None, 12, 13, 14, 15]),
    (6, [1, 2, 3, 4, 5, 6, 7, 8, 9, None, 13, 14, 15]),
    (7, [1, 2, 3, 4, 5, 6, 7, 8, 9, None, 13, 14, 15]),
    (8, [1, 2, None, 5, 6, 7, 8, 9, 10, None, 13, 14, 15]),
    (9, [1, 2, 3, None, 6, 7, 8, 9, 10, 11, None, 14, 15]),
    (10, [1, 2, 3, None, 7, 8, 9, 10, 11, 12, 13, 14, 15]),
    (11, [1, 2, 3, 4, None, 8, 9, 10, 11, 12, 13, 14, 15]),
    (12, [1, 2, 3, 4, None, 8, 9, 10, 11, 12, 13, 14, 15]),
    (13, [1, 2, 3, 4, 5, None, 9, 10, 11, 12, 13, 14, 15]),
    (14, [1, 2, 3, 4, 5, None, 9, 10, 11, 12, 13, 14, 15]),
    (15, [1, 2, 3, 4, 5, 6, None, 10, 11, 12, 13, 14, 15]),
])
def test_paginator(page, expected):
    """The paginator is a helper class that can be used with any iterable
    object.
    """
    p = Paginator(range(148), page=page, per_page=10)
    pages = list(p.get_pages(showmax=12))
    print(pages)
    print(expected)
    assert pages == expected


def test_whith_manual_total():
    """Yes indeed, the paginator can be used too without anything to actually
    be paginated. How quaint!
    """
    p = Paginator(None, page=1, per_page=20, total=490)

    assert p.page == 1
    assert not p.has_prev
    assert p.has_next
    assert p.total == 490
    assert p.num_pages == 25
    assert p.next_num == 2


def test_bool_paginator():
    assert Paginator(range(5))
    assert not Paginator([])


def test_when_0_items_per_page():
    with pytest.raises(AssertionError):
        Paginator(range(200), per_page=0)


@pytest.mark.parametrize("showmax", range(4))
def test_when_0_showmax(showmax):
    p = Paginator(range(200))
    with pytest.raises(AssertionError):
        p.get_pages(showmax=showmax)


@pytest.mark.parametrize("page,expected", [
    (1, [1, 2, None, 19, 20]),
    (10, [1, None, 9, 10, None, 20]),
    (20, [1, 2, None, 19, 20]),
    (3, [1, 2, 3, None, 20]),
])
def test_small_showmax(page, expected):
    p = Paginator(range(196), per_page=10, page=page)
    assert p.get_pages(showmax=4) == expected


def test_looking_for_trouble():
    p = Paginator(range(5), per_page=1, page=3)
    assert p.get_pages(showmax=4) == [1, 2, 3, None, 5]

    p = Paginator(range(5), per_page=1, page=4)
    assert p.get_pages(showmax=4) == [1, None, 3, 4, 5]


def test_showing():
    query = [str(num) for num in range(1, 86)]

    p = Paginator(query, per_page=10, page=1, padding=2)
    print(p.items)
    assert p.total == 85
    assert p.showing == 12
    assert p.items[0] == "1"
    assert p.items[-1] == "12"

    p = Paginator(query, per_page=10, page=2, padding=0)
    print(p.items)
    assert p.showing == 10
    assert p.items[0] == "11"
    assert p.items[-1] == "20"

    p = Paginator(query, per_page=10, page=2, padding=2)
    print(p.items)
    assert p.showing == 14
    assert p.items[0] == "9"
    assert p.items[-1] == "22"

    p = Paginator(query, per_page=10, page=9, padding=0)
    print(p.items)
    assert p.showing == 5
    assert p.items[0] == "81"
    assert p.items[-1] == "85"

    p = Paginator(query, per_page=10, page=9, padding=2)
    print(p.items)
    assert p.showing == 7
    assert p.items[0] == "79"
    assert p.items[-1] == "85"
