all: index

index: index.md
	pandoc --from markdown --to html -c styles.css --standalone -V pagetitle:"`head -n1 index.md`" $< > static/index.html
