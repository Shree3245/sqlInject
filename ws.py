from base64 import b64encode

pic = open('sc.png', 'br').read()
pic = b64encode(pic)

file = open("pic.txt","w+")
file.write(str(pic)) 

movie = open('sr.mp4','br').read()
movie = b64encode(movie)
file = open("movie.txt","w+")
file.write(str(movie)) 

music = open('m.mid','br').open()
music = b64encode(music)
file = open("music.txt","w+")
file.write(str(music))

 