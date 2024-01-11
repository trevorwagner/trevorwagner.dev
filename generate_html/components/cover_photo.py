from airium import Airium


def cover_photo(a: Airium, entry):
    with a.div(klass="cover-photo"):
        a.img(src=entry['coverPhoto']['url'])
        with a.p(_t="Photo by "):
            a.a(_t=entry['coverPhoto']['author']['username'],
                href="{}?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash".format(
                    entry['coverPhoto']['author']['profile']),
                target="blank")
            a(" on ")
            a.a(_t='Unsplash', href='{}?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash'.format(
                entry['coverPhoto']['source']),
                target="blank"
                )

    return
