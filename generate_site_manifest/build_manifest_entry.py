from re import match
from datetime import datetime
from pathlib import Path

from get_photo_details import query_photo_details


def get_page_type(path):
    f = ''
    page_type = ''

    try:
        f = match(r'.*/_static/(.*)/', path).group(1)
    except:
        f = '/'

    if f == 'posts':
        page_type = 'blogPost'
    elif f == 'pages':
        page_type = 'brochurePage'
    else:
        page_type = 'custom'

    return page_type


def get_relative_path(entry):
    page_type = entry['page']['type']
    relative_path = ''
    
    if page_type == 'blogPost':
        relative_path = '/blog/posts/{}/'.format(entry['slug'])
    elif entry['slug'] == 'index':
        relative_path = '/'
    else:
        relative_path = '/{}/'.format(entry['slug'])

    return relative_path


def build_manifest_entry(file_info):
    file_name = file_info['filePath']
    new_entry = {
        'slug': Path(file_name).stem,
        'file': {
            'fileName': file_name,
            'lastMod': file_info['lastMod']
        },
        'page': {
            'title': file_info['matter'][0]['title'],
            'type': get_page_type(file_name),
            'draft': file_info['matter'][0]['draft'],
        }
    }

    if new_entry['page']['type'] == 'blogPost':
        new_entry['page']['publishDate'] =\
            datetime.fromisoformat(file_info['matter'][0]['publishDate']).timestamp()
        new_entry['coverPhoto'] = query_photo_details(file_info['matter'][0]['coverPhoto'])

    new_entry['page']['relativePath'] = get_relative_path(new_entry)

    return new_entry
