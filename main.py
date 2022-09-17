from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import asksaveasfile
import matplotlib.pyplot as plt
import struct

#examples
# [25.4,19.1,9.5,4.75,2.0,0.84,0.425,0.074,0.005]
# [223,142,283,270,200,165,125,140,130]
# [88.8,81.7,67.5,54.0,44.0,35.7,29.4,22.4,15.9]

def float_to_hex(f):
    return bytes.fromhex(hex(struct.unpack('<I', struct.pack('<f', f))[0])[2:])

def hex_to_float(h):
	return round(struct.unpack('!f', bytes.fromhex(h))[0],5)

def isfloat(element):
    try:
        float(element)
        return True
    except ValueError:
        return False

def fathat_al_minkhul():
	for i in range(1,len(box1)):
		values_of_fathat_al_minlkhul.append(float(box1[i].get()))

def wazen_jaf_mahjoz():
	for i in range(1,len(box2)):
		values_of_wazen_jaf_mahjoz.append(float(box2[i].get()))

def percent_of_almahjozah():
	for i in values_of_wazen_jaf_mahjoz:
		values_of_percent_of_almahjozah.append(round((i/2000)*100,1))

def trakom():
	s = 0
	for i in values_of_percent_of_almahjozah:
		s += i
		trakom_val.append(round(s,1))

def marra():
	for i in trakom_val:
		marra_val.append(round(100-i,1))

def putting():
	for i in range(9):
		put_marra[i].set(f"{marra_val[i]}")

	for i in range(9):
		put_trakom[i].set(f"{trakom_val[i]}")

	for i in range(9):
		put_mahjouz[i].set(f"{values_of_percent_of_almahjozah[i]}")

def save_file():
	save_val.clear()

	file = asksaveasfile(initialfile = 'Untitled.soil',defaultextension=".soil",filetypes=[("Soil Documents","*.soil"),("All Files","*.*")])
	
	for i in range(1,len(box1)):
		if isfloat(box1[i].get()):
			save_val.append(box1[i].get())
		else:
			save_val.append(None)
			
	for i in range(1,len(box2)):
		if isfloat(box2[i].get()):
			save_val.append(box2[i].get())
		else:
			save_val.append(None)
			
	with open(file.name,"wb") as f:
		for i in save_val:
			if i == None:
				f.write(b"\x00\x00\x00\x00")
			else:
				f.write(float_to_hex(float(i)))

# to get values from (.soil) file format
def get_from_file():
	with open(sys.argv[1],"rb") as f:
		for i in range(0,len(f.read()),4):
			f.seek(0)
			if i < 36:
				values_of_fathat_al_minlkhul.append(hex_to_float(bytes.hex(f.read()[i:i+4])))
			else:
				values_of_wazen_jaf_mahjoz.append(hex_to_float(bytes.hex(f.read()[i:i+4])))


def plotting():
	x = values_of_fathat_al_minlkhul[::-1]
	y = marra_val[::-1]
	plt.plot(x,y)
	plt.xscale("log")
	plt.grid(True,which="both",ls="-")
	plt.show(block=False)

# to put values of fathat and wazen jaf in textboxes
def put_fatha_wazen():
	for i in range(9):
		put_fatha[i].set(f"{values_of_fathat_al_minlkhul[i]}")

	for i in range(9):
		put_wazen[i].set(f"{values_of_wazen_jaf_mahjoz[i]}")


def commando():
	if len(sys.argv) > 1:
		values_of_fathat_al_minlkhul.clear();values_of_percent_of_almahjozah.clear();values_of_wazen_jaf_mahjoz.clear();trakom_val.clear();marra_val.clear()
		get_from_file()
		percent_of_almahjozah();trakom();marra();putting();plotting()

	else:
		values_of_fathat_al_minlkhul.clear();values_of_percent_of_almahjozah.clear();values_of_wazen_jaf_mahjoz.clear();trakom_val.clear();marra_val.clear()
		try:
			fathat_al_minkhul();wazen_jaf_mahjoz();percent_of_almahjozah();trakom();marra();putting();plotting();
		except:
			messagebox.showerror('خطأ حسابي', 'هناك خطأ في أحد القيم أو أن هناك خانات فارغة')


root = Tk()


table_frame = Frame(root)
btns_frame = Frame(root)

f1 = Frame(table_frame)
f2= Frame(table_frame)
f3= Frame(table_frame)
f4= Frame(table_frame)
f5= Frame(table_frame)

root.geometry("650x300")


box1 = [Label(f1,text="(mm) فتحة المنخل")]
box2 = [Label(f2,text="(g) الوزن الجاف المحجوز")]
box3 = [Label(f3,text="النسبة المئوية المحجوزة")]
box4 = [Label(f4,text="النسبة المئوية التراكمية")]
box5 = [Label(f5,text="النسبة المئوية المارة")]

columns = [box1,box2,box3,box4,box5]

put_fatha = [StringVar() for i in range(9)]
put_wazen = [StringVar() for i in range(9)]

put_marra = [StringVar() for i in range(9)]
put_trakom = [StringVar() for i in range(9)]
put_mahjouz = [StringVar() for i in range(9)]

values_of_fathat_al_minlkhul = []
values_of_wazen_jaf_mahjoz = []
values_of_percent_of_almahjozah = []
trakom_val = []
marra_val = []

save_val = []


for i in range(9):
	box1.append(Entry(f1,textvariable = put_fatha[i]))
	box2.append(Entry(f2,textvariable = put_wazen[i]))
	box3.append(Entry(f3,textvariable = put_mahjouz[i]))
	box4.append(Entry(f4,textvariable = put_trakom[i]))
	box5.append(Entry(f5,textvariable = put_marra[i]))	

for i in columns:
	for j in i:
		j.pack()

if len(sys.argv) > 1:
	get_from_file()
	put_fatha_wazen()


click_btn = Button(btns_frame,text="احسب",command=commando,takefocus=0)
save_btn = Button(btns_frame,text="حفظ",command=save_file,takefocus=0)

btns_frame.pack(pady=20)

click_btn.pack(side=LEFT,padx=25)
save_btn.pack(side=LEFT,padx=25)

table_frame.pack(side=LEFT,expand=YES)

f1.pack(side=LEFT)
f2.pack(side=LEFT)
f3.pack(side=LEFT)
f4.pack(side=LEFT)
f5.pack(side=LEFT)

root.bind('<Up>' , up)
root.bind('<Down>' , down)
root.bind('<Right>' , right)
root.bind('<Left>' , left)
root.bind('<Return>', enter)

root.mainloop()

