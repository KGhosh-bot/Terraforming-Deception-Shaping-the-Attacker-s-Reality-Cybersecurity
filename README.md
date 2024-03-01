# Terraforming-Deception:Shaping-the-Attacker's-Reality-Cybersecurity
A Fake Architecture Orchestrator to implement defensive deception in cybersecurity, strategically creating services and components to mislead attackers and divert their attention and resources away from critical assets. 

By creating fake services and components that appear as valuable targets to attackers, defenders can divert the attacker's attention and resources away from critical assets. Attackers might spend time and effort trying to compromise these fake elements, leaving less capacity to target actual valuable assets. The goal of this project is to easily instantiate a complex "fake" infrastructure from an architectural diagram.

This project develops a Fake Architecture Orchestrator using Terraform and containerized Docker environments for cyber security deception, dynamically generating infrastructure based on draw.io diagrams and custom XML parsing. This automates deployment, streamlines resource management and misleads attackers through strategic deception.

<p align="center">
    <img src="images/project Ingredients.png", style="width: 400px; height: 400px;"/></center>
</p>

## Architecture Diagram
This diagram visually represents the desired fake infrastructure with six different  components and connections. A custom XML parser extracts component information, including names, types, and any associated attributes, from the draw.io diagram. 
<p align="center">
    <img src="images/fake architecture_small.png", style="width: 600px; height: 300px;"/></center>
</p>

## Docker Image Mapping
The parsed information is used to map detected components to specific Docker images. This mapping is achieved by loading a configuration file (config.json), which associates each component type with a corresponding Docker image configuration.
<p align="center">
    <img src="images/image mappings.png", style="width: 400px; height: 400px;"/></center>
</p>

## Terraform Plan Generation
The extracted component information and Docker image mappings are used to automatically generate Terraform resource configurations (main.tf) that includes resource blocks for each detected component. The configuration specifies the necessary attributes and configurations, utilizing Terraform's declarative language HashiCorp Configuration Language (HCL). 
<p align="center">
    <img src="images/terraform plan generation.png", style="width: 400px; height: 400px;"/></center>
</p>




