import spotipy
from spotipy.oauth2 import SpotifyOAuth
import qrcode
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
import os
import numpy as np

os.system("cls")

playlist_name = "test"

playlists = {
            "(g)old":       "https://open.spotify.com/playlist/2z5Nv5wPAGjUKDZzBeJq3L?si=248c71376bff4943",
            "Spikeball":    "https://open.spotify.com/playlist/2s2PdHeaSNINXdLgXWtjMv?si=62fd240512df487c",
            "HF":           "https://open.spotify.com/playlist/3jSD9sSEPEn5w1TYrqoIGk?si=904cfdf21c9f44f4&pt=48e2f02d071dd454d845b406f7429ac0",
            "SIK":          "https://open.spotify.com/playlist/6cgXtYKs80LipngAXP9Tc1?si=b9ccc5afe3614e97",
            "FB":           "https://open.spotify.com/playlist/4588eR8zlZc2I5ipK5zX34?si=a80e5158b07c4ebc",
            "HR":           "https://open.spotify.com/playlist/2uoCGdRkUWhxH1ZtfJopSO?si=1fe6bcca79984cb2",
            "HM":           "https://open.spotify.com/playlist/49XR4URAaZOQkFoKTuq9D6?si=1ec61eba78754f10",
            "HK":           "https://open.spotify.com/playlist/5defDRMAtRMVZOiCqBubDZ?si=ab3500c7cb1740d1",
            "test":         "https://open.spotify.com/playlist/60JZs4dAVFe5OgXcI8cWw5?si=cfabe21e170e439f"
            }

corrections = {'(g)old':
    {
    'Voyage voyage': '1986',
    'Funkytown - Single Version': '1980',
    'What A Feeling': '1983',
    'Hard to Say I\'m Sorry - 2007 Remaster': '1982',
    'The Power Of Love': '1985',
    'Careless Whisper': '1984',
    'September': '1978',
    'In The Army Now': '1986',
    'In a Broken Dream': '1972',
    'Layla': '1970',
    'Disco Inferno - Edit': '1976',
    'Maria Magdalena': '2013'

},
"Spikeball":
{
    "I Will Survive": '1978',
    "Ain't No Mountain High Enough - Stereo Version": '1967',
    "Don't Stop Believin'": '1981',
    "Should I Stay or Should I Go - Remastered": '1982',
    "September": '1978',
    "Wake Me up Before You Go-Go": '1984',
    "Beat It": '1983',
    "Don't Stop Me Now - Remastered 2011": '1979'
},
"HF":
{
    'Voyage voyage': '1986',
    'Funkytown - Single Version': '1980',
    'What A Feeling': '1983',
    'Hard to Say I\'m Sorry - 2007 Remaster': '1982',
    'The Power Of Love': '1985', 
    'Careless Whisper': '1984',
    'September': '1978',
    'In The Army Now': '1986',
    'In a Broken Dream': '1972',
    'Layla': '1970',
    'Disco Inferno - Edit': '1976',
    'Maria Magdalena': '1985',

    "I Will Survive": '1978',
    "Ain't No Mountain High Enough - Stereo Version": '1967',
    "Don't Stop Believin'": '1981',
    "Should I Stay or Should I Go - Remastered": '1982',
    "September": '1978',
    "Wake Me up Before You Go-Go": '1984',
    "Beat It": '1983',
    "Don't Stop Me Now - Remastered 2011": '1979',

    "Tequila (Original)": "1958",
    "Banana Boat (Day-O)": "1957",
    "Hit the Road Jack": "1960",
    "(What A) Wonderful World": "1967",
    "White Christmas": "1942",
    "La mer": "1946",
    "Take Five": "1959",
    "It's Been a Long, Long Time": "1945"
    
},
"HR" : {
    'Tutti Frutti': '1955',
    'Hound Dog': '1956',
    'See You Later, Alligator': '1956',
    'Johnny B. Goode': '1958',
    'The Good, The Bad And The Ugly - 2004 Remaster': '1966',
    'Green Green Grass Of Home': '1966',
    'Rock Around The Clock': '1954',
    'What A Wonderful World': '1967',
    'Video Killed The Radio Star': '1979',
    'Siebzehn Jahr, blondes Haar': '1965',
    'Just the Two of Us (feat. Bill Withers)': '1981',
    'I\'m So Excited': '1982',
    'Griechischer Wein': '1974',
    'Teenage Dirtbag': '2000',
    'In the Summertime': '1970',
    'Orinoco Flow': '1988',
    'California Dreamin\'': '1965',
    'No Woman, No Cry - Live At The Lyceum, London/1975': '1975',
    'Marieke': '1961',
    'I\'m Gonna Be (500 Miles)': '1988',
    'I Got You (I Feel Good)': '1965',
    '99 Luftballons': '1983',
    'Irgendwie, irgendwo, irgendwann': '1984',
    'In The Mood': '1939',
    'ブルーバード': '2008',
    'The Power Of Love': '1985',
    'Hey Jude': '1968',
    'Footloose': '1984',
    'Zombie': '1994',
    'Like a Prayer': '1989',
    'Stumblin\' In': '1978',
    'Make It Shine (Victorious Theme) (feat. Victoria Justice)': '2010',
    'Sex On The Beach': '1996',
    'Guajira Guantanamera': '1929',
    'Don\'t You (Forget About Me) - Remastered': '1985',
    'No Limit': '1993',
    'Riptide': '2013',
    'Disco Inferno - Edit': '1976',
    'Brazil': '2015',
    'ocean eyes': '2016',
    'Toxic': '2004',
    'September': '1978',
    'Bohemian Rhapsody': '1975',
    'The Cruel Angel\'s Thesis (Director\'s Edit Version)': '1995',
    'Disco Pogo': '2010',
    'Stayin Alive': '1977',
    'Amour plastique': '2018',
    'These Boots Are Made for Walkin\'': '1966',
    'Love is All Around': '1994',
    'The Fate of Ophelia': '2024',
    '愛♡スクリ～ム！': '2024',
    'CHASING SHADOWS': '2024'
},

"HM": {
    'Tutti Frutti': '1955',
    'Hound Dog': '1956',
    'Johnny B. Goode': '1958',
    '(What A) Wonderful World': '1960',
    'Take Five': '1959',
    'California Dreamin\' - Single Version': '1965',
    'Hey Joe': '1966',
    'What A Wonderful World': '1967',
    'Rock Around The Clock': '1954',
    'Son Of A Preacher Man': '1968',
    'Don\'t Go Breaking My Heart': '1976',
    'Ich hab\' ein zärtliches Gefühl': '1973',
    'Bohemian Rhapsody - Remastered 2011': '1975',
    'Eins Für Carmen Un En Insel': '1981',
    'Der Kommissar': '1981',
    'Nur geträumt': '1982',
    'Shout To The Top - USA Remix': '1984',
    'Easy Lover': '1984',
    'La vie en rose': '1946',
    'Holding Out for a Hero - From "Footloose" Soundtrack': '1984',
    'Love Is Strange': '1956',
    'Goldfinger': '1964',
    'Minnie the Moocher (Theme Song)': '1931',
    'Ein Freund, ein guter Freund - 1990 Digital Remaster': '1930',
    'La mer': '1946',
    '(We\'re Gonna) Rock Around The Clock - Single Version': '1954',
    'Is You Is Or Is You Ain\'t (My Baby)': '1944',
    'House of the Rising Sun': '1964',
    'Schöne Isabella aus Kastilien': '1929',
    'In the Mood': '1939',
    'Hells Bells': '1980',
    'Jailhouse Rock': '1957',
    'Escape (The Pina Colada Song)': '1979',
    'Enjoy the Silence': '1990',
    'Major Tom (...völlig losgelöst)': '1982',
    'Call Me': '1980',
    'Teenage Dirtbag': '2000',
    'Puttin\' on the Ritz': '1930', # Fred Astaire version
    'I Wanna Be Like You': '1968', # Kenny Ball version
    'Ich bin von Kopf bis Fuß auf Liebe eingestellt': '1930',
    'Lili Marleen': '1939',
    'Mrs. Robinson - From "The Graduate" Soundtrack': '1968',
    'Drei Haselnüsse für Aschenbrödel: Abfahrt des Königspaars und seiner Begleiter': '1973',
    'I Got You (I Feel Good)': '1965',
    '99 Luftballons': '1983',
    'Puttin\' On the Ritz': '1930', # Harry Richman version
    'Der Weg': '2002',
    'Männer': '1984',
    'Zombie': '1994',
    'Strangers In The Night - 2008 Remastered': '1966',
    'It\'s Been a Long, Long Time': '1945',
    'Total Eclipse of the Heart': '1983',
    'What I\'d Say (Remastered)': '1959',
    'Mr. Sandman': '1954',
    'Guajira Guantanamera': '1929',
    'Lean on Me': '1984', # Al Jarreau version
    'Disco Inferno - Edit': '1976',
    'Cabaret': '1972',
    'Theme From "New York, New York"': '1977',
    'Over the Rainbow': '1993',
    'James Bond Theme': '1962',
    'See You Later Alligator': '1955',
    'Disco Pogo': '2010',
    'Hit the Road Jack': '1961',
    'Hello, Dolly!': '1964',
    'Könntest du zaubern': '1977',
    'Careless Whisper - Remastered': '1984',
    '25grad (feat. Kasi)': '2024',
    "Drei haselnüsse für aschenbrödel - Motiv i. - Einleitung": "1973"
},

"HK": {
    # Medieval & Renaissance
    'Missa orbis factor - Kyrie': '950',  # 10th Century Gregorian Chant
    'Ut Queant Laxis': '770',            # Hymn to St. John (Guido of Arezzo)
    'Pange lingua (Gregorian chant)': '1263', # Text by Aquinas
    'Innsbruck, ich muß dich lassen': '1500',
    'If Ye Love Me': '1565',

    # Baroque (approx. 1600–1750)
    'Toccata': '1635',                    # From Fiori musicali (Frescobaldi)
    'Tarantella napoletana': '1654',      # Athanasius Kircher transcription
    'Aller Augen Warten Auf Dich, Herre': '1657',
    'Schmelzer: Polnische Sackpfeifen for 2 Violins and Continuo': '1664',
    'Canon in D': '1680',
    'Pastorale Für Orgel': '1716',        # Domenico Zipoli
    'Concerto No. 3 in G Major, RV 310: I. Allegro': '1711',
    'Fantasia & Fugue in G Minor, BWV 542: I. Fantasia': '1720',
    'Recorder Sonata in C major, Op. 1, No. 7, HWV 365: 1. Larghetto - Adagio': '1726',
    'Violin Concerto No.1 in A minor, BWV 1041: I. [Allegro moderato]': '1730',
    'Recorder Concerto in F Major, FWV L:F deest: I. Allegro': '1730',
    'Ouverture in D Minor: Gigue': '1740', # Johann Friedrich Fasch
    'Der Messias, HWV 56, Pt. 1: No. 4, Chor. Denn die Herrlichkeit Gottes - Auf deutsch gesungen': '1741',
    'Goldberg Variations: Variatio 7, BWV 988': '1741',
    'Cello Sonata in C Major, Op. 5 No. 3, H. 105: I. Andante': '1746',
    'Music for the Royal Fireworks, HWV 351: I. Ouverture': '1749',

    # Classical (approx. 1750–1820)
    'Cello Concerto No. 2 in A Major: I. Allegro con spirito': '1779',
    'Piano Concerto No. 20 in D Minor, K. 466: I. Allegro (Cadenza: Beethoven, WoO 58/1)': '1785',
    'Eine kleine Nachtmusik K. 525: Allegro': '1787',
    'Die Schöpfung, Hob. XXI:2, Pt. 1: Introduction. Die Vorstellung des Chaos. Largo': '1798',
    'Piano Sonata No. 14 in C-Sharp Minor, Op. 27 No. 2 "Moonlight Sonata": I. Adagio sostenuto - Recorded 1983': '1801',
    'Piano Concerto No. 5 in E-Flat Major, Op. 73 "Emperor": II. Adagio un poco mosso': '1809',
    'Erlkönig, D. 328': '1815',

    # Romantic (approx. 1820–1900)
    'Winterreise, D. 911: No. 1, Gute Nacht': '1827',
    'Nocturne Op. 9 No. 2': '1830',
    'Melodic Exercises / Melodische Übungsstücke, Op. 149, No. 1 - 10: No. 4, Allegro in C Major / C-Dur - Primo - Metronome: 1/2 = 69': '1833',
    'String Quartet in E-Flat Major, H. 277: II. Allegretto': '1834',
    'Kinderszenen, Op. 15: I. Von fremden Ländern und Menschen': '1838',
    'Elijah, Op. 70, MWV A25 - German Text / Part 1: No. 8: "Was hast du an mir getan"': '1846',
    'Piano Trio in G Minor, Op. 17: I. Allegro moderato': '1846',
    'Vier Lieder ohne Worte, Op. 8: I. Allegro moderato': '1846',
    'Abendlied, Op. 69 No. 3': '1855',
    'Piano Trio in B Minor, Op. 16: I. Allegro di molto e con brio': '1860',
    'Grieg: Suite No. 1 from Peer Gynt, Op. 46: I. Morning Mood': '1875',
    'Swan Lake (Suite), Op. 20a, TH.219: I. Scene - Swan Theme': '1876',
    'Der Karneval der Tiere: Das Aquarium': '1886',
    'Brahms: Double Concerto for Violin and Cello in A Minor, Op. 102: I. Allegro': '1887',
    'Mörike-Lieder: No. 17, Der Gärtner': '1888',
    'Clair De Lune': '1890',
    'String Quartet No. 12 In F Major, Op. 96 - "American" B.179: 4. Finale (Vivace ma non troppo)': '1893',

    # 20th Century & Contemporary
    'Pomp and Circumstance March No. 1 in D Major, Op. 39/1': '1901',
    'Piano Concerto No. 2 in C Minor, Op. 18: II. Adagio sostenuto - Live': '1901',
    'Rhapsody in Blue': '1924',
    'Prokofiev: Romeo and Juliet, Op. 64, Act 1: Dance of the Knights': '1935',
    'Lili Marleen': '1938',
    'Wie wunderbar ist doch Musik': '1957',
    'West Side Story: X. Tonight (Ensemble)': '1957',
    'Noposepe': '1962',
    'Sancte Michael Archangele': '1970',  # Approx. (Wolfango Dalla Vecchia)
    'Ich weiß nichts über sie': '1973',
    'Mediterranean Sundance / Rio Ancho - Live at Warfield Theatre, San Francisco, CA - December 5, 1980': '1976',
    'Aries (aus SIRIUS) · für C-Trompete & Elektronische Musik (1977): (Anfang)': '1977',
    'Veni sancte spiritus': '1979',       # Taizé (Jacques Berthier)
    'Das macht doch nichts (das merkt doch keiner) - 2016 Version': '1979',
    'Dance Me To The End Of Love': '1984', # Leonard Cohen composition
    'Grüezi Wohl, Frau Stirnimaa - Original Version': '1969'
},
"test": {
    "parents": "1940"
}

}

card_nb = 500                            #number of songs to turn into cards (max 100)
playlist_start = 0                     #select at which position to start in the playlist

# Spotify credentials and setup
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id='3cb78c8e36c144fbb79c974654f906bb',
    client_secret='673728c7df64475a9e06805d62cb15a0',
    redirect_uri='http://127.0.0.1:8888/callback',
    scope='user-read-playback-state user-modify-playback-state'
))

def getPlaylistID(share_link):
    return share_link[34:56]

fields = "items(track(name,artists(name),album(release_date),external_urls(spotify),is_local))"

# Step 1: Get songs from given playlist
def get_tracks(count,offset,link):
    tracks = []
    # Grab tracks from a given playlist
    results = sp.playlist_items(getPlaylistID(link), limit=count, offset=offset, fields=fields)
    items = results['items']
    for item in items:
        if len(tracks) >= count:
            break
        track = item['track']
        # Some tracks may be local or missing data; skip those
        if track and track['is_local'] is False:
            tracks.append(track)
    return tracks

# tracks = get_tracks(card_nb, playlist_start, Playlist_share_link)

tracks = []

for start_idx in range(0,card_nb,100):
    tracks += get_tracks(100, start_idx, playlists[playlist_name])

if playlist_name in corrections:
    for track in tracks:
        if track["name"] in corrections.get(playlist_name) and track:
            track['album']['release_date'] = corrections.get(playlist_name,{}).get(track["name"])

sorted_tracks = sorted(tracks, key = lambda t: t['album']['release_date'])

current_decade = 0
for x in sorted_tracks:
    if current_decade != int(x['album']['release_date'][2:3]):
        print(f'\n{'-'*85}\n')
        current_decade = int(x['album']['release_date'][2:3])
    print(f'{x['album']['release_date'][:4]} - {x['name']} by {x['artists'][0]['name']}')
print(f'got {len(tracks)} songs')
