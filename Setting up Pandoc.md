alias pandock='docker run --rm -v "$(pwd):/data" -u $(id -u):$(id -g) pandoc/extra'

 pandock lab2.md -o lab2.pdf --from markdown --template eisvogel --syntax-highlighting=idiomatic

