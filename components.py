import xml.etree.ElementTree as ET
import json
import html

def parse_drawio_xml(xml_data):
    with open(xml_data, 'r', encoding='utf-8') as file:
        data = file.read()
    root = ET.fromstring(data)

    components = {}
    i=0
    for child in root.iter('mxCell'):
        cell_id = child.attrib.get('id')
        cell_value = child.attrib.get('value', '').strip()

        # Check if id is between 2 and 56 and value is not empty
        if cell_id and cell_value:
            # Decode HTML entities and strip tags
            decoded_value = html.unescape(cell_value).replace('<div>', '_').replace("<br>", "_").replace('</div>', '')
#             decoded_value = ' '.join(re.findall(r'[A-Z][a-z]*', decoded_value))
            component = {'id': cell_id, 'type': decoded_value}
            components[i+1] = component
            i=i+1
    return components

def detect_components_from_drawio(xml_data):
    # Parse the XML data
    components = parse_drawio_xml(xml_data)
    print(components)
    # Map detected components to Docker images
    detected_components_to_docker_images = []
    encountered_component_types = set()

    for key,component in components.items():
        component_type = component["type"]

#         # Load the configuration file
#         with open("config.json") as f:
#             configuration = json.load(f)

        # Check if the component type has been encountered before
        if component_type not in encountered_component_types:

            # Append Docker image to the list only once for each component type
            docker_image = load_config("config.json")[component_type]
            docker_component={'type': component_type, 'image': docker_image['image'], 'name': docker_image['name']}
            detected_components_to_docker_images.append(docker_component)

            # Mark the component type as encountered
            encountered_component_types.add(component_type)


    return detected_components_to_docker_images

def load_config(config_path):
    with open(config_path) as f:
        configuration = json.load(f)

    component_to_docker_image_mapping = {}

    for component_type, docker_image in configuration.items():
        component_to_docker_image_mapping[component_type] = docker_image

    return component_to_docker_image_mapping

result= detect_components_from_drawio('fake architecture.drawio.xml')
print(result)

def generate_terraform_plan(detected_components_to_docker_images, plan_output_path="./main.tf"):

    config_text = """terraform {
  required_providers {
    docker = {
      source = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
}

provider "docker" {
  host    = "npipe:////.//pipe//docker_engine"
}

"""
    with open(plan_output_path, "w") as terraform_plan:
        # Write Terraform header
        terraform_plan.write(config_text)

        # Write resource blocks for each detected component
        for component in detected_components_to_docker_images:
            type = component["type"]
            docker_image = component["image"]
            name = component["name"]


            # Write Terraform resource block for pulling Image
            terraform_plan.write(f'resource "docker_image" "{name}" {{\n')
            terraform_plan.write(f'  name = "{docker_image}"\n')
            terraform_plan.write("}\n\n")
            # Write Terraform resource block for creating Container
            terraform_plan.write(f'resource "docker_container" "{type}" {{\n')
            terraform_plan.write(f'  image = docker_image.{name}.image_id\n')
            terraform_plan.write(f'  name = "{type}"\n')
            terraform_plan.write(f'  command = ["yes"]\n')
            # terraform_plan.write(f'  memory = "{memory}"\n')
            terraform_plan.write("}\n\n")
generate_terraform_plan(result)


