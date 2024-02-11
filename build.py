import os
import re

title = "Koi Farm 2 blog | "
months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"]

regex_title = re.compile("(\d*)_0?(\d*)")

template = open("template/template.html", "r").read()
has_index = False

def make_title(post):
    date = regex_title.search(post)

    return title + months[int(date[2]) - 1] + " " + date[1]

def print_post(post):
    global has_index

    with open("index.html" if not has_index else post + ".html", "w") as file:
        table = {
            "$title$": make_title(post),
            "$content$": open("posts/" + post + "/content.html").read()
        }
        pattern = re.compile("|".join(map(re.escape, table.keys())))

        def replace(match):
            return table[match.group(0)]

        file.write(pattern.sub(replace, template))
        file.close()

    has_index = True

def print_posts():
    for post in sorted(os.listdir("posts/"), reverse = True):
        print_post(post)

def clear_pages():
    for file in os.listdir("."):
        if file.endswith(".html"):
            os.remove(file)

clear_pages()
print_posts()