# Projeto_F1
F1 Telemetry Data Analysis & Virtual Race Engineer
---
## Overview
This project focuses on capturing, decoding, and analyzing telemetry data from the game F1 25 in order to build a data-driven environment for performance analysis.
The goal is to transform raw telemetry packets transmitted by the game into structured datasets that can later be used for:
- Performance analysis
- Visualization and telemetry dashboards
- Statistical race insights
- Development of a Virtual Race Engineer
- Machine learning models capable of predicting lap and performance
- The long-term objective is to create a system capable of analyzing driver performance and providing intelligent feedback “similar” to what real race engineers do.

## Project Goals
The main goals of this project are:
- Capture real-time telemetry data from F1 25
- Decode binary UDP packets into readable data
- Store structured telemetry datasets
- Build performance analysis tools
- Create visualizations for driver improvement
- Develop a virtual race engineer assistant
- Train machine learning models for lap prediction and performance insights

Initially the system is being developed using a specific track and session, but the architecture is designed to later support:
- Any track
- Any driver 
- Any session type


## Data Source
Telemetry data is obtained directly from the game using the official UDP Telemetry System provided by EA Sports / Codemasters.
The decoding of packets follows the official documentation:
- EA Sports F1 UDP Telemetry Specification for Developers

This document describes the structure of each telemetry packet and allows proper decoding of the binary data transmitted by the game.
Packets are transmitted in binary format and must be interpreted according to their structure.


## System Architecture
The project pipeline currently follows these steps:
## Telemetry Capture
The game sends telemetry packets through UDP.
A Python socket listener captures these packets in real time.
- _captura_dados_f1.py_


## Raw Packet Storage
Captured packets are stored in CSV format containing:
- Timestamp
- Packet size
- Raw hexadecimal data
- The packets are originally received as binary bytes by the socket listener.

For storage purposes, they are converted to hexadecimal strings before being written to CSV files.
Storing the raw packets allows the data to be preserved for future decoding, experimentation, and improvements to the parsing logic.


## Binary Decoding
- During the decoding stage, the hexadecimal representation is converted back into raw bytes using:
binascii.unhexlify()
- Once converted back to bytes, the packet structure can be decoded using Python's:
struct
- This allows the extraction of telemetry values defined in the official EA documentation.
- Examples of decoded information include:
Speed
RPM
Throttle / Brake
Gear
Tire temperatures
Fuel levels
Lap times
G-forces
Suspension data

## Data Processing
Once decoded, the telemetry data can be processed using tools such as:
- Pandas
- NumPy

This allows filtering, cleaning, and preparing the dataset for further analysis.


## Data Analysis and Visualization
With structured telemetry data it becomes possible to build:
- Performance comparisons
- Lap analysis
- Driver consistency metrics
- Track segment performance

Visualization tools may include:
- Matplotlib
- Plotly
- Seaborn

## Machine Learning
Future stages of the project aim to incorporate machine learning techniques to:
- Predict lap times
- Identify optimal driving patterns
- Detect performance losses
- Compare drivers or sessions

Possible models include:
- Regression models
- Time-series analysis
- Neural networks for telemetry patterns


## Virtual Race Engineer
Based on the telemetry analysis and machine learning models, a future goal of the project is to build a Virtual Race Engineer assistant capable of:
- Analyzing driving performance
- Providing performance suggestions
- Identifying braking or throttle inefficiencies


## Current Data Captured
The system currently captures multiple telemetry packet types including:
Packet ID
| Packet Name
Description
| 0
Motion
Car physics data (G-forces, suspension, orientation)
| 2
Lap Data
Lap times and track progress
| 6
Car Telemetry
Speed, throttle, brake, RPM and temperatures
| 7
Car Status
Fuel levels, tire compounds, damage
| 11
Session History
Historical lap data

Each packet is stored in a dedicated dataset for later decoding.


## Technologies Used
- Python
- UDP Networking (socket)
- Binary decoding (struct)
- Data storage (CSV)
- Data processing (pandas, numpy)

Additional technologies such as data visualization, advanced analysis tools, and machine learning models are planned for future stages of the project as the dataset and telemetry pipeline evolve.


## Future Work
- Planned improvements include:
- Full packet decoding according to the official specification
- Track map reconstruction from telemetry
- Sector performance analysis
- Data visualization
- Tire degradation models and other analysis as throttle
- Machine learning models for lap time prediction and performance analysis
- A functional similar Virtual Race Engineer assistant


## Inspiration 
My inspiration for this project comes from a lifelong passion for motorsport, especially Formula 1, that started in my childhood. Since I was very young, I’ve been fascinated by racing, the incredible speed of the cars, the sound of the engines, and the beauty of their aerodynamic design.There is something special about watching drivers and cars pushed to the absolute limit of performance.

Over the years, I’ve spent a lot of time watching races, including Formula 1, WEC, and other motorsport categories. I also enjoy watching classic and historic races, which helps me appreciate how the sport has evolved.

Beyond watching races, I also enjoy driving in virtual racing simulators, where I try to improve my own performance and understand the dynamics of driving at the limit. This personal experience made me realize how important data and telemetry are in motorsport. In professional racing, engineers rely heavily on data to analyze driver performance, improve car setup, optimize strategies, and support the entire team during race weekends.

Because of this, I wanted to build a project that combines two things I truly enjoy: motorsport and data analysis. 

The goal is to explore how telemetry data can be captured, processed, and analyzed to better understand performance and eventually create tools similar to those used by real race engineers.


# Status:
## Project currently in data acquisition and decoding stage.

