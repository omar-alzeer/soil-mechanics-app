from tkinter import Tk,Frame,Entry,Label,messagebox,Button,StringVar,LEFT,YES,NSEW,TOP,CENTER
from tkinter.filedialog import asksaveasfile , askopenfile
import matplotlib.pyplot as plt
import numpy as np
import struct
import sys
import Pmw

	
class App(Tk):
	def __init__(self):
		Tk.__init__(self)
		
		self.resizable(width=False,height=False)

		self.default_manakhel_num = 12
		self.get_from_manakhel = StringVar()
		self.manakhel_num = ""

		self.app_frame = Frame(self)
		self.commands_frame = Frame(self.app_frame)

		self.app_frame.pack(expand=YES,anchor=CENTER,padx=(10,10),pady=(2,10))

		self.group_table_frame = Pmw.Group(self.app_frame,tag_text="الجدول")
		self.group_buttons_frame = Pmw.Group(self.commands_frame,tag_text="الأوامر")
		self.group_num_frame = Pmw.Group(self.commands_frame,tag_text = "عدد المناخل")
		
		self.group_table_frame.grid(sticky=NSEW,padx=(0,10))
		self.group_buttons_frame.pack(side=TOP,fill="both",expand=YES)
		self.group_num_frame.pack(side=TOP,fill="both",expand=YES)

		self.table_frame = Frame(self.group_table_frame.interior())
		self.table_frame.grid(padx=(10,10),pady=(0,10))
		
		self.commands_frame.grid(column=1,row=0,sticky=NSEW)

		self.buttons_frame = Frame(self.group_buttons_frame.interior())
		self.buttons_frame.pack(expand=YES,anchor=CENTER)

		self.num_frame = Frame(self.group_num_frame.interior())
		self.num_frame.pack(expand=YES,anchor=CENTER)

		self.calc = Button(self.buttons_frame,text="حساب و رسم",command=self.run,takefocus=0)
		self.save = Button(self.buttons_frame,text="حفظ كملف",command=self.save_file,takefocus=0)
		self.open = Button(self.buttons_frame,text="فتح ملف",command=self.open_file,takefocus=0)

		self.calc.pack(pady=10)
		self.save.pack(padx=10,side=LEFT)
		self.open.pack(padx=10,pady=10)

		self.num_entry = Entry(self.num_frame,textvariable=self.get_from_manakhel)
		self.num_button = Button(self.num_frame,text="أدخل العدد",command=self.enter_num)

		self.num_entry.pack()
		self.num_button.pack(pady=(10,0))

		self.put_fatha = [StringVar() for i in range(self.default_manakhel_num)]
		self.put_wazen = [StringVar() for i in range(self.default_manakhel_num)]
		self.put_marra = [StringVar() for i in range(self.default_manakhel_num)]
		self.put_trakom = [StringVar() for i in range(self.default_manakhel_num)]
		self.put_mahjouz = [StringVar() for i in range(self.default_manakhel_num)]

		self.values_of_fathat_al_minlkhul = []
		self.values_of_wazen_jaf_mahjoz = []
		self.values_of_percent_of_almahjozah = []
		self.trakom_val = []
		self.marra_val = []
		self.save_val = []

		self.col1 = [Label(self.table_frame,text=" ")]
		self.col2 = [Label(self.table_frame,text="(mm) فتحة المنخل")]
		self.col3 = [Label(self.table_frame,text="(g) الوزن الجاف المحجوز")]
		self.col4 = [Label(self.table_frame,text="النسبة المئوية المحجوزة")]
		self.col5 = [Label(self.table_frame,text="النسبة المئوية التراكمية")]
		self.col6 = [Label(self.table_frame,text="النسبة المئوية المارة")]

		self.columns = [self.col1,self.col2,self.col3,self.col4,self.col5,self.col6]

		for row in range(self.default_manakhel_num):
			self.col1.append(Label(self.table_frame,text=f"{row+1}",state="disable"))
			self.col2.append(Entry(self.table_frame,textvariable = self.put_fatha[row],state="disable"))
			self.col3.append(Entry(self.table_frame,textvariable = self.put_wazen[row],state="disable"))
			self.col4.append(Entry(self.table_frame,textvariable = self.put_mahjouz[row],state="disable",takefocus=0))
			self.col5.append(Entry(self.table_frame,textvariable = self.put_trakom[row],state="disable",takefocus=0))
			self.col6.append(Entry(self.table_frame,textvariable = self.put_marra[row],state="disable",takefocus=0))

		for c , column in enumerate(self.columns):
			for r , entry in enumerate(column):
				if r==0 and c==0:
					continue
				entry.grid(row=r , column=c,sticky=NSEW)

	def clear_values(self):
		self.values_of_fathat_al_minlkhul.clear()
		self.values_of_percent_of_almahjozah.clear()
		self.values_of_wazen_jaf_mahjoz.clear()
		self.trakom_val.clear()
		self.marra_val.clear()

	def enter_num(self):
		self.manakhel_num = int(self.get_from_manakhel.get())
		self.clear_entry_boxes()

		for i in range(0,self.manakhel_num + 1):
			for j in self.columns:
				j[i].configure(state="normal")

		for i in range(self.manakhel_num + 1 , self.default_manakhel_num + 1):
			for j in self.columns:
				j[i].configure(state="disable")

	def float_to_hex(self,f):
	    return bytes.fromhex(hex(struct.unpack('<I', struct.pack('<f', f))[0])[2:])

	def hex_to_float(self,h):
		return round(struct.unpack('!f', bytes.fromhex(h))[0],5)

	def isfloat(self,element):
		try:
			float(element)
			return True
		except ValueError:
			return False

	def fathat_al_minkhul(self):
		for i in range(1,self.manakhel_num+1):
			self.values_of_fathat_al_minlkhul.append(float(self.col2[i].get()))

	def wazen_jaf_mahjoz(self):
		for i in range(1,self.manakhel_num+1):
			self.values_of_wazen_jaf_mahjoz.append(float(self.col3[i].get()))

	def percent_of_almahjozah(self):
		for i in self.values_of_wazen_jaf_mahjoz:
			self.values_of_percent_of_almahjozah.append(round((i/2000)*100,1))

	def trakom(self):
		s = 0
		for i in self.values_of_percent_of_almahjozah:
			s += i
			self.trakom_val.append(round(s,1))

	def marra(self):
		for i in self.trakom_val:
			self.marra_val.append(round(100-i,1))

	def putting(self):
		for i in range(self.manakhel_num):
			self.put_marra[i].set(f"{self.marra_val[i]}")
			self.put_trakom[i].set(f"{self.trakom_val[i]}")
			self.put_mahjouz[i].set(f"{self.values_of_percent_of_almahjozah[i]}")

	def plotting(self):
		x = np.array(self.values_of_fathat_al_minlkhul[::-1])
		y = np.array(self.marra_val[::-1])
		plt.plot(x,y)
		plt.xscale("log")
		plt.grid(True,which="both",ls="-")
		plt.show(block=False)

	def put_fatha_wazen(self):
		for i in range(self.manakhel_num):
			self.put_fatha[i].set(f"{self.values_of_fathat_al_minlkhul[i]}")
			self.put_wazen[i].set(f"{self.values_of_wazen_jaf_mahjoz[i]}")

	def clear_entry_boxes(self):
		for i in range(self.manakhel_num):
			self.put_marra[i].set("")
			self.put_trakom[i].set("")
			self.put_mahjouz[i].set("")

	def run(self):
		try:
			self.fathat_al_minkhul()
			self.wazen_jaf_mahjoz()
			self.percent_of_almahjozah()
			self.trakom()
			self.marra()
			self.putting()
			self.plotting()
			self.clear_values()
		except:
			messagebox.showerror('خطأ حسابي', 'هناك خطأ في أحد القيم أو أن هناك خانات فارغة')

	def get_from_file(self):
		s = -1
		with open(sys.argv[-1],"rb") as f:
			for j , i in enumerate(range(0,len(f.read()),4)):
				f.seek(0)
				if i < self.manakhel_num*4:
					self.put_fatha[j].set(str(self.hex_to_float(bytes.hex(f.read()[i:i+4]))))
				else:
					s = s + 1
					self.put_wazen[s].set(str(self.hex_to_float(bytes.hex(f.read()[i:i+4]))))

		f.close()

	def save_file(self):
		self.save_val.clear()

		file = asksaveasfile(initialfile = 'Untitled.soil',defaultextension=".soil",
							 filetypes=[("Soil Files","*.soil"),("All Files","*.*")])
		
		for i in range(1,len(self.col2)):
			if self.isfloat(self.col2[i].get()):
				self.save_val.append(self.col2[i].get())
			else:
				self.save_val.append(None)
				
		for i in range(1,len(self.col3)):
			if self.isfloat(self.col3[i].get()):
				self.save_val.append(self.col3[i].get())
			else:
				self.save_val.append(None)

		if file is not None:
			with open(file.name,"wb") as f:
				for i in self.save_val:
					if i == None:
						f.write(b"\x00\x00\x00\x00")
					else:
						f.write(self.float_to_hex(float(i)))

	def open_file(self):
		s = -1

		file = askopenfile(mode ='rb', filetypes =[('Soil Files', '*.soil')])
		self.clear_values()

		if file is not None:
			with open(file.name,"rb") as f:
				for j , i in enumerate(range(0,len(f.read()),4)):
					f.seek(0)
					if i < self.manakhel_num*4:
						self.put_fatha[j].set(str(self.hex_to_float(bytes.hex(f.read()[i:i+4]))))
					else:
						s = s + 1
						self.put_wazen[s].set(str(self.hex_to_float(bytes.hex(f.read()[i:i+4]))))

			self.clear_entry_boxes()
			f.close()


if __name__ == "__main__":
	App = App()
	if len(sys.argv) > 1:
		App.get_from_file()
	App.mainloop()