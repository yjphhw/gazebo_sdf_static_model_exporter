import xml.etree.ElementTree as ET
import random

def generate_model_config_xml(
    model_name: str,
    version: str = "1.11",
    author_name: str = "yjphhw",
    author_email: str = "yjphhw@qq.com",
    description: str = '',
) -> str:
    """
    Generate a Gazebo model.config XML with full extensibility.
    Args:
        model_name: Name of the model.
        version: Model version (not SDF version).
        author_name: Author name.
        author_email: Author email.
        description: Model description.
    Returns:
        XML string in model.config format.
    """

    root = ET.Element("model")
    # Basic fields
    ET.SubElement(root, "name").text = model_name
    ET.SubElement(root, "version").text = version
    # Author
    author = ET.SubElement(root, "author")
    ET.SubElement(author, "name").text = author_name
    ET.SubElement(author, "email").text = author_email
    # Description
    if description == '':
        description = (
            "This model is made by Blender SDF Exporter Extention!\n"
            "This model is created by sdf-export-plugin.\n"
            "The plugin home is: sdfexportplugin.yjphhw.github.com."
        )

    ET.SubElement(root, "description").text = description
    
    sdf_elem = ET.SubElement(root, "sdf", version=version)

    sdf_elem.text = "model.sdf"

    # Add XML declaration manually (ET doesn't include it by default)
    ET.indent(root) 
    rough_string = ET.tostring(root, encoding="unicode")

    xml_with_decl = '<?xml version="1.0" ?>\n' + rough_string

    return xml_with_decl

def generate_static_sdf_xml(
    model_name: str,
    sdf_verson: str = "1.11",
    mesh_format: str = "obj", 
    hastexture: bool = False
) -> str:
    """
    Generate a basic SDF model XML string for Gazebo/Ignition.
    Args:
        model_name (str): Name of the model.
        sdf_verson (str): SDF version (e.g., "1.10", "1.11").
        mesh_format (str): Mesh file extension (e.g., "obj", "dae", "stl").
    Returns:
        str: Formatted SDF XML string.
    """
    # Create root <sdf> element with version attribute
    sdf = ET.Element("sdf", version=sdf_verson)
    # <model name="...">
    model = ET.SubElement(sdf, "model", name=model_name)
    # <link name="body">
    link = ET.SubElement(model, "link", name="body")
    # <inertial auto="true" />
    ET.SubElement(link, "inertial", auto="true")
    # --- Collision ---
    collision = ET.SubElement(link, "collision", name="collision")
    density = ET.SubElement(collision, "density")
    density.text = "10.0"
    geometry_col = ET.SubElement(collision, "geometry")
    mesh_col = ET.SubElement(geometry_col, "mesh", optimization="convex_decomposition")
    uri_col = ET.SubElement(mesh_col, "uri")
    uri_col.text = f"models://{model_name}/mesh.{mesh_format}"
    # --- Visual ---
    visual = ET.SubElement(link, "visual", name="visual")
    geometry_vis = ET.SubElement(visual, "geometry")
    mesh_vis = ET.SubElement(geometry_vis, "mesh")
    uri_vis = ET.SubElement(mesh_vis, "uri")
    uri_vis.text = f"models://{model_name}/mesh.{mesh_format}"

    if not hastexture:
        # Material
        material = ET.SubElement(visual, "material")
        diffuse = ET.SubElement(material, "diffuse")
        diffuse.text =' '.join( [ '{:.2}'.format(random.random()) for _ in range(3)] + ['1.0'])
        ambient = ET.SubElement(material, "ambient")
        ambient.text = ' '.join( [ '{:.2}'.format(random.random()) for _ in range(3)] + ['1.0'])
        specular = ET.SubElement(material, "specular")
        specular.text = ' '.join( [ '{:.2}'.format(random.random()) for _ in range(3)] + ['1.0'])


    # Optional: Add indentation for readability (Python 3.9+)
    ET.indent(sdf)

    # Convert to string with XML declaration
    xml_str = ET.tostring(sdf, encoding="unicode")
    return f'<?xml version="1.0"?>\n{xml_str}'


if __name__=='__main__':
    print(generate_model_config_xml('test'))
    print(generate_static_sdf_xml('test', hastexture=True))