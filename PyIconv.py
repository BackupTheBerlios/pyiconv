#!/usr/bin/env python
# -*- coding: iso-8859-2 -*-
c = \
"""
  PyIconv.py - Prosty 'front-end' do programu iconv
  Copyright (C) 2003 Rafał 'jjhop' Kotusiewicz
  "Rafał Kotusiewicz" <jjhop@randal.qp.pl>
  http://randal.qp.pl/_projects/PyIconv/index.php
 
  This program is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public License
  as published by the Free Software Foundation; either version 2
  of the License, or any later version.
 
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.
 
  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

  $HOME/.pyiconv
  >  icon_path=/usr/bin/iconv
  >  from_enc=ISO_8859-2
  >  to_enc=WINDOWS-1250
"""

import Tkinter
import tkMessageBox
import tkFileDialog
import sys
import os
import os.path
import string

class PyIconv:
    version = "v.02.4"
    
    def __init__(self, config=None):

        self.config = config
        print c
        # for i in config.get_config_map().keys():
        #     print i , config[i]
        self.root = Tkinter.Tk()
        self.from_enc = Tkinter.StringVar(self.root)
        self.from_enc.set("WINDOWS-1250")

        self.input_file_name  = Tkinter.StringVar(self.root)
        self.output_file_name = Tkinter.StringVar(self.root)        

        self.to_enc = Tkinter.StringVar(self.root)
        self.to_enc.set("ISO_8859-2")
        
        self.menu = Tkinter.Menu(self.root)
        self.filem = Tkinter.Menu(self.menu)
        self.filem.config(tearoff=0)
        #self.filem.add_separator()
        self.filem.add_command(label="Exit", command=self.__exit)

        self.optionsm = Tkinter.Menu(self.menu)
        self.optionsm.config(tearoff=0)
        #self.optionsm.add_command(label="Options...", command=self.__options_dialog)
        self.optionsm.add_command(label="Options...", command=self.von)
        
        
        self.helpm = Tkinter.Menu(self.menu)
        self.helpm.config(tearoff=0)
        self.helpm.add_command(label="PyIconv Home Page", command=self.__open_home_page)
        self.helpm.add_command(label="About PyIconv", command=self.__about_pyiconv)
        self.helpm.add_separator()
        self.helpm.add_command(label="About Author", command=self.__about_author)
        
        self.menu.add_cascade(label="File", menu=self.filem)
        self.menu.add_cascade(label="Options", menu=self.optionsm)        
        self.menu.add_cascade(label="Help", menu=self.helpm)

        self.frame = Tkinter.Frame(self.root)
        self.frame.pack(expand=1, fill=Tkinter.BOTH)

        # WIERSZ PIERWSZY
        #Tkinter.Label(self.frame, text="sss: ").grid(column=0, row=1)
        self.option_from_enc = Tkinter.OptionMenu(self.frame, self.from_enc, "ISO_8859-1","ISO_8859-2","WINDOWS-1250")
        self.option_from_enc.configure(width = 14)
        self.option_from_enc.grid(column=0, row=1)
        
        self.input_file = Tkinter.Entry(self.frame)
        self.input_file.configure(state="normal", width=30)
        self.input_file.grid(column=1, row=1)
        
        Tkinter.Button(self.frame, text="Choose...", command=self.__get_input_file_name).grid(column=2, row=1)

        # WIERSZ DRUGI
        self.option_to_enc = Tkinter.OptionMenu(self.frame, self.to_enc,  "ISO_8859-1","ISO_8859-2","WINDOWS-1250")
        self.option_to_enc.configure(width = 14)
        self.option_to_enc.grid(column=0, row=2)

        self.output_file = Tkinter.Entry(self.frame)
        self.output_file.configure(state="normal", width=30)
        self.output_file.grid(column=1, row=2)
        Tkinter.Button(self.frame, text="Choose...", command=self.__get_output_file_name).grid(column=2, row=2)

        # WIERSZ TRZECI
        self.diff_check = Tkinter.Checkbutton(self.frame)
        self.diff_check.configure(text="Show diff when convert will be done....")
        self.diff_check.grid(column=0, sticky=Tkinter.W, columnspan=2, row=3)
        #self.diff_check.pack(side=Tkinter.LEFT, fill=Tkinter.BOTH, padx=2)


        # WIERSZ CZWARTY
        self.open_after = Tkinter.Checkbutton(self.frame)
        self.open_after.configure(text="Open converted file")
        self.open_after.grid(column=0, sticky=Tkinter.W, columnspan=2, row=4)

        # WIERSZ CZWARTY / PIĄTY
        self.proc_but = Tkinter.Button(self.frame, text="Convert!", command=self.convert).grid(column=2,rowspan=2,row=3,sticky="s")
        
        self.statusBar = Tkinter.Label(self.root, text="Application started...")
        self.statusBar.pack(side=Tkinter.LEFT, fill=Tkinter.BOTH, padx=2)

        self.root.bind("<ButtonRelease-3>", self.von)

        self.root.config(menu=self.menu)
        self.root.wm_minsize(width=450, height=180)
        self.root.wm_maxsize(width=450, height=180)
        title_ = "PyIconv " + self.version + " by jjhop@randal.qp.pl"
        self.root.wm_title(string=title_)
        #self.root.tk_strictMotif(1)
        #self.root.tk_bisque()
        tkMessageBox.showwarning("Uwaga!", "Uwaga!\n\nSciezka do pliku wykonywalnego iconv ustawiona na \"/usr/bin/iconv\"\naby ja zmienic nalezy edytowac plik programu w linii 141\n")                
        self.root.mainloop()

    def convert(self, evt=None):
        #print "Input:  " , self.input_file_name.get()
        #print "Output: " , self.output_file_name.get()
        #print "FROM:   " , self.from_enc.get()
        #print "TO:     " , self.to_enc.get()

        conv = Converter('/usr/bin/iconv');
        conv.set_from_enc(self.from_enc.get())
        conv.set_to_enc(self.to_enc.get())
        conv.set_input_file(self.input_file_name.get())
        conv.set_output_file(self.output_file_name.get())
        conv.prepare_command()
        conv.convert()
        
    def von(self, evt=None):
        tkMessageBox.showinfo('Not yet...','Not yet implemented')
        
    def __get_input_file_name(self):
        self.input_file_name.set( tkFileDialog.askopenfilename(filetypes=[("Text files","*.txt"), ("All files", "*.*")]) )
        self.input_file.configure(state="normal")
        self.input_file.insert(0, self.input_file_name.get())
        self.input_file.configure(state="readonly")
    def __get_output_file_name(self):
        self.output_file_name.set( tkFileDialog.asksaveasfilename(filetypes=[("Text","*.txt"), ("All files", "*.*")]) )
        self.output_file.configure(state="normal")
        self.output_file.insert(0, self.output_file_name.get())
        self.output_file.configure(state="readonly")

    def __options_dialog(self):
        # mamy self.config
        pass
    def __open_home_page(self):
        try:
            import webbrowser
            webbrowser.open_new("http://www.jjhop.net/apps/python/PyIconv/index.php")
        except:
            tkMessageBox.showinfo("Error...", "You need open site http://www.jjhop.net/apps/python/PyIconv/")
    def __about_pyiconv(self):
        tkMessageBox.showinfo("About program...", "\nPyIconv " + self.version + "\n\nPyIconv is simple front-end to iconv and I hope that is very useful.\nLast update: 23.02.2004\n")
    def __about_author(self):
        tkMessageBox.showinfo("About author...", "This program was created by Rafal 'jjhop' Kotusiewicz.\n\nWWW: http://www.jjhop.net\nEmail: jjhop@randal.qp.pl\n")
    def __exit(self):
        if tkMessageBox.askokcancel("Confirm exit", "Are You sure?") == 1:
            del self.config
            sys.exit(0)

class Converter:
    def __init__(self, iconv_path):
        self.iconv_path = iconv_path
        self.from_enc    = None
        self.to_enc      = None
        self.input_file  = None
        self.output_file = None
        self.command     = None
    def set_from_enc(self, from_enc):
        self.from_enc = from_enc
    def set_to_enc(self, to_enc):
        self.to_enc = to_enc
    def set_input_file(self, input_file):
        self.input_file = input_file
    def set_output_file(self, output_file):
        self.output_file = output_file
    def prepare_command(self):
        command = self.iconv_path + ' '
        command = command + ' -f ' + self.from_enc 
        command = command + ' -t ' + self.to_enc
        command = command + ' ' + self.input_file
        command = command + ' -o ' + self.output_file        
        self.command = command
    def convert(self, show_diff=None):
        print self.command
        ret = os.system(self.command)
        if ret == 0:
            # poinformuj o sukcesie
            tkMessageBox.showinfo("Powodzenie...", "Operacja konversji pliku zakonczona powodzeniem");
        else:
            # poinformuj o porażce
            tkMessageBox.showerror("Porazka...", "Operacja konversji pliku nie zakonczyla sie powodzeniem");

Converter("hello")    

class Configurator:
    """
        Configurator - klasa obsługująca pliki konfiguracyjne w formacie

        zmienna1=wartosc1
        zmienna2=wartosc2
        zmienna3=wartosc3

        Możemy z nich korzystac w nastepujący sposób:

        config = Configurator('/path/to/config_file')
        value = config.get_var('var_name')
          # lub
        value = config['var_name']
                       
    """
    def __init__(self, config_file):
        self.config_file = config_file
        self.config_map ={}
        self.change = 0
        try:
            fd = open(self.config_file)
            line = fd.readline()
            while line:
                as_list = string.split(line, '=', 2)
                self.config_map[as_list[0]] =  as_list[1][:-1]
                line = fd.readline()
            fd.close()
        except Exception, e:
            print ":" , e
    def __getitem__(self, key):
        if self.config_map.has_key(key):
            return self.config_map[key]
        else:
            raise LookupError, "Unknown config key"
    def __setitem__(self, key, value):
        # not yet implemented
        if self.config_map.has_key(key):
            if self.config_map[key] == value:
                return
            else:
                self.config_map[key] = value
                self.change = 1
        else:
            self.config_map[key] = value
            self.change = 1
    def __delitem__(self, key):
        if not self.config_map.has_key(key):
            return
        else:
            del self.config_map[key]
            self.change = 1
    def __del__(self):
        """ Destruktor """
        # not yet implemented
        if self.change:
            # zmianiamy konfigurację
            print 'zmieniamy...'
            try:
                vars = []
                for i in self.config_map.keys():
                    line = i + "=" + self.config_map[i] + "\n"
                    vars.append(line)
                fd = open(self.config_file,'w', 0)
                fd.writelines(vars)
                fd.close()
            except IOError, e:
                print e
    def get_var(self, key):
        return self.config_map[key]
    def set_var(self, key, value):
        self.__setitem__(self, key, value)    
    def get_config_map(self):
        return self.config_map
    def dump_config(self):
        self.__del__()
    

if __name__ == '__main__':
    #if string.atoi(str(sys.version_info[0]) + str(sys.version_info[1])) < 23:
    #   raise Exception("Niewłaściwa wersja interpretera!")
    try:
        # ustalamy nazwe pliku konfiguracyjnego $HOME/.pyiconv
        if 1: #plik_istnieje i mozna go czytac
            config = Configurator("/home/jjhop/congo")
            PyIconv(config)
        else:
            PyIconv()
    except Exception, e:
        print e
    else:
        del config        
