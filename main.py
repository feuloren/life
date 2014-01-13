#!/usr/bin/python
# -*- coding:utf-8 -*-

from gi.repository import Gtk

import computer

class Adjust(Gtk.Adjustment):
    def __init__(self, current, min, top, text):
        super(Gtk.Adjustment, self).__init__()

        self.configure(current, min, top, 1, 1, 1)
        self.text_model = text
        self.connect('value-changed', self.value_changed_cb)

        self.label = None

    def value_changed_cb(self, *args):
        if self.label:
            self.label.set_label(self.compute_text())

    def compute_text(self):
        return self.text_model % int(self.get_value())

    def create_widget(self):
        hbox = Gtk.VBox()

        self.label = Gtk.Label(label=self.compute_text())
        hbox.pack_start(self.label, False, False, 0)
        scale_width = Gtk.HScale(adjustment=self, digits=0, draw_value=False)
        hbox.pack_start(scale_width, True, True, 0)

        return hbox

class MainWindow(Gtk.Window):
    START_HEIGHT = 10
    START_WIDTH = 10

    def __init__(self):
        Gtk.Window.__init__(self, title="The Game of Life")

        self.vbox = Gtk.HBox()
        self.add(self.vbox)

        self.hbox = Gtk.VBox()
        self.vbox.pack_start(self.hbox, False, True, 6)

        button = Gtk.Button(label="Start Start Start")
        button.connect('clicked', self.on_start_button_clicked)
        self.hbox.pack_start(button, False, False, 6)

        button = Gtk.Button(label="Fill randomly")
        button.connect('clicked', self.on_random_button_clicked)
        self.hbox.pack_start(button, False, False, 6)

        self.width_adj = Adjust(self.START_WIDTH, 5, 200, "Width : %s")
        self.width_adj.connect('value-changed', lambda c : self.computer.set_size(width=int(c.get_value())))
        self.hbox.pack_start(self.width_adj.create_widget(), False, False, 6)

        self.height_adj = Adjust(self.START_HEIGHT, 5, 200, "Height : %s")
        self.height_adj.connect('value-changed', lambda c : self.computer.set_size(height=int(c.get_value())))
        self.hbox.pack_start(self.height_adj.create_widget(), False, False, 6)

        self.iters_adj = Adjust(1, 1, 100, "Iterations : %s")
        self.hbox.pack_start(self.iters_adj.create_widget(), False, False, 6)

        self.canvas = Gtk.DrawingArea()
        self.vbox.pack_start(self.canvas, True, True, 0)

        self.computer = computer.LifeComputer(self.START_WIDTH, self.START_HEIGHT)
        self.computer.connect_changed_handler(self.grid_changed)

    def on_start_button_clicked(self, widget):
        self.computer.compute()

    def on_random_button_clicked(self, widget):
        self.computer.fill_random()

    def grid_changed(self, computer):
        print "Wow Very Change !"
        print computer.height
        print computer.width
        print computer[...]

if __name__ == '__main__':
    win = MainWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
