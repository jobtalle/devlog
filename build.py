import os
import re

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
template_index = open("template/template_index.html", "r").read()

def compress_html(string):
    return re.sub("|".join(map(re.escape, ["    ", "\n"])), "", string)

def print_posts():
    posts = sorted(os.listdir("posts/"), reverse = True)
    post_index = ""
    post_dates = []
    post_links = []

    for index, post in enumerate(posts):
        date = regex_title.search(post)
        post_dates.append(months[int(date[2]) - 1] + " " + date[1])
        post_links.append("<li><a href=\"%s\">%s</a></li>" % (
            post + ".html",
            post_dates[index]))

    for index, post in enumerate(posts):
        with open(post + ".html", "w") as file:
            post_index = ""

            for link_index, link in enumerate(post_links):
                post_index += link if index != link_index else "<li>%s</li>" % post_dates[link_index]

            table = {
                "$index$": post_index,
                "$title$": "Koi Farm 2 blog | " + post_dates[index],
                "$date$": post_dates[index],
                "$post$": open("posts/" + post + "/content.html").read().replace("src=\"", "src=\"posts\\%s\\" % post),
                "$previous$": "<span class=\"previous\"><a href=\"%s\">%s</a></span>" % (
                    posts[index + 1] + ".html",
                    "<< previous") if index < len(posts) - 1 else "",
                "$next$": "<span class=\"next\"><a href=\"%s\">%s</a></span>" % (
                    posts[index - 1] + ".html",
                    "next >>") if index > 0 else "",
            }
            pattern = re.compile("|".join(map(re.escape, table.keys())))

            def replace(match):
                return table[match.group(0)]

            file.write(compress_html(pattern.sub(replace, template)))
            file.close()

    with open("index.html", "w") as file:
        file.write(compress_html(template_index.replace("$index$", posts[0] + ".html")))
        file.close()

def clear_pages():
    for file in os.listdir("."):
        if file.endswith(".html"):
            os.remove(file)

clear_pages()
print_posts()