#!/bin/sh
# Rebuild the case report PDF from docs/Case_Report.md  (needs pandoc + wkhtmltopdf)
cd "$(dirname "$0")/.."
pandoc docs/Case_Report.md -f markdown+pipe_tables+raw_html -t html5 -s --css style.css --metadata pagetitle="Bambinos AI PM Case" -o docs/_report.html
wkhtmltopdf --enable-local-file-access --disable-smart-shrinking --zoom 1.28 --page-size A4 -T 14mm -B 14mm -L 13mm -R 13mm --footer-center "Bambinos.live AI PM case  |  page [page] of [topage]" --footer-font-size 7 docs/_report.html docs/Case_Report.pdf
