# 该代码不需要，但是是人工智能生成的，有许多可以借鉴的地方
import bpy
import os
from pathlib import Path
from bpy_extras.io_utils import ExportHelper

# --- 常量 ---
SDF_VERSION = "1.11"
DEFAULT_AUTHOR = "Blender User"
DEFAULT_EMAIL = "user@example.com"


class ExportSDFModelPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_export_sdf"
    bl_label = "Export Static SDF Model"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        obj = context.object

        if obj is None or obj.type != 'MESH':
            layout.label(text="Select a MESH object!", icon='ERROR')
            return

        layout.label(text=f"Export '{obj.name}' as SDF model", icon='INFO')

        scene = context.scene
        layout.prop(scene, "sdf_model_name")
        layout.prop(scene, "sdf_author_name")
        layout.prop(scene, "sdf_author_email")
        layout.prop(scene, "sdf_mesh_format")
        layout.prop(scene, "sdf_save_dir")

        layout.separator()
        layout.operator("object.export_sdf_model", text="Export SDF Model", icon='EXPORT')


def generate_model_config(model_name, author_name, author_email):
    return f"""<?xml version="1.0"?>
<model>
  <name>{model_name}</name>
  <sdf version="{SDF_VERSION}">model.sdf</sdf>
  <version>1.0</version>
  <author>
    <name>{author_name}</name>
    <email>{author_email}</email>
  </author>
  <description>
    This model is made by Blender using the SDF Export Plugin.
    Plugin: https://github.com/yjphhw/sdf-export-plugin
  </description>
</model>
"""


def generate_model_sdf(model_name, mesh_format):
    return f"""<?xml version="1.0"?>
<sdf version="{SDF_VERSION}">
  <model name="{model_name}">
    <link name="body">
      <inertial auto="true"/>
      <collision name="collision">
        <density>1000.0</density>
        <geometry>
          <mesh optimization="convex_decomposition">
            <uri>model://{model_name}/mesh.{mesh_format}</uri>
          </mesh>
        </geometry>
      </collision>
      <visual name="visual">
        <geometry>
          <mesh>
            <uri>model://{model_name}/mesh.{mesh_format}</uri>
          </mesh>
        </geometry>
        <material>
          <diffuse>0.1 0.2 0.4 1.0</diffuse>
          <ambient>0.1 0.2 0.4 1.0</ambient>
          <specular>0.1 0.2 0.4 1.0</specular>
        </material>
      </visual>
    </link>
  </model>
</sdf>
"""


class ExportSDFModelOps(bpy.types.Operator):
    bl_idname = "object.export_sdf_model"
    bl_label = "Export SDF Model"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.object
        if not obj or obj.type != 'MESH':
            self.report({'ERROR'}, "Please select a mesh object!")
            return {'CANCELLED'}

        scene = context.scene
        model_name = scene.sdf_model_name.strip()
        author_name = scene.sdf_author_name.strip() or DEFAULT_AUTHOR
        author_email = scene.sdf_author_email.strip() or DEFAULT_EMAIL
        mesh_format = scene.sdf_mesh_format
        save_dir = bpy.path.abspath(scene.sdf_save_dir)

        # 输入验证
        if not model_name:
            self.report({'ERROR'}, "Model name cannot be empty!")
            return {'CANCELLED'}

        try:
            save_path = Path(save_dir)
            save_path.mkdir(parents=True, exist_ok=True)  # 自动创建目录
            model_dir = save_path / model_name

            if model_dir.exists():
                self.report({'ERROR'}, f"Model folder '{model_name}' already exists! Choose a new name.")
                return {'CANCELLED'}

            model_dir.mkdir()

            # 生成 SDF 文件
            config_xml = generate_model_config(model_name, author_name, author_email)
            sdf_xml = generate_model_sdf(model_name, mesh_format)

            (model_dir / "model.config").write_text(config_xml, encoding='utf-8')
            (model_dir / "model.sdf").write_text(sdf_xml, encoding='utf-8')

            # 导出网格
            mesh_path = model_dir / f"mesh.{mesh_format}"
            if mesh_format == 'glb':
                bpy.ops.export_scene.gltf(
                    filepath=str(mesh_path),
                    use_selection=True,
                    export_normals=True,
                    export_materials='EXPORT',
                    export_colors=True,
                    export_cameras=False,
                    export_lights=False,
                )
            elif mesh_format == 'stl':
                bpy.ops.export_mesh.stl(
                    filepath=str(mesh_path),
                    use_selection=True,
                    global_scale=1.0,
                    use_mesh_modifiers=True,
                    ascii=False
                )
            elif mesh_format == 'dae':
                # 确保 Collada 插件已启用
                if not hasattr(bpy.ops.wm, 'collada_export'):
                    self.report({'ERROR'}, "Collada export not available. Enable 'Import-Export: Autodesk COLLADA' add-on.")
                    return {'CANCELLED'}
                bpy.ops.wm.collada_export(
                    filepath=str(mesh_path),
                    selected=True,
                    apply_modifiers=True
                )

            self.report({'INFO'}, f"SDF model exported to: {model_dir}")
            return {'FINISHED'}

        except Exception as e:
            self.report({'ERROR'}, f"Export failed: {str(e)}")
            return {'CANCELLED'}


def register():
    # 使用带前缀的属性名，避免冲突
    bpy.types.Scene.sdf_model_name = bpy.props.StringProperty(
        name="Model Name",
        default="my_blender_model",
        description="Name of the SDF model"
    )
    bpy.types.Scene.sdf_author_name = bpy.props.StringProperty(
        name="Author Name",
        default=DEFAULT_AUTHOR
    )
    bpy.types.Scene.sdf_author_email = bpy.props.StringProperty(
        name="Author Email",
        default=DEFAULT_EMAIL
    )
    bpy.types.Scene.sdf_save_dir = bpy.props.StringProperty(
        name="Save Directory",
        default="//sdf_models",  # 相对 blend 文件
        subtype='DIR_PATH'       # 在 UI 中显示为文件夹选择器
    )
    bpy.types.Scene.sdf_mesh_format = bpy.props.EnumProperty(
        name="Mesh Format",
        items=[
            ('glb', "glTF Binary (.glb)", "Compact binary glTF format"),
            ('stl', "STL (.stl)", "Simple triangle mesh"),
            ('dae', "COLLADA (.dae)", "Requires Collada add-on enabled"),
        ],
        default='glb'
    )

    bpy.utils.register_class(ExportSDFModelPanel)
    bpy.utils.register_class(ExportSDFModelOps)


def unregister():
    bpy.utils.unregister_class(ExportSDFModelOps)
    bpy.utils.unregister_class(ExportSDFModelPanel)
    del bpy.types.Scene.sdf_model_name
    del bpy.types.Scene.sdf_author_name
    del bpy.types.Scene.sdf_author_email
    del bpy.types.Scene.sdf_save_dir
    del bpy.types.Scene.sdf_mesh_format


if __name__ == "__main__":
    register()