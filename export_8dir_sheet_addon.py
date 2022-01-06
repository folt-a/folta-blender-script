
import bpy
from bpy.props import StringProperty, IntProperty, BoolProperty
import rna_keymap_ui  # キーマップリストに必要
import datetime
import math

################################################
# アドオン情報
bl_info = {
    "name": "Folta Export Chara Chipset",
    "author": "Folta",
    "version": (1, 0, 0),
    "blender": (2, 93, 2),
    "location": "",
    "description": "",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "UI"
}


##################################################
##################################################
# 翻訳辞書
BKTEMPLATE_translation_dict = {
    "en_US": {
        ("*", "hoge"):
        "ほげ",
    },
    "ja_JP": {
        ("*", "hoge"):
        "ほげ",
    }
}


##################################################
##################################################
# アドオン設定
class BKTEMPLATE_Preferences(bpy.types.AddonPreferences):
    bl_idname = __name__
    ################################################
    # アドオンプロパティ(ここのプロパティの状態はユーザー設定で保存される)
    # bktemplate_addon_setting_bool = bpy.props.BoolProperty(
    #     default=True, name="Bool", description="Bool")

    ################################################

    def draw(self, context):
        layout = self.layout

        preferences = bpy.context.preferences
        # addon_prefs = bpy.context.preferences.addons[__name__].preferences

        # layout.label(text="AddonPreferencesSample")

        # layout.prop(addon_prefs, "bktemplate_addon_setting_bool")

        ################################################
        # キーマップリスト
        box = layout.box()
        col = box.column()

        col.label(text="Keymap List:", icon="KEYINGSET")

        kc = bpy.context.window_manager.keyconfigs.addon
        for km, kmi in addon_keymaps:
            km = km.active()
            col.context_pointer_set("keymap", km)
            rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)

        ################################################
        # URL
        # row = layout.row()
        # row.label(text="Link:", icon="NONE")

        # row.operator(
        #     "wm.url_open", text="gumroad",
        #     icon="URL").url = "https://gum.co/VLdwV"
        # layout.label(text="",icon="NONE")


################################################
class EXPORT_OT_SimpleOperator(bpy.types.Operator):
    bl_idname = "export.simple_operator"
    bl_label = "出力"
    bl_description = ""
    bl_options = {'REGISTER', 'UNDO'}

    bktemplate_operator_bool = BoolProperty(
        default=True, name="bktemplate_operator_bool", description="bktemplate_operator_bool")

    def execute(self, context):
        addon_prefs = bpy.context.preferences.addons[__name__].preferences

        print("8Dir SpritesSheet Export")
        print(datetime.datetime.now().time())

        lightZ = [135,
                  90,
                  45,
                  0,
                  315,
                  270,
                  225,
                  180]

        # lightZ = [0,
        #           45,
        #           90,
        #           135,
        #           180,
        #           225,
        #           270,
        #           315]

        lights = []
        cameras = []
        for i in bpy.context.visible_objects:
            if i.type == "LIGHT":
                lights.append(i)
                print(i.name)
            if i.type == "CAMERA":
                cameras.append(i)
                # print(i.name)
                # print(i.location)
        sorted_cameras = cameras.sort(key=lambda obj: obj.name)

        for item in cameras:
            print(item.name)

        for index, v in enumerate(lightZ):
            bpy.data.scenes['Scene'].camera = cameras[index]
            # lights[0].location = vector3s[index]
            # lights[0].rotation_euler[2] = v
            for light in lights:
                light.rotation_euler[2] = v
            # print(lights[0].rotation_euler[2])
            # print(cameras[index].name)
            scene = bpy.context.scene
            tmp_names = []
            tmp_name1 = ""
            tmp_name2 = ""
            tmp_name3 = ""
            tmp_name4 = ""
            for node in scene.node_tree.nodes:
                if node.type == 'OUTPUT_FILE':
                    # 名前保持

                    for slot_index, file_slot in enumerate(node.file_slots):
                        tmp_names.append(file_slot.path)
                        # tmp_name1 = node.file_slots[0].path
                        # tmp_name2 = node.file_slots[1].path
                        # tmp_name3 = node.file_slots[2].path
                        # tmp_name4 = node.file_slots[3].path

                        file_slot.path = cameras[index].name + file_slot.path
                        # node.file_slots[0].path = cameras[index].name + node.file_slots[0].path
                        # node.file_slots[1].path = cameras[index].name + node.file_slots[1].path
                        # node.file_slots[2].path = cameras[index].name + node.file_slots[2].path
                        # node.file_slots[3].path = cameras[index].name + node.file_slots[3].path
                        # print(node.file_slots[slot_index].path)
                        # node.file_slots[4].path = '####_' + cameras[index].name

            bpy.ops.render.render(animation=True)

            for node in scene.node_tree.nodes:
                if node.type == 'OUTPUT_FILE':
                    # 名前を戻す
                    for slot_index, file_slot in enumerate(node.file_slots):
                        file_slot.path = tmp_names[slot_index]

                    # node.file_slots[0].path = tmp_name1
                    # node.file_slots[1].path = tmp_name2
                    # node.file_slots[2].path = tmp_name3
                    # node.file_slots[3].path = tmp_name4
                    # print(node.file_slots[0].path)
                    # node.file_slots[4].path = '####_' + cameras[index].name
        print("FINISHED")
        lights[0].rotation_euler[2] = lightZ[0]
        return{'FINISHED'}

################################################
# クラスの登録
classes = (
    BKTEMPLATE_Preferences,
    EXPORT_OT_SimpleOperator,
)


################################################
addon_keymaps = []


def register():
    ################################################
    # クラスの登録
    for cls in classes:
        bpy.utils.register_class(cls)

    ################################################
    # 辞書の登録
    bpy.app.translations.register(__name__, BKTEMPLATE_translation_dict)  # 辞書

    ################################################
    # キーマップ
    wm = bpy.context.window_manager.keyconfigs.addon.keymaps.new

    # km = wm(name = 'Mesh', space_type='EMPTY', region_type='WINDOW', modal=False)
    km = wm(name='3D View Generic', space_type='VIEW_3D')
    kmi = km.keymap_items.new(
        "export.simple_operator", 'A', 'PRESS', alt=True, shift=True, ctrl=True)
    addon_keymaps.append((km, kmi))
    kmi.active = True


################################################
def unregister():
    ################################################
    # クラスの削除
    for cls in classes:
        bpy.utils.unregister_class(cls)

    ################################################
    # 辞書の削除
    bpy.app.translations.unregister(__name__)   # 辞書の削除

    ################################################
    # キーマップの削除
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


################################################
if __name__ == "__main__":
    register()
