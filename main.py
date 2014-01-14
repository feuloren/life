#!/usr/bin/python
# -*- coding:utf-8 -*-

import cairo
from gi.repository import Gtk, Gdk, GObject, GLib

import computer

class Adjust(Gtk.Adjustment):
    def __init__(self, current, min, top, text):
        super(Gtk.Adjustment, self).__init__()

        self.configure(current, min, top+1, 1, 1, 1)
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

    def get_value(self):
        return int(super(Gtk.Adjustment, self).get_value())

class GridCanvas(Gtk.DrawingArea):
    __gsignals__ = {'click' : (GObject.SIGNAL_RUN_FIRST, None, (int,int,))}

    def __init__(self, array):
        super(Gtk.DrawingArea, self).__init__()

        self.border = 1
        self.size = 10

        self.array = array

        self.connect("draw", self.draw_cb)
        self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK |
                        Gdk.EventMask.BUTTON_RELEASE_MASK | #
                        Gdk.EventMask.BUTTON1_MOTION_MASK | #
                        Gdk.EventMask.POINTER_MOTION_HINT_MASK)
        self.connect("button-press-event", self.button_press_cb)
        self.connect("button-release-event", self.button_release_cb)
        self.connect("motion_notify_event", self.motion_event_cb)

    def draw_grid(self, array):
        self.array = array
        w = self.get_window()
        w.invalidate_region(w.get_visible_region(), False)

    def draw_cb(self, w, cr):
        cr.set_source_rgb(1, 1, 1)
        cr.paint()

        print(self.array.shape)

        for i, line in enumerate(self.array):
            for j, val in enumerate(line):
                cr.rectangle(self.border + ((self.border + self.size) * i),
                             self.border + ((self.border + self.size) * j),
                             self.size, self.size)
                if val == 1:
                    cr.set_source_rgb(1, 0.2, 0.3)
                else:
                    cr.set_source_rgb(0.9, 0.9, 0.9)
                cr.fill()

        print("draw")

    def button_press_cb(self, w, event):
        self.emit('click', event.x // (self.border + self.size), event.y // (self.border + self.size))
        print("button press")

    def button_release_cb(self, w, e):
        print("button release")

    def motion_event_cb(self, w, e):
        print("button move")

class MainWindow(Gtk.Window):
    START_HEIGHT = 5
    START_WIDTH = 5

    def __init__(self):
        Gtk.Window.__init__(self, title="The Game of Life")

        self.vbox = Gtk.HBox()
        self.add(self.vbox)

        self.hbox = Gtk.VBox()
        self.vbox.pack_start(self.hbox, False, True, 6)

        button = Gtk.Button(label="Start Start Start")
        button.connect('clicked', self.on_start_button_clicked)
        self.hbox.pack_start(button, False, False, 6)

        # Boutons
        button = Gtk.Button(label="Fill randomly")
        button.connect('clicked', self.on_random_button_clicked)
        self.hbox.pack_start(button, False, False, 6)

        # Slides
        self.size_adj = Adjust(5, 1, 100, "Size : %s")
        self.size_adj.connect('value-changed', self.set_size)
        self.hbox.pack_start(self.size_adj.create_widget(), False, False, 6)

        #self.width_adj = Adjust(self.START_WIDTH, 5, 200, "Width : %s")
        #self.width_adj.connect('value-changed', lambda c : self.computer.set_size(width=int(c.get_value())))
        #self.hbox.pack_start(self.width_adj.create_widget(), False, False, 6)
        #
        #self.height_adj = Adjust(self.START_HEIGHT, 5, 200, "Height : %s")
        #self.height_adj.connect('value-changed', lambda c : self.computer.set_size(height=int(c.get_value())))
        #self.hbox.pack_start(self.height_adj.create_widget(), False, False, 6)

        self.iters_adj = Adjust(1, 1, 100, "Iterations : %s")
        self.hbox.pack_start(self.iters_adj.create_widget(), False, False, 6)

        # LifeComputer
        self.computer = computer.LifeComputer(self.START_WIDTH, self.START_HEIGHT)
        self.computer.connect_changed_handler(self.grid_changed)

        # Aire de dessin
        self.canvas = GridCanvas(self.computer[...])
        self.canvas.connect('click', lambda w, x, y: self.computer.toggle(x,y))
        self.vbox.pack_start(self.canvas, True, True, 0)

        self.set_size_request(800, 500)

    def set_size(self, a):
        s = self.size_adj.get_value()
        self.computer.set_size(s, s)

    def on_start_button_clicked(self, widget):
        self.computer.compute()

        iters = self.iters_adj.get_value()
        if iters > 1:
            self.iterations_left = iters - 1
            GLib.timeout_add(200, self.compute)

    def compute(self):
        if self.iterations_left == 0:
            return False # arrêter les itérations

        self.computer.compute()
        self.iterations_left -= 1
        return True # continuer les itérations

    def on_random_button_clicked(self, widget):
        self.computer.fill_random()

    def grid_changed(self, computer):
        self.canvas.draw_grid(computer[...])

if __name__ == '__main__':
    win = MainWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
