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

def make_file(post, index):
    return "index.html" if index == 0 else post + ".html"

def print_posts():
    posts = sorted(os.listdir("posts/"), reverse = True)

    for index, post in enumerate(posts):
        with open(make_file(post, index), "w") as file:
            date = regex_title.search(post)
            title_date = months[int(date[2]) - 1] + " " + date[1]

            table = {
                "$title$": title + title_date,
                "$date$": title_date,
                "$content$": open("posts/" + post + "/content.html").read(),
                "$previous$": "<a href=\"%s\"><span class=\"previous\"></span></a>" % (
                    make_file(posts[index + 1], index + 1)) if index < len(posts) - 1 else "",
                "$next$": "<a href=\"%s\"><span class=\"next\"></span></a>" % (
                    make_file(posts[index - 1], index - 1)) if index > 0 else "",
            }
            pattern = re.compile("|".join(map(re.escape, table.keys())))

            def replace(match):
                return table[match.group(0)]

            file.write(pattern.sub(replace, template))
            file.close()

def clear_pages():
    for file in os.listdir("."):
        if file.endswith(".html"):
            os.remove(file)

clear_pages()
print_posts()