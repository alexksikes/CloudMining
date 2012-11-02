__author__ = 'Alex Ksikes <alex.ksikes@gmail.com>'

import urllib
import web


def get_paging(start, max_results, query=False, results_per_page=15,
    window_size=15, max_allowed_results=1000):
    max_allowed_pages = max_allowed_results / results_per_page

    c_page = start / results_per_page + 1
    if not start:
        c_page = 1
    nb_pages = max_results / results_per_page
    if max_results % results_per_page != 0:
        nb_pages += 1

    left_a = right_a = False
    if c_page > 1:
        left_a = (c_page - 2) * results_per_page
    if c_page < nb_pages:
        right_a = start + results_per_page
    if right_a > max_allowed_pages:
        right_a = False

    left = c_page - window_size / 2
    if left < 1:
        left = 1
    right = left + window_size - 1
    max_pages = (nb_pages > max_allowed_pages) and max_allowed_pages or nb_pages
    if right > max_pages:
        left = left - (right - max_pages)
        if left < 1:
            left = 1
        right = max_pages

    pages = []
    for i in range(left, right + 1):
        pages.append(web.storage(
            number=i,
            start=(i - 1) * results_per_page
        ))

    leftmost_a = rightmost_a = False
    if pages and pages[0].number > 1:
        leftmost_a = web.storage(number=1, start=0)
    if pages and pages[-1].number < nb_pages and nb_pages < max_allowed_pages:
        rightmost_a = web.storage(
            number=nb_pages, start=(nb_pages - 1) * results_per_page)

    return web.storage(
        start=start,
        max_results=max_results,
        c_page=c_page,
        nb_pages=nb_pages,
        pages=pages,
        leftmost_a=leftmost_a,
        left_a=left_a,
        right_a=right_a,
        rightmost_a=rightmost_a,
        query_enc=query and urllib.quote(query) or ''
    )
