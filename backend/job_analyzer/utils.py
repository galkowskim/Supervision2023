import base64
import io
import os
import urllib.parse
from typing import Any, List, Optional, Union
import matplotlib.pyplot as plt
import pandas as pd
from django.core.files.uploadedfile import UploadedFile
from PIL import Image
from wordcloud import STOPWORDS, WordCloud

stopwords = set(STOPWORDS)


def show_wordcloud(data, color='blanchedalmond'):
    try:

        wordcloud = WordCloud(background_color=color, max_words=200, max_font_size=40, random_state=0,
                              stopwords=stopwords, width=800, height=400)

        wordcloud.generate(str(data))
        plt.figure(figsize=(20, 10), facecolor='k')
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.tight_layout(pad=0)

        image = io.BytesIO()
        plt.savefig(image, format="jpg")

        image.seek(0)
        string = base64.b64encode(image.read())
        image_64 = "data:image/png;base64," + urllib.parse.quote_plus(string)
        return image_64
    except ValueError:
        return None


def plot_priority(data):
    try:
        labels = ['B. niski', 'Niski', 'Średni', 'Wysoki', 'B. wysoki']
        plt.figure(figsize=(20, 10), facecolor='white')
        plt.grid(color='grey', linestyle='-', linewidth=0.25, alpha=1)
        plt.bar(labels, data, color='orange', width=0.4, edgecolor='darkblue')
        plt.xlabel("Priorytet", fontsize=45)
        plt.ylabel("Liczba ogłoszeń", fontsize=45)
        plt.xticks(fontsize=30)
        plt.yticks(fontsize=30)
        image = io.BytesIO()
        plt.savefig(image, format="jpg")
        image.seek(0)
        string = base64.b64encode(image.read())
        image_64 = "data:image/png;base64," + urllib.parse.quote_plus(string)
        return image_64
    except ValueError:
        return None


def plot_fake(data):
    try:
        labels = ['Tak', 'Nie']
        plt.figure(figsize=(20, 10), facecolor='white')
        plt.grid(color='grey', linestyle='-', linewidth=0.25, alpha=1)
        plt.bar(labels, data, color='orange', width=0.4, edgecolor='darkblue')
        plt.xlabel("Czy oszustwo?", fontsize=45)
        plt.ylabel("Liczba ogłoszeń", fontsize=45)
        plt.xticks(fontsize=30)
        plt.yticks(fontsize=30)
        image = io.BytesIO()
        plt.savefig(image, format="jpg")
        image.seek(0)
        string = base64.b64encode(image.read())
        image_64 = "data:image/png;base64," + urllib.parse.quote_plus(string)
        return image_64
    except ValueError:
        return None
