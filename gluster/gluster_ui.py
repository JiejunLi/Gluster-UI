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


import gtk
from gluster_ui_constants import CmdBase
from gluster_ui_widgets import Button


class WidgetBase(dict):

    def __init__(self, name, itype, label='', value='', **kwargs):
        super(WidgetBase, self).__init__(self)
        self.__setitem__('type', itype)
        self.__setitem__('name', name)
        self.__setitem__('label', label)
        self.__setitem__('value', value)

        for key in ('title', 'get_conf', 'get_conf_args',
                    'set_conf', 'set_conf_args',
                    'show_conf', 'conf_path',
                    'params', 'vhelp', 'width',
                    'init_func', 'init_func_args',
                    'callbacks', 'callback_sigs'):
            v = kwargs.get(key, None)
            self.__setitem__(key, v)


class GlstLayout(list):

    def __init__(self, name, tab_string):
        super(GlstLayout, self).__init__()
        self.append(name)
        self.append(tab_string)


class GlstCreate(GlstLayout):

    def __init__(self):
        super(GlstCreate, self).__init__('create', 'Create Volume')

    def confirm_cmd(self, obj):
        from gluster import glst
        page = glst.page_create
        volname = page.volume_name_value_Entry.get_text()
#        voltype = page.volume_type_value_Entry.get_text()
        brickpath = page.volume_brick_value_Entry.get_text()
        if obj.get_label() == 'force create':
            warn_message = "Warn froce create volume"
            if resp_id == gtk.RESPONSE_OK:
                cmd = '/usr/sbin/gluster volume create %s %s force' % (volname, brickpath)
                commands.getoutput(command)
        else:
            if resp_id == gtk.RESPONSE_OK:
                cmd = '/usr/sbin/gluster volume create %s %s' % (volname, brickpath)


    def get_layout(self):
        create = WidgetBase('create', 'Label', 'Please input volume params', title=True)
        volume_name_label = WidgetBase('volume_name_label', 'Label', \
                                       'Volume Name:')
        volume_name_value = WidgetBase('volume_name_value', 'Entry', '', 'volName')
        volume_type_label = WidgetBase('volume_type_label', 'Label', \
                                       'Volume Type:')
        volume_type_value = WidgetBase('volume_type_value', 'Entry', '', 'distribute')
        volume_brick_label = WidgetBase('volume_brick_label', 'Label', \
                                        'Block Path:')
        volume_brick_value = WidgetBase('volume_brick_value', 'Entry', '', 'ip:/volPath')

        create_button = WidgetBase('create_button', Button, '', params={'labels': ['create', 'force create'], 'callback': [self.confirm_cmd, self.confirm_cmd]})
#        create_params = WidgetBase('create_apply', ApplyRestBtn, params={'apply_cb':self.create_apply_cb})

        self.append([
                    (create,),
                    (volume_name_label, volume_name_value), \
                    (volume_type_label, volume_type_value), \
                    (volume_brick_label, volume_brick_value),\
                    (WidgetBase('empty', 'Label', '', vhelp=100),),
                    (create_button,),
                    ])
        return self

#    def create_apply_cb(self, btn):
#        from gluster import glst
#        page = glst.page_create
#        name = page.volume_name_value_Entry.get_text()
#        tyep = page.volume_type_value_Entry.get_text()
#        bricks = page.volume_brick_value_Entry.get_text()


class GlstDelete(GlstLayout):

    def __init__(self):
        super(GlstDelete, self).__init__('delete', 'Delete Volume')

    def get_layout(self):
        delete = WidgetBase('delete', 'Label', 'Please input volume name', title=True)
        volume_name_label = WidgetBase('volume_name_label', 'Label', 'Volume Name:')
        volume_name_value = WidgetBase('volume_name_value', 'Entry', '', 'volName')

        self.append([
                    (delete,),
                    (volume_name_label, volume_name_value),
                    (WidgetBase('empty', 'Label', '', vhelp=100),),
                    ])
        return self

class GlstStatus(GlstLayout):

    def __init__(self):
        super(GlstStatus, self).__init__('status', 'Volume Status')

    def get_layout(self):
        status = WidgetBase('status', 'Label', 'Please input volume name', title=True)
        volume_name_label = WidgetBase('volume_name_label', 'Label', 'Volume Name:')
        volume_name_value = WidgetBase('volume_name_value', 'Entry', '', 'volName')
        self.append([
                    (status,),
                    (volume_name_label, volume_name_value),
                    (WidgetBase('Empty', 'Label', '', vhelp=100),),
                    ])
        return self

class GlstInfo(GlstLayout):

    def __init__(self):
        super(GlstInfo, self).__init__('info', 'Volume Info')

    def get_layout(self):
        info = WidgetBase('info', 'Label', 'Please input volume name', title=True)
        volume_name_label = WidgetBase('volume_name_label', 'Label', 'Volume Name:')
        volume_name_value = WidgetBase('volume_name_value', 'Entry', '', 'volName')
        self.append([
                    (info,),
                    (volume_name_label, volume_name_value),
                    (WidgetBase('Empty', 'Label', '', vhelp=100),),
                    ])
        return self

class GlstSet(GlstLayout):

    def __init__(self):
        super(GlstSet, self).__init__('set', 'Volume Set')

    def get_layout(self):
        set = WidgetBase('set', 'Label', 'set volume properties', title=True)
        volume_properties_label = WidgetBase('volume_properties_label', 'Label', 'Properties')
        volume_properties_value = WidgetBase('volume_properties_value', 'Entry', '', 'value')
        self.append([
                    (set,),
                    (volume_properties_label, volume_properties_value),
                    (WidgetBase('Empty', 'Label', '', vhelp=100),),
                    ])
        return self

class GlstPeer(GlstLayout):

    def __init__(self):
        super(GlstPeer, self).__init__('Peer', 'Peer')

    def get_layout(self):
        peer = WidgetBase('peer', 'Label', 'gluster peer', title=True)
        gluster_peer_label  = WidgetBase('gluster_peer_label', 'Label', 'hostIP')
        gluster_peer_value = WidgetBase('gluster_peer_value', 'Entry', '', 'value')
        self.append([
                    (peer,),
                    (gluster_peer_label, gluster_peer_value),
                    (WidgetBase('Empty', 'Label', '', vhelp=100),),
                    ])
        return self

layouts = \
        [
            GlstCreate().get_layout(),
            GlstDelete().get_layout(),
            GlstStatus().get_layout(),
            GlstInfo().get_layout(),
            GlstSet().get_layout(),
            GlstPeer().get_layout(),
        ]
#            GlstHelp().get_layout(),
#        ]
