from string import Template

title = "Awesome title"
subtitle = "Even more awesome subtitle"
lst = ["1", "2", "3"]

sub = {"input": 1}  # { 'title':title, 'subtitle':subtitle, 'list':'\n'.join(lst) }

f = open("randomize_tmp.txt")
src = Template(f.read())
result = src.substitute(sub)

print(result)
