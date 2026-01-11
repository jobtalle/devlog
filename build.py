import os
import re
import sys
from datetime import datetime

from PIL import Image

def compress_html(string):
    return re.sub("|".join(map(re.escape, ["    ", "\n"])), "", string)

def replace_multiple(string, table):
    return re.compile("|".join(map(re.escape, table.keys()))).sub(lambda match: table[match.group(0)], string)

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
regex_header = re.compile("<h2[^>]*>(.*?)</h2>")
template = open("template/template.html", "r").read()
template_index = open("template/template_index.html", "r").read()
template_rss = open("template/template_rss.xml", "r").read()
template_rss_item = open("template/template_rss_item.xml", "r").read()
style = replace_multiple(open("template/style.css", "r").read(),
    {
        ": ": ":",
        ", ": ",",
        " {": "{"
    })

def process_post(string, post, date):
    string = replace_multiple(string, {
        "src=\"": f"src=\"posts\\{post}\\",
        "</h2>": f"</h2><h3>{date}</h3>"
    })

    def add_image_dimensions(match):
        src_attr = match.group(0)
        src_path = match.group(1)

        if src_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
            try:
                with Image.open(src_path) as img:
                    width, height = img.size
                    return f'{src_attr} width="{width}" height="{height}"'
            except (OSError, IOError):
                pass

        return src_attr

    string = re.sub(r'src="([^"]*)"', add_image_dimensions, string)

    return string

def print_posts(selective = None):
    posts = sorted(os.listdir("posts/"), reverse = True)
    post_index = ""
    post_years = []
    post_dates = []
    post_links = []
    post_html = []
    rss_items = []

    for index, post in enumerate(posts):
        date = regex_title.search(post)
        post_years.append(int(date[1]))
        post_dates.append(months[int(date[2]) - 1] + " " + date[1])
        post_html.append(open("posts/" + post + "/content.html").read())
        post_links.append("<li><a title=\"%s\" href=\"%s\">%s</a></li>" % (
            regex_header.search(post_html[index])[1],
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
        output_name = post + ".html"

        if selective is not None and output_name != selective:
            continue

        if os.path.exists(output_name):
            os.remove(output_name)

        with open(output_name, "w") as file:
            post_index = ""

            for link_index, link in enumerate(post_links):
                if link_index > 0 and post_years[link_index - 1] != post_years[link_index]:
                    post_index += "<li><hr></li>"

                post_index += link if index != link_index else "<li>%s</li>" % post_dates[link_index]

            post_index += "<hr>"

            file.write(compress_html(replace_multiple(template,
                {
                    "$index$": post_index,
                    "$title$": post_dates[index],
                    "$style$": style,
                    "$post$": process_post(post_html[index], post, post_dates[index]),
                    "$previous$": "<span class=\"previous\"><a href=\"%s\">%s</a></span>" % (
                        posts[index + 1] + ".html",
                        "<< previous") if index < len(posts) - 1 else "",
                    "$next$": "<span class=\"next\"><a href=\"%s\">%s</a></span>" % (
                        posts[index - 1] + ".html",
                        "next >>") if index > 0 else "",
                    "$year$": str(datetime.now().year)
                })))
            file.close()

    with open("index.html", "w") as file:
        file.write(compress_html(template_index.replace("$index$", posts[0] + ".html")))
        file.close()

    with open("rss.xml", "w") as file:
        file.write(compress_html(template_rss.replace("$items$", "".join(rss_items))))
        file.close()

print_posts(sys.argv[1] if len(sys.argv) > 1 else None)