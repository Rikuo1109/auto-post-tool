from bs4 import BeautifulSoup
from markdown import markdown
import re


def markdown_to_text(markdown_string):
    """Converts a markdown string to plaintext"""
    html = markdown(markdown_string)

    html = re.sub(r"<pre>(.*?)</pre>", " ", html)
    html = re.sub(r"<code>(.*?)</code >", " ", html)

    soup = BeautifulSoup(html, "html.parser")
    text = "".join(soup.findAll(text=True))

    return text


markdown_text = """
**in dam**
*in nghieng*
#Title large
> Hello

"""

print(markdown_to_text(markdown_text))
