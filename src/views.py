import os
import requests
from bs4 import BeautifulSoup
from flask import g, redirect, render_template, url_for, send_from_directory

from src import app
from .models import Page

nb_chapters_to_display = 15


@app.route('/')
def homepage():
    list_url = 'https://www.mangapanda.com/actions/selector/?id=103&which=0'
    chapter_list = requests.get(list_url).json()
    display_links = [{'label': f"{c.get('chapter')} - {c.get('chapter_name')}",
                      'link': url_for('render_page', chapter=c.get('chapter'), page_no=1),
                      } for c in chapter_list[-nb_chapters_to_display:]]
    return render_template('homepage.html', display_links=display_links)


@app.route('/<chapter>')
def redirect_first_page(chapter):
    try:
        chapter = int(chapter)
    except ValueError:
        return redirect(url_for('homepage'))
    return redirect(url_for('render_page', chapter=chapter, page_no=1))


@app.route('/<chapter>/<page_no>')
def render_page(chapter=900, page_no=1):
    if page_no == '0':
        return redirect(url_for('homepage'))
    page = Page.query.filter_by(chapter=chapter, page_no=page_no).first()
    if page:
        img_url = page.url
    else:
        try:
            source_url = f'https://www.mangapanda.com/one-piece/{chapter}/{page_no}'
            html = requests.get(source_url).text
            soup = BeautifulSoup(html, 'html.parser')
            img_url = soup.find('img', {'id': 'img'}).get('src')
            page = Page(chapter, page_no, img_url)
            g.page = page
        except Exception:
            print('page_no', page_no)
            if page_no == '1':  # Probably a second redirect, get out of loop
                return redirect(url_for('homepage'))
            print('should not be here!')
            return redirect(url_for('render_page', chapter=int(chapter) + 1, page_no=1))
    return render_template('page.html',
                           previous_page=url_for('render_page', chapter=chapter, page_no=int(page_no) - 1),
                           next_page=url_for('render_page', chapter=chapter, page_no=int(page_no) + 1),
                           current_image_url=img_url,
                           current_page_title=f'Chapter {chapter} - Page {page_no}')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
