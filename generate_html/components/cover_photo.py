from airium import Airium


def cover_photo(a: Airium, entry):
    with a.div(klass="mt-12"):
        a.img(src=entry['coverPhoto']['url'])
        with a.p(_t="Photo by ", klass="mt-2 mb-4"):
            a.a(_t=entry['coverPhoto']['author']['username'],
                href="{}?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash".format(
                    entry['coverPhoto']['author']['profile']),
                klass="text-zinc-500 underline hover:no-underline",
                target="blank")
            a(" on ")
            a.a(_t='Unsplash', href='{}?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash'.format(
                entry['coverPhoto']['source']),
                klass="text-zinc-500 underline hover:no-underline",
                target="blank"
                )

    return
