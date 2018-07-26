from flask import Flask, jsonify, request, redirect, render_template, url_for, send_from_directory
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def homepage():
    list_url = 'https://www.mangapanda.com/actions/selector/?id=103&which=409741'
    chapter_list = requests.get(list_url).json()
    base_url = request.host_url
    string = '<ul>{}</ul>'.format(''.join(['<li><a href="{}">{}</a></li>'.format(base_url + c.get('chapter') + '/1',c.get('chapter')+' - '+c.get('chapter_name')) for c in chapter_list[-10:]]))
    return string

@app.route('/<chapter>/<page>')
def render_page(chapter=900, page=1):
    url = 'https://www.mangapanda.com/one-piece/' + str(chapter) + ('/' + str(page) if int(page)>1 else '')
    html = requests.get(url).text
    server_url = request.host_url
    soup = BeautifulSoup(html, 'html.parser')
    img_url =soup.find('img', {'id':'img'}).get('src')
    return '<div><a href="{prev}">prev</a> <a href="{next}">next</a></div><a href={next}><img src={cur} style="width=100%;height=auto;"/></a>'.format(prev=server_url+str(chapter)+'/'+str(int(page)-1), next=server_url+str(chapter)+'/'+str(int(page)+1), cur=img_url)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
