from airium import Airium

menu_items = [
    {"name": 'Experience', "path": '/experience/'},
    {"name": 'Services', "path": '/services/'},
    {"name": 'Blog', "path": '/blog/'},
    {"name": 'Privacy Policy', "path": '/privacy-policy/'},
]


def navigation_menu(a: Airium, entry):
    with a.ul(klass="navigation"):
        for item in menu_items:
            if entry['page']['relativePath'] == item['path']:
                a.li(_t=item['name'])
            else:
                with a.li():
                    a.a(_t=item['name'], href=item['path'])
    return
