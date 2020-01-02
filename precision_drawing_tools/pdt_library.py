# ***** BEGIN GPL LICENSE BLOCK *****
#
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ***** END GPL LICENCE BLOCK *****
#
# -----------------------------------------------------------------------
# Author: Alan Odom (Clockmender), Rune Morling (ermo) Copyright (c) 2019
# -----------------------------------------------------------------------
#
import bpy
from bpy.types import Operator
from mathutils import Vector
from pathlib import Path
from .pdt_functions import debug, oops
from .pdt_msg_strings import PDT_ERR_NO_LIBRARY


class PDT_OT_LibShow(Operator):
    """Show Library File Details."""
    bl_idname = "pdt.lib_show"
    bl_label = "Show Library Details"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        """Shows Location Of PDT Library File.

        Args:
            context: Blender bpy.context instance.

        Returns:
            Status Set.
        """

        scene = context.scene
        pg = scene.pdt_pg
        file_path = context.preferences.addons[__package__].preferences.pdt_library_path
        pg.error = str(Path(file_path))
        debug("PDT Parts Library:")
        debug(f"{pg.error}")
        bpy.context.window_manager.popup_menu(oops, title="Information - Parts Library File", icon="INFO")
        return {"FINISHED"}


class PDT_OT_Append(Operator):
    """Append from Library at cursor Location."""

    bl_idname = "pdt.append"
    bl_label = "Append"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        """Appends Objects from PDT Library file.

        Appended Objects are placed at Cursor Location.

        Args:
            context: Blender bpy.context instance.

        Notes:
            Uses pg.lib_objects, pg.lib_collections & pg.lib_materials

        Returns:
            Status Set.
        """

        scene = context.scene
        pg = scene.pdt_pg
        obj_names = [o.name for o in context.view_layer.objects]
        file_path = context.preferences.addons[__package__].preferences.pdt_library_path
        path = Path(file_path)

        if path.is_file() and ".blend" in str(path):
            if pg.lib_mode == "OBJECTS":
                # Force object Mode
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.wm.append(
                    filepath=str(path), directory=str(path) + "/Object", filename=pg.lib_objects
                )
                for obj in context.view_layer.objects:
                    if obj.name not in obj_names:
                        obj.select_set(False)
                        obj.location = Vector(
                            (scene.cursor.location.x, scene.cursor.location.y, scene.cursor.location.z)
                        )
                return {"FINISHED"}
            elif pg.lib_mode == "COLLECTIONS":
                bpy.ops.wm.append(
                    filepath=str(path), directory=str(path) + "/Collection", filename=pg.lib_collections
                )
                for obj in context.view_layer.objects:
                    if obj.name not in obj_names:
                        obj.select_set(False)
                        obj.location = Vector(
                            (scene.cursor.location.x, scene.cursor.location.y, scene.cursor.location.z)
                        )
                return {"FINISHED"}
            elif pg.lib_mode == "MATERIALS":
                bpy.ops.wm.append(
                    filepath=str(path), directory=str(path) + "/Material", filename=pg.lib_materials
                )
                return {"FINISHED"}
        else:
            errmsg = PDT_ERR_NO_LIBRARY
            self.report({"ERROR"}, errmsg)
            return {"FINISHED"}


class PDT_OT_Link(Operator):
    """Link from Library at Object's Origin."""

    bl_idname = "pdt.link"
    bl_label = "Link"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        """Links Objects from PDT Library file.

        Linked Objects are placed at Cursor Location

        Args:
            context

        Notes:
            Uses pg.lib_objects, pg.lib_collections & pg.lib_materials

        Returns:
            Status Set.
        """

        scene = context.scene
        pg = scene.pdt_pg
        file_path = context.preferences.addons[__package__].preferences.pdt_library_path
        path = Path(file_path)
        if path.is_file() and ".blend" in str(path):
            if pg.lib_mode == "OBJECTS":
                # Force object Mode
                bpy.ops.object.mode_set(mode='OBJECT')
                bpy.ops.wm.link(
                    filepath=str(path), directory=str(path) + "/Object", filename=pg.lib_objects
                )
                for obj in context.view_layer.objects:
                    obj.select_set(False)
                return {"FINISHED"}
            elif pg.lib_mode == "COLLECTIONS":
                bpy.ops.wm.link(
                    filepath=str(path), directory=str(path) + "/Collection", filename=pg.lib_collections
                )
                for obj in context.view_layer.objects:
                    obj.select_set(False)
                return {"FINISHED"}
            elif pg.lib_mode == "MATERIALS":
                bpy.ops.wm.link(
                    filepath=str(path), directory=str(path) + "/Material", filename=pg.lib_materials
                )
                return {"FINISHED"}
        else:
            errmsg = PDT_ERR_NO_LIBRARY
            self.report({"ERROR"}, errmsg)
            return {"FINISHED"}
