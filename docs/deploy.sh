#!/bin/bash
mkdocs build
rm site/assets/javascripts/lunr/min/lunr.ar.min.js
rm site/assets/javascripts/lunr/min/lunr.da.min.js
rm site/assets/javascripts/lunr/min/lunr.de.min.js
rm site/assets/javascripts/lunr/min/lunr.du.min.js
rm site/assets/javascripts/lunr/min/lunr.es.min.js
rm site/assets/javascripts/lunr/min/lunr.fi.min.js
rm site/assets/javascripts/lunr/min/lunr.fr.min.js
rm site/assets/javascripts/lunr/min/lunr.hi.min.js
rm site/assets/javascripts/lunr/min/lunr.hu.min.js
rm site/assets/javascripts/lunr/min/lunr.it.min.js
rm site/assets/javascripts/lunr/min/lunr.ja.min.js
rm site/assets/javascripts/lunr/min/lunr.jp.min.js
rm site/assets/javascripts/lunr/min/lunr.nl.min.js
rm site/assets/javascripts/lunr/min/lunr.no.min.js
rm site/assets/javascripts/lunr/min/lunr.pt.min.js
rm site/assets/javascripts/lunr/min/lunr.ro.min.js
rm site/assets/javascripts/lunr/min/lunr.ru.min.js
rm site/assets/javascripts/lunr/min/lunr.sv.min.js
rm site/assets/javascripts/lunr/min/lunr.th.min.js
rm site/assets/javascripts/lunr/min/lunr.tr.min.js
rm site/assets/javascripts/lunr/min/lunr.vi.min.js
rm site/assets/javascripts/lunr/min/lunr.zh.min.js
rsync --recursive --delete --progress site code:/var/www/sqla-wrapper/
