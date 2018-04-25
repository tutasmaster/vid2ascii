import math
import sys
import subprocess
import time
from PIL import Image
from PIL import ImageEnhance
from PIL import ImageOps

print ("Number of arguments:" + str(len(sys.argv)) + " arguments.")
print ("Argument List:" + str(sys.argv))

videoname = "video.mp4"
fps = 30
start = 00
time = 10
outputname = "output"
fsize = 10
scale = 5

if(len(sys.argv) < 8):
	print("Your input should be: \" py vidToASCII.py videoname.mp4 <fps> <seconds> <outputName> <font-size in pixels> <scale> \"")
	print("Instructions on how to use this can be found in the README.md")
	sys.exit()

for i in range(1,len(sys.argv)):
	if i == 1:
		videoname = str(sys.argv[1])
	elif i == 2:
		fps = int(sys.argv[2])
	elif i == 3:
		time = int(sys.argv[4])
	elif i == 4:
		outputname = str(sys.argv[5])
	elif i == 5:
		fsize = int(sys.argv[6])
	elif i == 6:
		scale = int(sys.argv[7])
		
#args = ["ffmpeg.exe","-ss",str(start),"-t",str(time),"-i", videoname ,"-r",str(fps),outputname + "%1d.jpg"]
#subprocess.Popen(args)

a = open(outputname + ".html","w")

symbols = ["$","@","B","%","8","W","M","#","*","o","a","h","k","b","d","p","q","w","m","Z","O","0","Q","L","C","J","U","Y","X","z","c","v","u","n","x","r","j","f","t","/","|","(",")","1","{","}","[","]","?","-","+","~","i","!","1","I",";",":",",","^","`","'","."," "]
symbolSize = 1/len(symbols)

print("will it work?")
print("<pre style=\"font-size: " + str(fsize) + "px; display: inline-block; font-family: monospace;letter-spacing: 0.0em;line-height: 0.7em;\">", file=a)

for d in range(1,time*fps):
	print("<div id=\"" + str(d) + "\" style=\"display: none;\">", file=a);
	im = Image.open(str(outputname) + str(d) + ".jpg").convert('RGB')
	im = ImageOps.autocontrast(im)
	im = ImageOps.equalize(im)
	enhancer = ImageEnhance.Contrast(im)
	#im = enhancer.enhance(3.0)
	px = im.load()
	width,height = im.size
	
	for y in range(0, height//scale):
		for x in range(0, width//scale):
			pxRGB = im.getpixel((int(x*scale),int(y*scale)))
			R,G,B = pxRGB
			brt = sum([R,G,B])/3/255
			if brt > 0.1:
				pos = round(brt/symbolSize)
			elif brt <= 0.1:
				pos = 1
			else:
				pos = len(symbols)
			print(symbols[pos - 1],end="",file=a)
		print("", file=a)
	print("</div>",end="", file=a)
	print("FRAME: " + str(d))
print("</pre>", file=a)
print("""
<audio id="audio">
  <source src="output.mp3">
</audio>

<script>

var fps = """ + str(fps) + """;
var videoEnd = """ + str((fps*time)-1) + """;

Number.prototype.pad = function(size) {
  var s = String(this);
  while (s.length < (size || 2)) {s = "0" + s;}
  return s;
}

var playing = false; 
var i = 1;
function showVid(){

	i++;
	if(i > videoEnd){
		clearInterval(videoInterval);
		audio.pause();
		i = 1;
	}
	document.getElementById(i.toString()).style.display = "block";
}

var videoInterval;

var audio = document.getElementById("audio"); 

function bPressed(){
	playing = !playing;
	if(playing){
		clearInterval(videoInterval);
		videoInterval = setInterval(function(){
		if(i < 1){
			i = 1
		}
		if(i > videoEnd){
			i = videoEnd - 10;
		}
		document.getElementById(i.toString()).style.display = "none"; 
		showVid(); 
		document.getElementById("Playing").innerHTML = "Time: " + Math.floor((((i/fps)/60)/60)).pad(2) + ":" + Math.floor((((i/fps)/60)%60)).pad(2) + ":" + Math.floor(((i / fps)%60)).pad(2) + "/" + Math.floor((((videoEnd/fps)/60)/60)).pad(2) + ":" + Math.floor((((videoEnd/fps)/60)%60)).pad(2) + ":" + Math.floor(((videoEnd / fps)%60)).pad(2)  + " | FPS: " + fps
		document.getElementById("seconds").value = Math.floor(i/fps);}, 1000/10);
		audio.currentTime = (1/fps) * i;
		audio.play();
	}else{
		clearInterval(videoInterval);
		audio.pause();
	}
}

function forward(){
	document.getElementById(i.toString()).style.display = "none";
	i += 10 * fps;
	if(i > videoEnd){
		i = videoEnd - 10;
	}
	bPressed();
	bPressed();
}

function backward(){
	document.getElementById(i.toString()).style.display = "none";
	i -= 10 * fps;
	if(i < 1) {
		1
	}
	bPressed();
	bPressed();
}

function restart(){
	document.getElementById(i.toString()).style.display = "none";
	i = 1;
	bPressed();
	bPressed();
}

function skipTo(){
	document.getElementById(i.toString()).style.display = "none";
	i = (document.getElementById("seconds").value) * fps;
	bPressed();
	bPressed();
}

</script>
<p>
	<button onclick="backward()" type="button" id="backwards">-10 seg</button>
	<button onclick="bPressed()" type="button" id="play">Play/Pause</button>
	<button onclick="forward()" type="button" id="forwards">+10 seg</button>
</p>
<p>
	<button onclick="restart()" type="button" id="reset">Restart</button>
	<button onclick="skipTo()" type="button" id="skip">Restart</button>
	<input id="seconds" type="number" min="1" max=\"""" + str(time - 1) + """\">Seconds: </input>
</p>
<p id="Playing">
	Time: 00:00:00/00:00:00 | FPS: 00fps 
</p>

""",file=a);


