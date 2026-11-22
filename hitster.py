import spotipy
from spotipy.oauth2 import SpotifyOAuth
import qrcode
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
import io
from datetime import datetime
import os
import json
from pathlib import Path



os.system("cls")

playlist_name = "HM"

playlists = {
            "(g)old":       "https://open.spotify.com/playlist/2z5Nv5wPAGjUKDZzBeJq3L?si=248c71376bff4943",
            "Spikeball":    "https://open.spotify.com/playlist/2s2PdHeaSNINXdLgXWtjMv?si=62fd240512df487c",
            "HF":           "https://open.spotify.com/playlist/3jSD9sSEPEn5w1TYrqoIGk?si=904cfdf21c9f44f4&pt=48e2f02d071dd454d845b406f7429ac0",
            "HJa":          "https://open.spotify.com/playlist/0mJp57O1Z9tOtQMp1ABwrY?si=9950d808584e491a",
            "HR":           "https://open.spotify.com/playlist/2uoCGdRkUWhxH1ZtfJopSO?si=1fe6bcca79984cb2",
            "HM":           "https://open.spotify.com/playlist/49XR4URAaZOQkFoKTuq9D6?si=1ec61eba78754f10",
            "HK":           "https://open.spotify.com/playlist/5defDRMAtRMVZOiCqBubDZ?si=ab3500c7cb1740d1",
            "test":         "https://open.spotify.com/playlist/60JZs4dAVFe5OgXcI8cWw5?si=cfabe21e170e439f",
            "HFi":          "https://open.spotify.com/playlist/1idyl1BeulpGHcUgtlR0wZ?si=5ec34c50f078450c"
            }


# Constants for layout
page_width, page_height = A4
print_margin = 4 * mm          # <--- NEW: 10mm margin on all sides

# New: Calculate actual usable space for cards
usable_width = page_width - (2 * print_margin)
usable_height = page_height - (2 * print_margin)

cols, rows = 3, 6               
cpp = cols*rows                 
card_width = usable_width / cols     # <--- UPDATED: Uses usable_width
card_height = usable_height / rows   # <--- UPDATED: Uses usable_height

qr_size = card_height*0.35      
margin_x = (card_width - qr_size) / 2
margin_y = (card_height - qr_size) / 2
std_line_limit = int(card_width/8*0.77) # for bigger cards 
std_fs = int(card_height*0.1)

simple_mode = True                     #simple mode to save printing costs
# simple_qr = True
simple_font = 'Courier'

lines_yes_no = False                    #other design choices
qr_bg = False
text_bg = True
random_colors = False                   #decide if colors should match song year
font = 'Courier'
add_dt_to_filename = False

card_nb = 250                           #number of songs to turn into cards (max 100)

data_path = Path(__file__).with_name("playlist_data.json")
with open(data_path, "r", encoding="utf-8") as f:
    playlist_data = json.load(f)

corrections = playlist_data.get("corrections", {})
exclude = playlist_data.get("exclude", {})

#available fonts:
#    "Courier", "Courier-Bold", "Courier-Oblique", "Courier-BoldOblique",
#    "Helvetica", "Helvetica-Bold", "Helvetica-Oblique", "Helvetica-BoldOblique",
#    "Times-Roman", "Times-Bold", "Times-Italic", "Times-BoldItalic",
#    "Symbol", "ZapfDingbats"
#

fields = "items(track(name,artists(name),album(release_date),external_urls(spotify),is_local,uri))"

if(add_dt_to_filename):
    file_name = f"hitster_cards_{playlist_name}_{datetime.now().strftime('%Y-%m-%d_%Hh%M')}.pdf"
else:
    file_name = f"hitster_cards_{playlist_name}.pdf"

class qr_bg_obj:
    def __init__(self, distance_to_qr, line_length, qr_size, pdf):
        self.e1 = distance_to_qr+qr_size/2
        self.l = line_length
        self.d = distance_to_qr
        self.pdf = pdf
        self.lw = 0.7
        self.qrs = qr_size

    def draw(self,x,y, design):
        match design:
            case 'corners':
                self.pdf.setFillColor('white')
                self.pdf.setLineCap(1)
                self.pdf.setLineWidth(self.lw)
                # self.pdf.setStrokeColorRGB(15/256, 70/256, 142/256)     #blue
                self.pdf.setStrokeColorRGB(12/256, 114/256, 114/256)     #turquoise
                self.pdf.rect(x-self.e1, y-self.e1, qr_size+2*self.d, qr_size+2*self.d, stroke = 1, fill = 0)
                self.pdf.rect(x-self.e1-self.lw, y-self.e1+self.l, qr_size+2*self.d+2*self.lw, qr_size+2*self.d-2*self.l, stroke = 0, fill = 1)
                self.pdf.rect(x-self.e1+self.l, y-self.e1-self.lw, qr_size+2*self.d-2*self.l, qr_size+2*self.d+2*self.lw, stroke = 0, fill = 1)

            case 'circles':
                # self.pdf.setFillColor('white')
                # self.pdf.setStrokeColor('white')
                # self.pdf.setLineWidth(0.5)
                # self.pdf.rect(x-margin_x, y-margin_y, card_width, card_height, stroke = 1, fill = 1)
                self.pdf.setStrokeColor('black')
                self.pdf.setLineCap(1)
                self.pdf.setLineWidth(self.lw)
                self.pdf.setStrokeColorRGB(15/256, 70/256, 142/256)
                for r in range(int(self.qrs/2*1.4142), int(min(card_height, card_width)/2), 15):
                    self.pdf.circle(x,y,r, stroke = 1, fill = 0)


# Spotify credentials and setup
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id='3cb78c8e36c144fbb79c974654f906bb',
    client_secret='25916ff55090410088036046f81d4441',
    redirect_uri='http://127.0.0.1:8888/callback',
    scope='user-read-playback-state user-modify-playback-state'
))

class tr:
    def __init__(self, title, artist, year, stdll, stdfs):
        self.year = year
        s = len(title)//stdll

        match (s):
            case 0:
                self.ll = stdll
            case 1:
                self.ll = int(stdll*1.2)
            case 2:
                self.ll = int(stdll*1.4)
            case 3:
                self.ll = int(stdll*1.6)
            case _:
                self.ll = int(stdll*1.8)

        self.tlist = cutter(title, self.ll)
        match len(self.tlist):
            case 1:
                self.t_offset = stdfs+2
                self.t_fs = stdfs
            case 2:
                self.t_offset = stdfs
                self.t_fs = stdfs-2
            case 3:
                self.t_offset = stdfs-2
                self.t_fs = stdfs-4
            case 4:
                self.t_offset = stdfs-4
                self.t_fs = stdfs-5
            case _:
                self.t_offset = stdfs-5
                self.t_fs = stdfs-6

        self.alist = cutter(artist, self.ll)
        match len(self.alist):
            case 1:
                self.a_offset = stdfs+2
                self.a_fs = stdfs
            case 2:
                self.a_offset = stdfs
                self.a_fs = stdfs-2
            case 3:
                self.a_offset = stdfs-2
                self.a_fs = stdfs-4
            case 4:
                self.a_offset = stdfs-4
                self.a_fs = stdfs-5
            case _:
                self.a_offset = stdfs-5
                self.a_fs = stdfs-6

def getPlaylistID(share_link):
    return share_link.split("playlist/")[1].split("?")[0]

# Step 1: Get songs from given playlist (paginated in batches of 100)
def get_tracks(target_count, link, f, ex):
    tracks = []
    playlist_id = getPlaylistID(link)
    offset = 0
    batch_size = 100  # Spotify API max limit per request

    while target_count is None or len(tracks) < target_count:
        results = sp.playlist_items(
            playlist_id,
            limit=batch_size,
            offset=offset,
            fields=f
        )
        items = results.get('items', [])
        if not items:
            break  # Reached the end of the playlist

        for item in items:
            if target_count is not None and len(tracks) >= target_count:
                break
            track = item.get('track')
            # Skip local files, missing tracks, and excluded titles
            if track and not track.get('is_local', False) and track['name'] not in ex:
                tracks.append(track)

        if len(items) < batch_size:
            break  # Fewer than 100 returned means no more pages left

        offset += batch_size

    return tracks

def correct(t, cor):
    for track in t:
        if track["name"] in cor:
            track['album']['release_date'] = cor[track['name']]
    return t

tracks = get_tracks(card_nb, playlists[playlist_name], fields, exclude.get(playlist_name, []))
if playlist_name in corrections:
    tracks = correct(tracks, corrections[playlist_name])

# Create a ReportLab canvas for PDF
pdf = canvas.Canvas(file_name, pagesize=A4)

# Helper to generate QR code image bytes from URL
def generate_qr_image(url):
    qr = qrcode.QRCode(box_size=10, border=1)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white').convert('RGB')
    return img


def find_space(s, lim): #search for a fitting line break
    i = lim-1
    while i!= 0:
        if s[i] == ' ':
            return i
        i -= 1
    return lim
        
def cutter(s, lim): #insert line breaks if a string is too long
    if len(s)<lim:
        return [s]
    else:
        idx = find_space(s, lim)
        return [s[:idx]] + cutter(s[idx+1:],lim)

# def lines(pdf): #draw lines in between the cards
#     for l in range(1,cols):
#         pdf.line(card_width*l,0,card_width*l,page_height)
#     for l in range(1,rows):
#         pdf.line(0,card_height*l,page_width,card_height*l)

def lines(pdf): 
    # Optional: Draw a rectangle around the whole grid (cutting boundary)
    pdf.rect(print_margin, print_margin, usable_width, usable_height)

    # Vertical inner lines
    for l in range(1,cols):
        x = print_margin + (card_width * l)
        pdf.line(x, print_margin, x, page_height - print_margin)
        
    # Horizontal inner lines
    for l in range(1,rows):
        y = print_margin + (card_height * l)
        pdf.line(print_margin, y, page_width - print_margin, y)

def get_pic_number(year, idx):

    if random_colors:
        return idx%15
    else:
        n = int((year-1950)/5)
        if n>14:
            return 14
        elif n<0:
            return 0
        else:
            return n

if simple_mode:
    font = simple_font
    bgo = qr_bg_obj(0.15*qr_size, 0.3*qr_size, qr_size, pdf)
    # text_bg = False
    # lines_yes_no = True

if(font[:7] == 'Courier'): std_line_limit = int(std_line_limit*0.75) 

num_sets = (len(tracks) + cpp - 1) // cpp
for set_n in range(num_sets):

    pdf.setLineWidth(0.1)
    if lines_yes_no: lines(pdf)
    
    # --- QR SIDE ---
    for idx, track in enumerate(tracks[set_n*cpp:], start=set_n*cpp): 
        col = cols-((idx%cpp) % cols)-1
        row = idx%cpp // cols
        
        # ADDED offset: print_margin
        x = print_margin + (col * card_width) + margin_x
        y = (page_height - print_margin) - ((row + 1) * card_height) + margin_y
        
        track_uri = track['uri']
        track_id = track_uri.split(':')[-1]
        track_url = f"https://open.spotify.com/track/{track_id}"
        
        qr_img = generate_qr_image(track_url)
        
        img_buffer = io.BytesIO()
        qr_img.save(img_buffer, format='PNG')
        img_buffer.seek(0)

        if simple_mode: bgo.draw(x+qr_size/2,y+qr_size/2, 'corners')
        elif qr_bg: pdf.drawImage('bg_aspect.png', x-margin_x, y-margin_y, card_width, card_height)
        
        pdf.drawInlineImage(Image.open(img_buffer), x, y, qr_size, qr_size)

        if((idx+1)%cpp == 0):
            pdf.showPage()
            break

    if (set_n == len(tracks)//cpp) and (len(tracks)%cpp!=0):
        pdf.showPage()

    pdf.setLineWidth(0.1)
    if lines_yes_no: lines(pdf)
    pdf.setFont(font,std_fs)
    
    # --- TEXT SIDE ---
    for idx, track in enumerate(tracks[set_n*cpp:], start=set_n*cpp): 
        ctr = tr(track['name'],
                   ", ".join(artist['name'] for artist in track['artists']),
                   track['album']['release_date'][:4],
                   std_line_limit,
                   std_fs)

        col = (idx%cpp) % cols
        row = idx%cpp // cols
        
        # ADDED offset: print_margin
        x = print_margin + ((col+0.5) * card_width)
        y = (page_height - print_margin) - ((row + 0.5) * card_height)
        
        if text_bg:
            path = f"gradient_images\\gradient_{get_pic_number(int(ctr.year),idx)}.png"
            try:
                pdf.drawImage(path, x-0.5*card_width, y - 0.5 * card_height, card_width, card_height)
            except: pass

        pdf.setFont(font, ctr.t_fs)
        for a, text in enumerate(ctr.tlist):
            pdf.drawCentredString(x,y+0.31*card_height-ctr.t_offset*(-0.5*(len(ctr.tlist)-1)+a),text)

        pdf.setFontSize(ctr.a_fs)
        for a, text in enumerate(ctr.alist):
            pdf.drawCentredString(x,y-0.34*card_height+ctr.a_offset*(0.5*(len(ctr.alist)-1)-a),text)
        
        pdf.setFont(font, 34)
        if(font[:7] == 'Courier'):pdf.setFont('Courier', 38)
        pdf.drawCentredString(x, y-0.08*card_height, ctr.year)

        if((idx+1)%cpp == 0):
            pdf.showPage()
            break

pdf.save()
# ...

print(f'got {len(tracks)} songs')
print(f"PDF {file_name} generated!")