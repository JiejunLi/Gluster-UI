#!/usr/bin/env python
# encoding=utf-8

# Copyright (C) 2015 Alljun Lee, CT
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA
#
# Refer to the README and COPYING files for full details of the license


import gtk, vte 
from utils import new_attr
from gluster_ui_constants import GTK_SIGNAL_CHILD_EXIT, GTK_SIGNAL_KEY_PRESS,\
                            GTK_SIGNAL_CLICKED, GLST_DEFAULT,\
                            GLST_COLOR_BUTTON_HEIGHT, GLST_LOG_WIN_WIDTH,\
                            GLST_LOG_WIN_HEIGHT, GLST_LOG_PAGE_BG,\
                            GLST_INIT_BTN_BG, GLST_SELECTED_BTN_BG,\
                            GLST_SELECTED_TAB_BG, GLST_INIT_BOX_BG,\
                            GLST_TEXT_HEIGHT, GLST_TEXT_WIDTH,\
                            GLST_ALIGNMENT_CONTENT_X, GLST_ALIGNMENT_CONTENT_Y,\
                            GLST_PADDING_TITLE, GLST_PADDING_LIST,\
                            GLST_PAGE_WIDGET_HPADDING, GLST_DEFAULT,\
                            GLST_PADDING_CONTENT_FIRST,\
                            GLST_PADDING_CONTENT_NEXT,\
                            GLST_PAGE_LISTS_HPADDING,\
                            GLST_BUTTON_LIST_HEIGHT


class ColorWidget(gtk.EventBox):

    def __init__(self, GtkWidget, *args, **kwargs):
        super(ColorWidget, self).__init__()
        self.color_widget = getattr(gtk, GtkWidget)(*args)
        self.add(self.color_widget)
        self.init_color = kwargs.get('init_color', None)

        label = kwargs.get('label', '')
        signals_to_handle = kwargs.get('signals_to_handle', [])

        if self.init_color is not None:
            self.change_color('bg', gtk.STATE_NORMAL, self.init_color)
        for signal in signals_to_handle:
            self.color_widget.connect(signal,
                    getattr(self, signal.replace('-', '_').lower() + '_cb'))
        if label:
            self.color_widget.set_label(label)

    def change_color(self, category, state, color):
        _color = gtk.gdk.Color(color)
        modifier = "modify_%s" % category
        if isinstance(self.color_widget, gtk.Label):
            getattr(self, modifier)(state, _color)
        else:
            getattr(self.color_widget, modifier)(state, _color)


class ColorNotebookTab(ColorWidget):

    def __init__(self, label, init_btn_bg=GLST_SELECTED_TAB_BG,
                 signals_to_handle=[]):
        super(ColorNotebookTab, self).__init__('Label', label=label,
                                        init_color=GLST_SELECTED_TAB_BG,
                                        signals_to_handle=signals_to_handle)
        self.show_all()

    def get_label(self):
        return self.color_widget.get_label()


class ColorButton(ColorWidget):

    def __init__(self, label, init_btn_bg=GLST_INIT_BTN_BG,
                 signals_to_handle=["focus-in-event", "focus-out-event",
                                    "state-changed"]):
        super(ColorButton, self).__init__('Button', label=label,
                                          init_color=GLST_INIT_BTN_BG,
                                          signals_to_handle=signals_to_handle)

    def focus_in_event_cb(self, widget, event):
        self.change_color('bg', gtk.STATE_NORMAL, GLST_SELECTED_BTN_BG)

    def focus_out_event_cb(self, widget, event):
        self.change_color('bg', gtk.STATE_NORMAL, GLST_INIT_BTN_BG)

    def state_changed_cb(self, widget, state):
        if state == gtk.STATE_PRELIGHT:
            self.change_color('bg', gtk.STATE_PRELIGHT, GLST_SELECTED_BTN_BG)


class Button(gtk.HButtonBox):

    def __init__(self, data):
        super(Button, self).__init__()
        labels = data['labels']
        btn_nr = len(labels)
        callbacks = data.get('callback', [lambda _:_]*btn_nr)
        signal = data.get('signal', 'clicked')
        btn_type = data.get('type', 'Button')
        self.set_layout(gtk.BUTTONBOX_END)
        self.btns = []
        for t, cb in zip(labels, callbacks):
            btn = getattr(gtk, btn_type)(t)
            btn.connect(signal, cb)
            self.btns.append(btn)
            self.pack_start(btn, False, False, padding=5)
        self.set_size_request(-1, GLST_BUTTON_LIST_HEIGHT)


class DetailedList(gtk.ScrolledWindow):

    def __init__(self, data):
        gtk.ScrolledWindow.__init__(self)
        self.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
        labels = data['labels']
        liststore = gtk.ListStore(*([str] * len(labels)))
        self.treeview = gtk.TreeView(liststore)
        if data.get('callback'):
            self.treeview.connect(data.get('signal',
                                    GTK_SIGNAL_CLICK_DETALLIST),
                                  data['callback'])
        # store a copy of datas for callback to use.
        self.treeview.treeview_datas = []
        for idx, label in enumerate(labels):
            self.treeview.insert_column_with_attributes(-1,
                label, gtk.CellRendererText(), text=idx)
        self.add(self.treeview)
        self._liststore = liststore
        self.treeview.set_size_request(-1, GLST_DETAILED_LIST_HEIGHT)

    def show_conf(self, list_of_entry):
        self._liststore.clear()
        for v in list_of_entry:
            self.treeview.treeview_datas.append(v)
            self._liststore.append(v)


class ConfirmDialog(gtk.MessageDialog):

    def __init__(self, message=""):
        super(ConfirmDialog, self).__init__(None,
                        gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                        gtk.MESSAGE_WARNING, gtk.BUTTONS_OK_CANCEL,
                        message)
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_title("Continue?")

    def run_and_close(self):
        resp_id = self.run()
        self.destroy()
        return resp_id


class ColorVBox(ColorWidget):

    def __init__(self, init_color, *args):
        super(ColorVBox, self).__init__('VBox', init_color=init_color, *args)
        self.set_border_width(0)
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color(init_color))


class GlstPage(ColorVBox):

    def __init__(self, layout):
        super(GlstPage, self).__init__(GLST_INIT_BOX_BG, False, 10)
        self.glst_widgets = {}
        for ir, item_row in enumerate(layout[2]):
            hbox = gtk.HBox(False)
            if ir == (len(layout[2]) - 1):
                hbox.pack_start(gtk.Label(), True, False)
            for i, item in enumerate(item_row):
                # check to create item via gtk basic class
                # or via comstum functions which is callable
                if callable(item['type']):
                    if item.get('params'):
                        _item = item['type'](item['params'])
                    else:
                        _item = item['type']()
                    item['type'] = 'custom'
                else:
                    _item = self._create_item(item)
                _item.get_conf = item.get('get_conf', None)
                _item.get_conf_args = item.get('get_conf_args', None)
                new_attr(self, item['name'] + '_' + item['type'], _item)
                self.glst_widgets['%s_%s' % (item['name'], item['type'])] = _item
                if isinstance(_item, DetailedList):
                    hbox.set_size_request(GLST_DEFAULT, GLST_DEFAILEDLIST_HEIGHT)
                if item.get('vhelp'):
                    hbox.set_size_request(GLST_DEFAULT, item['vhelp'])

                # We need to set 'DOUBLE ALIGNMENT HERE:'
                # first sets the alignment of text inside the hbox label.
                # then, sets the alignment of label inside the hbox.
                # and finally, pack the widget into the hbox.
                if hasattr(_item, 'set_alignment'):
                    if isinstance(_item, gtk.Entry):
                        _item.set_alignment(GLST_ALIGNMENT_CONTENT_X)
                    else:
                       _item.set_alignment(GLST_ALIGNMENT_CONTENT_X,
                                           GLST_ALIGNMENT_CONTENT_Y)
                alig = gtk.Alignment()
                alig.add(_item)
                if item.get('title'):
                   alig.set_padding(0, 0, GLST_PADDING_TITLE, 0)
                else:
                    if i == 0:
                        if i == len(item_row) - 1:
                            alig.set_padding(0, 0, GLST_PADDING_CONTENT_FIRST, 20)
                        else:
                            alig.set_padding(0, 0, GLST_PADDING_CONTENT_FIRST, 0)
                    else:
                        if i == len(item_row) - 1:
                            alig.set_padding(0, 0, GLST_PADDING_CONTENT_NEXT, 20)
                        else:
                             alig.set_padding(0, 0, GLST_PADDING_CONTENT_NEXT, 0)
                if isinstance(_item, (gtk.CheckButton, DetailedList)):
                    alig.set(0, 0, 1, 1)
                    alig.set_padding(0, 0, GLST_PADDING_LIST, GLST_PADDING_LIST)
                    hbox.pack_start(alig, True, True)
                else:
                    hbox.pack_start(alig, False, False)
            self.color_widget.pack_start(hbox, False, False,
                                padding=GLST_PAGE_WIDGET_HPADDING)

    def _create_item(self, data):
        itype = data['type']
        label = data.get('label')
        value = data.get('value')
        callbacks = data.get('callbacks')
        callbacks_signals = data.get('callback_sigs')
        init_func = data.get('init_func')
        init_func_args = data.get('init_func_args')
        item = getattr(gtk, itype)()
        item.set_size_request(GLST_DEFAULT, GLST_TEXT_HEIGHT)
        if value and hasattr(item, 'set_text'):
            item.set_text(value)
        elif label and hasattr(item, 'set_label'):
            item.set_label(label)
        if itype == 'Label':
            text_width = data.get('width') or GLST_TEXT_WIDTH
            item.set_width_chars(text_width)
            if len(label) > GLST_TEXT_WIDTH:
                item.set_line_warp(True)
                item.set_size_request(GLST_DEFAULT,
                                GLST_TEXT_HEIGHT*((len(label)//text_width)+1))
        if init_func is not None:
            for func, args in zip(init_func, int_func_args):
                getattr(item, func)(*args)
        if callbacks is not None:
            for cb, sig in zip(callbacks, callback_signals):
                item.connect(sig, cb)
        return item


class ShellWindow(gtk.Window):

    def __init__(self, parent=None, confirm=False, confirm_msg=""):
        super(ShellWindow, self).__init__(gtk.WINDOW_TOPLEVEL)
        self.set_title('Terminal')
        self.is_shell_hide = False
        self.is_shell_exited = True
        self.swparent = parent
        self.confirm = confirm
        self.confirm_msg = confirm_msg
        self.swparent.connect(GTK_SIGNAL_KEY_PRESS, self.toggle)
        self.connect(GTK_SIGNAL_KEY_PRESS, self.toggle)

    def shell_show(self, command=None):
        if self.is_shell_exited:
            if self.swparent:
                w, h = self.swparent.get_size()
                self.set_size_request(w, h)
                self.set_position(gtk.WIN_POS_CENTER)

            self.shell_main = vte.Terminal()
            self.shell_main.fork_command()
            self.shell_main.connect(GTK_SIGNAL_CHILD_EXIT, self.shell_exit)

            if command:
                self.shell_main.feed_child(command)

            self.add(self.shell_main)
            self.is_shell_exited = False
            self.show_all()
        elif self.is_shell_hide:
            self.is_shell_hide = False
            self.present()

    def shell_exit(self, terminal):
        terminal.destroy()
        self.hide()
        self.is_shell_exited = True

    def toggle(self, widget, event):
        key = gtk.gdk.keyval_name(event.keyval)
        if key == 'F2':
            if self.is_shell_exited or self.is_shell_hide:
                if self.confirm == False or \
                ConfirmDialog(self.confirm_msg).run_and_close() == \
                gtk.RESPONSE_OK:
                    self.shell_show()
                else:
                    self.hide()
                    self.is_shell_hide = True


class LogWindow(gtk.Window):

    def __init__(self, parent=None):
        super(LogWindow, self).__init__(gtk.WINDOW_TOPLEVEL)
        self.logshell = ShellWindow(self)
        self.set_position(gtk.WIN_POS_CENTER)
        self.set_title('Logging Terminal')
        self.is_logwin_hide = True
        self.files = ('/var/log/messages', '/var/log/glusterfs/cli.log',
                        '/var/log/vdsm/vdsm.log')

        if parent:
            self.swparent = parent
            w, h = self.swparent.get_size()
            self.set_size_request(w, h)
            self.swparent.connect(GTK_SIGNAL_KEY_PRESS, self.toggle)
        self.connect(GTK_SIGNAL_KEY_PRESS, self.toggle)
        v = gtk.VBox(False, 1)
        v.pack_start(gtk.Label("Choose log file to view"), False, False)
        sg_btn = gtk.SizeGroup(gtk.SIZE_GROUP_BOTH)

        for f in self.files:
            btn = ColorButton(f.split('/')[-1])
            btn.color_widget.connect(GTK_SIGNAL_CLICKED, self.log_show, f)
            btn.color_widget.set_size_request(GLST_DEFAULT, GLST_COLOR_BUTTON_HEIGHT)

            sg_btn.add_widget(btn)
            h = gtk.HBox()
            h.pack_start(btn, True, False)
            v.pack_start(h, False, False)

        btn_back = ColorButton('Back')
        btn_back.color_widget.connect(GTK_SIGNAL_CLICKED,
                            lambda _: self.hide())

        alignb = gtk.Alignment()
        alignb.add(btn_back)
        alignb.set_size_request(GLST_LOG_WIN_WIDTH, GLST_LOG_WIN_HEIGHT)
        sg_btn.add_widget(btn_back)
        alignb.set(1, 1, 0, 0)
        v.pack_start(alignb, True, False)

        align = ColorWidget('Alignment', 0.5, 0.5, 0, 0,
                            init_color=GLST_LOG_PAGE_BG)
        align.color_widget.add(v)
        self.add(align)

    def toggle(self, widget, event):
        key = gtk.gdk.keyval_name(event.keyval)
        if key == 'F8':
            if self.is_logwin_hide:
                self.show_all()
            else:
                self.hide()
            self.is_logwin_hide = not self.is_logwin_hide

    def log_show(self, _, filename):
        self.logshell.shell_show('tail -f %s; exit\n' % filename)
