from airium import Airium

from xml.sax.saxutils import escape


def page_title(a: Airium, entry):
    if entry['slug'] == 'index':
        a.title(_t='Trevor Wagner | Project-Focused Software Engineer, QA Automation')
    else:
        if entry['page']['type'] == 'blogPost':
            a.title(_t='Blog Post: {} | Trevor Wagner'.format(escape(entry['page']['title'])))
        else:
            a.title(_t='{} | Trevor Wagner'.format(escape(entry['page']['title'])))

    return
