venv:
	python3 -m venv venv
	source venv/bin/activate

clean: venv
	rm -fR ./_dist

ready: venv
	python3 -m pip install -r './requirements.txt'

manifest: ready
	python3 generate_site_manifest

rssFeed: manifest
	python3 generate_rss_feed

siteMap: manifest
	python3 generate_xml_sitemap


all: manifest generate_rss_feed generate_xml_sitemap