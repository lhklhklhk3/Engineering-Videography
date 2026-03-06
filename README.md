Engineering-Videography
<div align="center"><img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version"><img src="https://img.shields.io/badge/FFmpeg-5.0+-green.svg" alt="FFmpeg Version"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License"></div>
A full-process solution for engineering scene videography, focusing on hardware selection, shooting specifications, and automated video processing. Lightweight adaptation to core scenarios such as engineering construction recording, equipment inspection, and achievement display.
Project Overview
A collection of videography tools and guidelines for the engineering field. Through concise configurations and automated scripts, it lowers the technical threshold for engineering video collection, processing, and management, and is adaptable to various engineering scenarios such as construction, bridges, and roads.
Quick Start
Environment Dependencies
Python 3.8+
FFmpeg 5.0+ (core dependency for video processing)
Optional: OpenCV (frame analysis/annotation)
One-Click Deployment
# Install dependencies
pip install -r requirements.txt

# Launch the main program
python main.py
Module	Core Capabilities
Configuration Management (config_manager)	Visually configure shooting parameters and video processing rules to adapt to different engineering scenarios
Automated Video Processing	Batch compression / frame extraction / metadata addition, balancing the volume and quality of engineering archive videos
Scene-Based Shooting Guidelines	Standardized shooting templates for construction recording / equipment inspection / achievement display
Directory Structure
Engineering-Videography/
├── main.py            # Program entry point
├── config_manager.py  # Core logic for configuration management
├── settings_dialog.py # Visual configuration interface
├── requirements.txt   # Dependency list
└── app.ico            # Program icon
