# SDF Static Model Exporter

[![Blender](https://img.shields.io/badge/Blender-%23F5792A.svg?logo=blender&logoColor=white)](https://www.blender.org/)
[![Gazebo](https://img.shields.io/badge/Gazebo-Harmonic%2B-blue)](https://gazebosim.org)


Bridge between Blender's modeling capabilities and Gazebo's physics simulation. Export static 3D models from Blender directly to SDF format for use in Gazebo simulations.

SDF(SDFormat) is the official model specification format for [Gazebo](https://gazebosim.org). While Gazebo excels in physics-based simulation, its native modeling capabilities are limited.

[Blender](https://www.blender.org/) is an easy-to-use, powful, free and open source 3D creation suite. It supports the entirety of the 3D pipeline—modeling, rigging, animation, simulation, rendering, compositing and motion tracking, even video editing and game asset creation. In other words, blender can make beatuful 3D model.

So, it is possible to make/write an extention to extend blender to export model to SDF, that making Gazebo models easliy.

SDF Static Model Exporter, an extention of blender, can export a 3D model built by blender to SDF model. After export, the exported model can be added Gazebo to enrich your simulation environment. 

SDF Static Model Exporter bridges both platforms by enabling ‌direct export of 3D models to SDF format‌. Generated models can be seamlessly integrated into Gazebo simulations.

Have fun with Blender & Gazebo!

## Features
-  🚀 Single-click export of Blender models to SDF
-  🧱 Automatic mesh optimization for physics simulation
-  📦 Preserves object hierarchy and transformations
-  💡 Lightweight implementation (~50KB)

## Install

### 1. prerequisite

1. Blender 5.0.0 or newer
2. Gazebo Harmonic or newer

### 2. Download this repository as a .zip file.

Download the extention at release part. download the file : gazebo_sdf_static_model_exporter-1.0.0.zip


### 3. Install the zip file as local extention
In Blender:
Navigate to Edit-> Preferences -> Add-ons

Click ‌Install...‌ (top-right) and select the .zip file
Enable the add-on by checking its box.

then, boom, you have successfully✅ ‌ install the SDF static Model Exporter.

## How to use

It is recommanded to look a 10 minutes usage tutorial video to learn.

Bilibili is my favorite platform, a 10-minute tutorial is available on ‌Bilibili‌ ([Bilibili](https://www.bilibili.com/video/BV1DJf2BwESM/)).

📌 My channel covers Gazebo, ROS 2, and simulation tools – subscriptions welcome!

## Roadmap‌

Future updates may include:

* Texture support
* Custom material/color export
* Enhanced collision mesh handling

⚠️ Complex SDF features (e.g., joints, dynamics) require manual post-processing.

## Contribution‌

Bug reports and feature requests: ‌GitHub Issues‌
Support the project: ‌⭐ Star‌ or ‌Donate‌

## Notes‌

An add-on for exporting ‌dynamic robots‌ (SDF) is in development.
