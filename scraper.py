from bs4 import BeautifulSoup
import requests
import re #regex
from PIL import Image, ImageDraw, ImageFont
import textwrap
from gtts import gTTS #text to speech
import sys #cmd arguments
from mutagen.mp3 import MP3 #get audio durations


video_name = sys.argv[1]
url = sys.argv[2]
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
page = requests.get(url, headers=headers)

#slide class
class Slide:
    duration = 3
    def __init__(self, index, title, content):
        self.index = index
        self.title = title
        self.content = content
    

#web scraping, this stuff is specific to the website, feel free to change
print(page.status_code)
soup = BeautifulSoup(page.content, 'html.parser')
title = soup.find('h1').contents[0]

#assuming 1 intro paragraphs
preview = soup.findAll('p')[1].text

#removing promo
for div in soup.find_all("p", {'class':'promote'}): 
    div.decompose()

#slide titles
h2_items = soup.find_all('h2')
item_titles = []

for item in h2_items:
    title_text = item.text
    title_text = title_text.replace(' ', '. ', 1)
    item_titles.append(title_text)

#removing junk
p_items = soup.find_all('p')

for p in p_items:
    if len(p.text) == 0:
        p_items.remove(p)

p_items.pop(0)
p_items.pop(0)
p_items.pop(0)
del p_items[-1]
del p_items[-1]


item_contents = []
for i,k in zip(p_items[0::2], p_items[1::2]):
    para_content = i.text + "\n" + k.text
    para_content = re.sub('\[[0-9]+\]', '', para_content) #removing citations
    item_contents.append(para_content)

#creating slides
slides = []
#creating intro slide
intro_slide = Slide(0, title, preview)
#creating outro slide
outro_slide = Slide(11, "Thank you for watching!", "Please Like & Subscribe!")

slides.append(intro_slide)
for i in range(1, 11):
    slide = Slide(i, item_titles[i-1], item_contents[i-1])
    slides.append(slide)
slides.append(outro_slide)

#creating images for slides
font = ImageFont.truetype("arial.ttf", 60)

i = 0
for slide in slides:
    i = i+1
    if i == 1 or i == 12:
        img = Image.new('RGB', (632, 420), 'white')
    else:
        img = Image.new('RGB', (632, 420), (222,222,200))
    lines = textwrap.wrap(slide.title, width=20) #multi line title
    y_text = 80
    draw = ImageDraw.Draw(img)
    for line in lines:
        w, h = font.getsize(line)
        draw.text(((632 - w) / 2, y_text), line, font=font, fill="black")
        y_text += h     
    img.save("E:/youtube-generator/"+video_name+"/images/" + str(i) + ".jpg")


#generating audio files, durations and blueprint

text_file = open(""+video_name+"/input.txt", "w")
audio_list = open(""+video_name+"/audio.txt", "w")
i = 0
for slide in slides:
    i = i + 1
    tts = gTTS(text=slide.content, lang='en')
    tts.save("E:/youtube-generator/"+video_name+"/audio/" + str(i) + ".mp3")
    #get durations here
    audio = MP3("E:/youtube-generator/"+video_name+"/audio/" + str(i) + ".mp3")
    slide.duration = audio.info.length
    #write audio clips
    audio_list.write("file " + "'audio/" + str(i) + ".mp3'")
    audio_list.write("\n")
    #write video clips
    text_file.write("file " + "'images/" + str(i) + ".jpg'")
    text_file.write("\n")
    text_file.write("duration " + str(slide.duration))
    text_file.write("\n")
text_file.write("file " + "'images/" + str(12) + ".jpg'")        
text_file.close()