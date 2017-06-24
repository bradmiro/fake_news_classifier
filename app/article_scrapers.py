from datetime import datetime
from lxml import html
import requests


def download_data(url):
    """ Download the HTML from the provided url.

    http://docs.python-requests.org/en/master/user/quickstart/

    :param url: String of the url
    :return: String of the raw HTML
    """

    raw_html = requests.get(url).content
    html_string = html.fromstring(raw_html)
    return html_string


def bloomberg_article(raw_html):
    """
    Article parameters:
    source, author, date, text, title, images
    """

    article_params = {'source': 'bloomberg',
                      'author': '',
                      'date': '',
                      'text': '',
                      'title': '',
                      'images': [],
                      }
    
    # Parse the article's author
    for obj in raw_html.xpath("//address[@class='lede-text-only__byline']"):
        obj_text = obj.text_content()
        if obj_text[:2].lower() == 'by':
            author = obj_text[3:obj_text.find('\n')]
            article_params['author'] = author

    # Parse the published date
    date_obj = raw_html.xpath("//time[@class='article-timestamp']/@datetime")[0]
    date = datetime.strptime(date_obj[:-5], '%Y-%m-%dT%H:%M:%S')
    article_params['date'] = date
    
    # Parse all article paragraphs out
    for paragraph_obj in raw_html.xpath("//div[@class='body-copy']/p"):
        article_params['text'] += ' ' + paragraph_obj.text_content().strip()

    # Parse article title
    title_obj = raw_html.xpath("//span[@class='lede-text-only__highlight']")[0]
    title_text = title_obj.text_content().strip()
    article_params['title'] = title_text

    # Parse images from article
    image_obj = raw_html.xpath("//img[@class='lazy-img__image']/@data-native-src")
    article_params['images'] = image_obj

    return article_params


if __name__ == '__main__':

    test_url = 'https://www.bloomberg.com/news/articles/2017-06-23/trump-didn-t-record-comey-white-house-tells-house-intel-panel'

    test_article_html = download_data(url=test_url)
    test_article_params = bloomberg_article(raw_html=test_article_html)
    print(test_article_params)
