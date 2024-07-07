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
template_rss = open("template/template_rss.xml", "r").read()
template_rss_item = open("template/template_rss_item.xml", "r").read()

def compress_html(string):
    return re.sub("|".join(map(re.escape, ["    ", "\n"])), "", string)

def replace_multiple(string, table):
    return re.compile("|".join(map(re.escape, table.keys()))).sub(lambda match: table[match.group(0)], string)

def process_post(string, post, date):
    return replace_multiple(string,
        {
            "src=\"": "src=\"posts\\%s\\" % post,
            "</h2>": "</h2><h3>%s</h3>" % date
        })

def print_posts():
    posts = sorted(os.listdir("posts/"), reverse = True)
    post_index = ""
    post_dates = []
    post_links = []
    rss_items = []

    for index, post in enumerate(posts):
        date = regex_title.search(post)
        post_dates.append(months[int(date[2]) - 1] + " " + date[1])
        post_links.append("<li><a href=\"%s\">%s</a></li>" % (
            post + ".html",
            post_dates[index]))

        rss_table = {
            "$title": post_dates[index],
            "$link$": "https://devlog.koifarmgame.com/" + post + ".html",
            "$description$": "Koi Farm 2 devlog | " + post_dates[index]
        }

        def replace(match):
            return rss_table[match.group(0)]

        rss_pattern = re.compile("|".join(map(re.escape, rss_table.keys())))
        rss_items.append(rss_pattern.sub(replace, template_rss_item))

    for index, post in enumerate(posts):
        with open(post + ".html", "w") as file:
            post_index = ""

            for link_index, link in enumerate(post_links):
                post_index += link if index != link_index else "<li>%s</li>" % post_dates[link_index]

            file.write(compress_html(replace_multiple(template,
                {
                    "$index$": post_index,
                    "$title$": post_dates[index],
                    "$post$": process_post(open("posts/" + post + "/content.html").read(), post, post_dates[index]),
                    "$previous$": "<span class=\"previous\"><a href=\"%s\">%s</a></span>" % (
                        posts[index + 1] + ".html",
                        "<< previous") if index < len(posts) - 1 else "",
                    "$next$": "<span class=\"next\"><a href=\"%s\">%s</a></span>" % (
                        posts[index - 1] + ".html",
                        "next >>") if index > 0 else "",
                })))
            file.close()

    with open("index.html", "w") as file:
        file.write(compress_html(template_index.replace("$index$", posts[0] + ".html")))
        file.close()

    with open("rss.xml", "w") as file:
        file.write(compress_html(template_rss.replace("$items$", "".join(rss_items))))
        file.close()

def clear_pages():
    for file in os.listdir("."):
        if file.endswith(".html"):
            os.remove(file)

clear_pages()
print_posts()