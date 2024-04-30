timestamp:
	TZ=America/Chicago date -Iseconds

modtimes: 
	bash ./fix_modtimes.sh

clean:
	rm -fR ./_dist

manifest:
	python3 -m generate_site_manifest

rss: manifest
	python3 -m generate_rss_feed
	cp ./public/feed/index.php ./_dist/html/blog/feed/

sitemap: manifest
	python3 -m generate_xml_sitemap

pages: manifest
	python3 -m generate_html

site: manifest pages sitemap rss
	cp -R ./public/{.htaccess,css,js,images,robots.txt} ./_dist/html/

devserver:
	bash ./dev_server.sh


