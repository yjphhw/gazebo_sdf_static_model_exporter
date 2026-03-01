import bpy
from  pathlib import Path
from .sdf_temp import generate_model_config_xml, generate_static_sdf_xml
# a blender extension to export sdf model, specifically for static sdf model.
# Gazebo version should bigger than Harmonic

# --- 常量 ---
SDF_FORMAT = "1.11"
DEFAULT_AUTHOR = "yjphhw"
DEFAULT_EMAIL = "yjphhw@qq.com"
DEFAULT_MODEL_NAME = "my_blender_model"


class ExportSDFModelPanel(bpy.types.Panel):
    bl_idname = "OBJECT_PT_export_sdf"
    bl_label = "Export Static SDF Model"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        scene = context.scene
        layout= self.layout
   
        obj=context.object
        if obj is None or obj.type != "MESH":
            layout.label(text='Current object is not mesh, select mesh and retry please !')
            return 
        obj.select_set(True)    #设置为选中
        layout.label(text=f"Object '{obj.name}' will export as SDF Static Model!")
        
        layout.prop(scene, "model_name", )
        layout.prop(scene, "author_name", )
        layout.prop(scene, "author_email", )
        layout.prop(scene, "mesh_format", )
        layout.prop(scene, "save_dir", )
        layout.prop(scene, "exporttexture", )
        # 按钮
        layout.operator("object.exportsdfmodel", text="执行操作")



class ExportSDFModelOps(bpy.types.Operator):
    bl_idname = "object.exportsdfmodel"
    bl_label = "exportsdf"
    
    def execute(self, context):
        scene = context.scene
        
        model_name = scene.model_name
        save_dir= scene.save_dir
        
        model_dir=Path(save_dir)/model_name
        isexporttexture=scene.exporttexture

        if model_dir.exists():
            raise Exception( 'model path exists ! change model_name, and try again!')

        #model_dir.mkdir()
        #make model and thumbnails directory
        (model_dir/'thumbnails').mkdir(parents=True)

        #save model thumbnails
        bpy.context.scene.render.filepath = str(model_dir/'thumbnails/1.png')
        bpy.context.scene.render.image_settings.file_format = 'PNG'
        #bpy.ops.render.render(write_still=True)
        bpy.ops.render.opengl(write_still=True)

        # below loacals() use below variables
        sdf_format = SDF_FORMAT
        author_name=scene.author_name
        author_email=scene.author_email
        
        mesh_format=scene.mesh_format

        config_xml=generate_model_config_xml(model_name, sdf_format, author_name, author_email)

        sdf_pattern=generate_static_sdf_xml(model_name, sdf_format, mesh_format, isexporttexture)

        (model_dir / "model.config").write_text(config_xml, encoding='utf-8')
        (model_dir / "model.sdf").write_text(sdf_pattern, encoding='utf-8')

        if mesh_format=='glb':
            #bpy.ops.export_scene.gltf(filepath= str(model_dir/'mesh.glb'), 
            #use_selection=True, export_copyright='Exported from Blender',
            #export_keep_originals=True   ,export_normals=True,)  #texture is node exported
            bpy.ops.export_scene.gltf(
                filepath=str(model_dir/'mesh.glb'),
                # 对象选择
                use_selection=True,          # 仅导出选中对象
                # 材质与纹理
                export_materials='EXPORT',            # 导出材质（必须！）
                export_image_format='JPEG',           # 自动选择 PNG/JPEG（根据图像）
                export_unused_images=True,              # 不导出未使用的图像
                export_texcoords=True,                   # 导出 UV（必须有纹理才有效）
                export_normals=True,                  # 导出法线
                export_tangents=False,                # 通常不需要，除非 PBR 需要
                # 纹理嵌入（关键！）
                export_keep_originals=False,          # ❗必须为 False 才能嵌入纹理到 GLB
                export_extras=False,                  # 是否导出自定义属性（可选）
                # 其他
                export_yup=True,                      # glTF 使用 Y-up 坐标系（标准）
                export_apply=True,                    # 应用修改器和变换（推荐）
                export_cameras=False,
                export_lights=False,
                export_copyright="Made with Blender SDF Exporter",    # 可选版权信息
                export_format="GLB",
                )
        elif mesh_format =='stl':
            # 导出选中对象为二进制 STL，应用修改器，使用 Blender 默认坐标系
            bpy.ops.wm.stl_export(
                filepath=str(model_dir/f'mesh.stl'),
                export_selected_objects=True,   # 只导出选中对象
                ascii_format=False,             # 二进制格式（更小）
                apply_modifiers=True,           # 应用修改器
                global_scale=1.0,               # 不缩放
                forward_axis='Y',
                up_axis='Z')
        elif mesh_format == 'obj':
            bpy.ops.wm.obj_export(
              filepath=str(model_dir/f'mesh.obj'),
              check_existing=True,
              export_selected_objects=True,      # Only export selected objects
              export_uv=True,                    # Essential for textures
              export_normals=True,
              export_colors=False,
              export_materials=isexporttexture,  # Generate .mtl file
              export_pbr_extensions=False,       # Keep it simple (no PBR in basic OBJ)
              path_mode='COPY',                  # 🔑 COPY textures to output dir!
              forward_axis='Y',
              up_axis='Z',
              global_scale=1.0,
              apply_modifiers=True,
              apply_transform=True,
              export_triangulated_mesh=False,    # Set True if Gazebo needs triangles
            )
        else:
            bpy.ops.wm.collada_export(filepath= str(model_dir/'mesh.dae'),
            selected=True,)
        
        def draw(self, context):
            self.layout.label(text="模型已成功导出！")
        context.window_manager.popup_menu(draw, title="操作完成", icon='INFO')
        return {'FINISHED'}
   

def register():
    bpy.types.Scene.model_name = bpy.props.StringProperty(
        name="Model Name",
        default=DEFAULT_MODEL_NAME
    )
    
    
    bpy.types.Scene.author_name = bpy.props.StringProperty(
        name="Author Name",
        default=DEFAULT_AUTHOR
    )
    bpy.types.Scene.author_email = bpy.props.StringProperty(
        name="Author Email",
        default=DEFAULT_EMAIL
    )
    
    
    bpy.types.Scene.save_dir = bpy.props.StringProperty(
        name="Save Dir",
        default="./",
        subtype='DIR_PATH'       # 在 UI 中显示为文件夹选择器
    )

    bpy.types.Scene.exporttexture = bpy.props.BoolProperty(
      name="Export Texture",
      default=True
      )
    
    # 定义枚举项列表
    mesh_formats = [
    ("obj", "obj", "这是第一个选项"), 
    #("glb", "glb", "这是第二个选项"),  #glob has problem
    ("stl", "stl", "这是第三个选项"),
    # dae blender5.0 not support
    ]
    # 注册场景属性
    bpy.types.Scene.mesh_format = bpy.props.EnumProperty(
    name="Mesh Format",
    description="从列表中选择一个选项",
    items=mesh_formats,
    default="stl"
    )
    '''
    bpy.types.Scene.b = bpy.props.FloatProperty(
        name="b",
        default=1.0,
        min=0,
        max=10
    )'''
    
    bpy.utils.register_class(ExportSDFModelPanel)
    bpy.utils.register_class(ExportSDFModelOps)


def unregister():
    bpy.utils.unregister_class(ExportSDFModelOps)
    bpy.utils.unregister_class(ExportSDFModelPanel)
    del bpy.types.Scene.model_name
    del bpy.types.Scene.author_name 
    del bpy.types.Scene.author_email 
    del bpy.types.Scene.save_dir 
    del bpy.types.Scene.mesh_format 


if __name__=='__main__':
    register()




