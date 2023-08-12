import random
import re
import textwrap
from io import BytesIO
import string
from string import ascii_letters

import moviepy.audio.fx.all as afx
import moviepy.video.VideoClip
import requests
from PIL import Image, ImageFont, ImageDraw, ImageFilter
from bs4 import BeautifulSoup
from deep_translator import GoogleTranslator
from moviepy.editor import *
import moviepy.editor

from selenium import webdriver
import collections

from time import sleep

def createAVideo(index_images_video, amount_video, index_video):
    # Selecting the images
    dir_path = r'C:\Users\georg\PycharmProjects\videoMaker\images'
    result_images = []
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            result_images.append('images\\' + path)
    #print(result_images)

    # Selecting the songs
    dir_path_music = r'C:\Users\georg\PycharmProjects\videoMaker\songs'
    result_songs = []
    for path in os.listdir(dir_path_music):
        if os.path.isfile(os.path.join(dir_path_music, path)):
            result_songs.append(path)

    sequence_result_images = []

    if (index_video * amount_video <= len(result_images)):
        if (index_video == 0):
            sequence_result_images = result_images[index_images_video:amount_video]
        else:
            sequence_result_images = result_images[index_images_video:amount_video*index_video]
    else:
        sequence_result_images = result_images[index_images_video:len(result_images)]
    print(f'sequence_result_images: ', sequence_result_images)

    durations_list = [17] * len(sequence_result_images)
    
    # Choose the amount of images to make a video => result_images[0:20]
    clip = ImageSequenceClip(sequence=sequence_result_images, durations=durations_list) #fps=0.01 == 200s
    musicToClip = AudioFileClip(f'songs/{random.choice(result_songs)}')
    audioclip = afx.audio_loop(musicToClip, duration=clip.duration)
    audioclipFadeOut = afx.audio_fadeout(audioclip, 10)
    audioclipFadeInOut = afx.audio_fadein(audioclipFadeOut, 2)

    clip = clip.set_audio(audioclipFadeInOut)
    #clip.ipython_display(width=360)
    clip.write_videofile(f"video{index_video}.mp4", fps=30)
    audioclip.close()
    clip.close()
    print(f'Video {index_video} created! :)')
    #audioclip.reader.close()
    #clip.reader.close()


def createAShort(index_images_video, amount_video, index_video):
    # Selecting the images
    dir_path = r'C:\Users\georg\PycharmProjects\videoMaker\images'
    result_images = []
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            result_images.append('images\\' + path)
    # print(result_images)

    # Selecting the songs
    dir_path_music = r'C:\Users\georg\PycharmProjects\videoMaker\songs'
    result_songs = []
    for path in os.listdir(dir_path_music):
        if os.path.isfile(os.path.join(dir_path_music, path)):
            result_songs.append(path)

    sequence_result_images = []

    if (index_video * amount_video <= len(result_images)):
        if (index_video == 0):
            sequence_result_images = result_images[index_images_video:amount_video]
        else:
            sequence_result_images = result_images[index_images_video:amount_video * index_video]
    else:
        sequence_result_images = result_images[index_images_video:len(result_images)]
    print(f'sequence_result_images: ', sequence_result_images)

    durations_list = [9] * len(sequence_result_images)

    # Choose the amount of images to make a video => result_images[0:20]
    clip = ImageSequenceClip(sequence=sequence_result_images, durations=durations_list).resize((1080, 1080))  # fps=0.01 == 200s
    musicToClip = AudioFileClip(f'songs/{random.choice(result_songs)}')
    audioclip = afx.audio_loop(musicToClip, duration=clip.duration)
    #audioclipFadeOut = afx.audio_fadeout(audioclip, 10)
    #audioclipFadeInOut = afx.audio_fadein(audioclipFadeOut, 2)

    #clip = clip.set_audio(audioclipFadeInOut)
    clip = clip.set_audio(audioclip)

    # clip.ipython_display(width=360)
    clip.write_videofile(f"short{index_video}.mp4", fps=30)
    audioclip.close()
    clip.close()
    print(f'Short {index_video} created! :)')

    # Adding a gif in the video
    video = VideoFileClip(f"short{index_video}.mp4")

    #interactions_youtube = r"assets/videos/interactions_youtube.gif"
    interactions_youtube = r"assets/videos/interacoes_youtube.gif"

    gif = VideoFileClip(interactions_youtube, has_mask=True).loop().set_duration(video.duration)\
        .resize(width=video.w)\
        .set_pos(("center", "top"))
        #.margin(left=8, top=8, opacity=0)\

    final_video = CompositeVideoClip([video, gif])

    final_video.write_videofile(f"short{index_video}WithCTA.mp4", fps=video.fps)

    # audioclip.reader.close()
    # clip.reader.close()

def countWordsQuote(str_quote):
    return len(str_quote.split())

def downloadImagesToCreateImageQuote():
    print('===== Starting downloadImagesToCreateImageQuote()')
    amount_images = 0
    while amount_images < 250:
        print(f'Downloading image {amount_images}')
        response = requests.get("https://picsum.photos/1920/1270/?blur").content
        if b'Something went wrong. Timed out.' in response:
            sleep(3)
            continue
        else:
            with open(f'assets/images/images_to_use/image_{amount_images}.jpg', 'wb') as handler:
                handler.write(response)
            amount_images += 1

        sleep(1.5)

def createImageQuote(quotesAuthorObject):
    print('===== Starting createImageQuote()')
    # https://stackoverflow.com/questions/67473444/how-to-make-text-shadow-effect-in-pillow-python
    # https://jdhao.github.io/2020/08/18/pillow_create_text_outline/
    # https://pixabay.com/api/docs/

    # THIS IS THE PROBLEM SOLVE
    # https://www.alpharithms.com/fit-custom-font-wrapped-text-image-python-pillow-552321/
    #print(textQuote)
    dir_path = r'assets\fonts'
    result_fonts = []
    for path in os.listdir(dir_path):
        result_fonts.append(path)

    images_dir_path = r'assets\images\images_to_use'
    result_images = []
    for path in os.listdir(images_dir_path):
        image_path = f'assets/images/images_to_use/{path}'

        try:
            image_file = Image.open(image_path)
            if (image_file):
                result_images.append(f'assets/images/images_to_use/{path}')
        except(IOError, SyntaxError):
            print('Image is corrupted')
            print(f'IOError: {IOError}')
            print(f'SyntaxError: {SyntaxError}')


    #print(f'result_fonts: {result_fonts}')
    index_image = 0

    for obj in quotesAuthorObject:
        if countWordsQuote(obj['quote']) <= 35:
            print(f'Creating the image {index_image}')
            choose_image_random = random.choice(result_images)
            #if index_image % 2 == 0:
            #    response = requests.get("https://picsum.photos/1920/1270/?blur")
            #else:
            #    response = requests.get("https://placeimg.com/1920/1270/arch")
            #my_image = Image.open("assets/images/image1.jpg")
            #print(f'Image response: {response}')
            #get_image_from_response = BytesIO(response.content)

            my_image = Image.open(choose_image_random)

            #logo_image = Image.open("assets/images/logo.png")
            logo_image = Image.open("assets/images/logo_english.png")
            #logo_image = Image.open("assets/images/logo_crista.png")

            logo_image = logo_image.convert("L")
            threshold = 50
            logo_image = logo_image.point(lambda x: 255 if x > threshold else 0)
            logo_image = logo_image.resize((logo_image.width // 2, logo_image.height // 2))
            logo_image = logo_image.filter(ImageFilter.CONTOUR)
            logo_image = logo_image.point(lambda x: 0 if x == 255 else 255)

            font_size = 120
            img_fraction = 0.50

            choose_font_random = random.choice(result_fonts)

            quote_font = ImageFont.truetype("assets/fonts/MahoneSansBold.ttf", font_size)  # 120

            avg_char_width = sum(quote_font.getsize(char)[0] for char in ascii_letters) / len(ascii_letters)
            max_char_count = int((my_image.size[0] * .95) / avg_char_width)
            text = textwrap.fill(text=obj['quote'], width=max_char_count)

            quote_text = text
            r"""
                File "C:\Users\georg\PycharmProjects\videoMaker\venv\lib\site-packages\PIL\ImageFont.py", line 454, in getsize
                size, offset = self.font.getsize(text, "L", direction, features, language)
                OSError: invalid argument
            """
            while quote_font.getsize(quote_text)[0] < img_fraction * my_image.size[0]:
                font_size -= 1
                quote_font = ImageFont.truetype("assets/fonts/MahoneSansBold.ttf", font_size, layout_engine=ImageFont.LAYOUT_BASIC)

            font_size += 2
            quote_font = ImageFont.truetype("assets/fonts/MahoneSansBold.ttf", font_size)
            author_quote_font = ImageFont.truetype(f"assets/fonts/{choose_font_random}", font_size - 15)

            x = my_image.size[0] / 2
            y = my_image.size[1] / 2

            position_logo = (int(x) + 700, int(y) + 400)

            my_image.paste(logo_image, position_logo, logo_image)

            blur_image = my_image.filter(ImageFilter.BLUR)
            image_editable = ImageDraw.Draw(blur_image)

            image_editable.text(xy=(x, y), text=quote_text, anchor="mm",  font=quote_font, stroke_width=4, stroke_fill="black", fill=(237, 230, 211),
                                )  # (Starting_Coordinates, Text, Text_Color_RGB_Format, Font_style)

            image_editable.text(xy=(x, y + 550), text=obj['author'], anchor="ms", font=author_quote_font, stroke_width=4,
                                stroke_fill="white", fill=(0, 0, 0),
                                )

            nameOfFile = f"result{index_image}.jpg"

            blur_image.save(f"images/{nameOfFile}")
            index_image += 1
            sleep(1)

def removeAuthorFromQuote(textQuote):
    findAuthorIndex = textQuote.rindex(chr(8213))
    onlyTextQuote = textQuote[:findAuthorIndex]

    return onlyTextQuote

def getAmountOfPages(URL):
    req = requests.get(URL + '1')
    soup = BeautifulSoup(req.text, 'lxml')
    total_items = soup.find('span', {'class': 'previous_page disabled'}).find_parent().find_all('a')
    last_number_total = total_items[-2].text

    return int(last_number_total) - 1

def makeScraping(URL, language):
    print('===== Starting makeScraping()')

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    quotes = []
    authorQuotes = []

    numberOfQuotesFile = 1
    amountPages = getAmountOfPages(URL)
    #print(f'amountPages: {amountPages}')

    for page in range(1, amountPages // 2):
        print(f'\rWebScraping - Page: {page}\r')
        req = requests.get(URL + str(page))  # Christian-living

        soup = BeautifulSoup(req.text, 'lxml')

        for a in soup.find_all('div', class_='quoteText'):
            textQuote = a.getText()
            authorQuote = a.find('span', class_='authorOrTitle')
            # print("author: ", authorQuote.getText())
            authorQuoteWithoutPunctuation = re.sub(r'[^a-zA-Z]', " ", authorQuote.getText())
            getOnlyText = re.sub(r'"(.*?)"', " ", textQuote)
            textWithoutCDATA = getOnlyText.split("//<![", 1)
            newTextQuote = re.sub(r"\n", "", textWithoutCDATA[0])
            newTextQuoteWithoutQuotes = removeAuthorFromQuote(newTextQuote)

            if language == 'pt':
                # Translate to Portuguese
                translateTextQuote = GoogleTranslator(source="en", target="pt").translate(newTextQuoteWithoutQuotes)
            else:
                # English only
                translateTextQuote = newTextQuoteWithoutQuotes

            quotes.append(translateTextQuote)
            authorQuotes.append(authorQuoteWithoutPunctuation)
            numberOfQuotesFile = numberOfQuotesFile + 1

    #print(quotes)
    #print(len(quotes))

    return quotes, authorQuotes

def saveInsideTxt(quotes, author_quotes, name_file):
    with open(f'{name_file}.txt', 'w', encoding='utf-8') as f:
        i = 0
        for line in quotes:
            print('line: ' + line)
            f.write(str(i + 1) + ' - ' + line)
            #f.write('\nAutor Original: ' + author_quotes[i])
            f.write('\nAuthor: ' + author_quotes[i])
            f.write('\n\n')
            i = i + 1

def createTagsFromText(quotes, author_quotes, index_tags_video, video_type):
    # Portuguese Tags
    '''
    tags_example = ["frases", "reflexão", "refletir", "vida", "amor", "para refletir", "citaçoes", "citacoes",
                   "profundo", "FRASES DE SABEDORIA", "MOTIVAÇÃO", "REFLEXÃO", "sabedoria"]
    '''

    # Christian Tags
    '''
    tags_example = ["FrasesCristas", "InspiraçãoCrista", "PalavraDeDeus", "VersículosBíblicos", "MotivaçãoCrista",
                    "CrescimentoEspiritual", "Oracao", "Fe", "AmorDeDeus", "Jesus", "Bíblia",
                    "Evangelho", "Gratidao", "PazInterior", "ComunidadeCrista"]
    '''
    # English Tags
    '''
    tags_example = ["wisdom", "lifeadvice", "philosophy", "mindfulness", "selfimprovement", "success", "happiness", "Motivation",
                    "inspiration", "mentalhealth", "personaldevelopment", "positivity", "selfhelp", "awareness",
                    "consciousness", "selfdiscovery", "enlightenment", "wellness", "innerpeace"]
     '''

    # Tags Motivacionais
    tags_example = ["Motivação", "Inspiração", "Autoaperfeiçoamento", "Foco", "Persistência", "Determinação", "Sucesso",
                    "MentalidadePositiva",
                    "DesenvolvimentoPessoal", "Autoconfiança", "Metas", "Produtividade", "SuperandoDesafios", "Conquistas",
                    "Vencedor", "ForçaDeVontade", "Coragem", "AtitudePositiva", "EstiloDeVidaSaudável", "BemEstar"]


    quotes_together = " ".join(quotes)
    split_it = quotes_together.split()
    Counter = collections.Counter(split_it)
    most_occur = Counter.most_common(50)
    tags_total = author_quotes

    for occur in most_occur:
        tags_total.append(occur[0])

    #print(f'most_occur: {most_occur}')

    allTags = []

    for line in tags_total:
        for tag in tags_example:
            elementTag = string.capwords(f'{tag} de {line}').replace(" ", "")

            allTags.append(elementTag)

    unique_values_tags_total = (list(set(allTags)))

    with open(f'tags{video_type}{index_tags_video}.txt', 'w', encoding="utf-8") as f:
        i = 1

        for elementTag in unique_values_tags_total:
                f.write(f'#{elementTag}, ')
                i += 1

    with open(f'authors{video_type}{index_tags_video}.txt', 'w', encoding="utf-8") as f:
        i = 1

        for author in author_quotes:
                f.write(f'#{author}, ')
                i += 1

def progress_bar(prefix, progress, total):
    percent = 100 * (progress / float(total))
    bar = '>' * int(percent) + '-' * (100 - int(percent))
    print (f"\r{prefix}: |{bar}| {percent:.2f}%", end="\r")


def get_quotes_from_text_file(name_file):
    with open(f'{name_file}.txt', encoding='utf8') as text_file:
        index = 1
        lines = text_file.readlines()

        only_quotes_and_authors = [i for i in lines if i != '\n']

        quotes = []
        author_quotes = []

        for quote in only_quotes_and_authors:
            if index % 2 == 1:
                get_only_quote = quote.split('-')[-1].strip()

                # quotes
                quotes.append(get_only_quote)
            else:
                get_only_author = quote.split(':')[-1].strip()

                # authors
                author_quotes.append(get_only_author)

            index += 1

    return quotes, author_quotes


def main():
    URL = "https://www.goodreads.com/quotes/tag/christian-living?page="
    URL1 = "https://www.goodreads.com/quotes/tag/wisdom?page="
    URL2 = "https://www.goodreads.com/quotes/tag/believe?page="
    URL3 = "https://www.goodreads.com/quotes/tag/inspirational?page="
    URL4 = "https://www.goodreads.com/quotes/tag/life-lessons?page="
    # https://goquotes.docs.apiary.io/#reference/get-random-quote(s)/apiv1random/get-random-quote(s)?console=1
    # https://zenquotes.io/

    # File Names
    # name_file = 'citacoesDeSabedoriaEmPortugues'
    # name_file = 'citacoesCristasEmPortugues'
    #name_file = 'wisdomQuotesInEnglish'
    name_file = 'citacoesInspiradoras'

    # Get Quotes from Web Scraping
    quotes, author_quotes = makeScraping(URL3, 'pt')

    # Get Quotes from file
    #quotes, author_quotes = get_quotes_from_text_file(name_file)

    array_quotes_author = [{"quote": quote, "author": author} for quote, author in zip(quotes, author_quotes)]
    print(f"Quotes: {array_quotes_author}")

    saveInsideTxt(quotes, author_quotes, name_file)

    type_video = 'SHORTS'

    createTagsFromText(quotes, author_quotes, 1, type_video)

    #downloadImagesToCreateImageQuote()

    createImageQuote(array_quotes_author)

    dir_path = r'assets/images/images_to_use'
    print(f'dir_path: {os.listdir(dir_path)} ')

    amount_images_to_video = len(os.listdir(dir_path))

    print(f'quotes: {quotes}')
    print(f'author_quotes: {author_quotes}')

    # Amount of images to show in video
    # ORDINARY VIDEO
    #amount_video = 20
    #type_video = 'VIDEO'

    # SHORTS
    amount_video = 6

    index_to_video = 1
    for index in range(0, amount_images_to_video, amount_video): #0, 29, 10
        print(f'Amount Images To Video: {amount_images_to_video}')

        print(f'Index: {index}')
        print(f'Amount {type_video}: {amount_video}')
        print(f'Index to {type_video}: {index_to_video}')

        if (index_to_video * amount_video <= amount_images_to_video):
            createTagsFromText(quotes[index:index_to_video*amount_video], author_quotes[index:index_to_video*amount_video], index_to_video, type_video)
        else:
            createTagsFromText(quotes[index:amount_images_to_video], author_quotes[index:amount_images_to_video], index_to_video, type_video)

        if type_video == 'VIDEOS':
            createAVideo(index, amount_video, index_to_video)
        else:
            createAShort(index, amount_video, index_to_video)

        index_to_video += 1

main()

#get_quotes_from_text_file('wisdomQuotesInEnglish')
