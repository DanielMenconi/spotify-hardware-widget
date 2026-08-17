# Spotify Hardware Widget

<img width="350" src="https://github.com/DanielMenconi/spotify-hardware-widget/blob/f07f00a1a9bb68b33bbe55be0d157af6b7ea7b14/assets/oled_demo.jpg" alt="Spotify OLED Widget">

A physical Spotify widget built with Python, AWS and Arduino.

The system monitors the currently playing Spotify track, stores listening history in AWS MySQL RDS and displays live listening statistics on an OLED display connected to an Arduino UNO.

---

## Architecture

```text
Spotify API
      ↓
Python Application
      ↓
AWS API Gateway
      ↓
AWS Lambda
      ↓
AWS RDS MySQL
      ↓
Statistics returned to Python
      ↓
Arduino UNO
      ↓
OLED Display
```

---

## Features

- Reads the currently playing Spotify track
- Prevents duplicate track registrations using Spotify track IDs
- Stores listening history in AWS MySQL RDS
- Calculates artist listening statistics for the last 30 days
- Displays live song information on an OLED display
- Uses a serverless AWS backend
- Communicates with Arduino through USB serial communication

---

## Technologies

### Cloud

- AWS Lambda
- AWS API Gateway
- AWS RDS MySQL
- AWS IAM
- Amazon VPC
- Security Groups

### Backend

- Python
- Requests
- PyMySQL

### Spotify Integration

- Spotify Web API
- Spotipy

### Hardware

- Arduino UNO
- SSD1306 OLED Display
- USB Serial Communication

---

## Example Output

```text
Now Playing

Lamette (feat. Salmo)
Rose Villain

Plays (30d): 3
```

---

## Repository Structure

```text
spotify-hardware-widget/
│
├── assets/
│   └── oled_demo.jpg
│
├── arduino/
│   └── spotify_widget.ino
│
├── database/
│   └── schema.sql
│
├── spotify_auth.py
├── README.md
└── requirements.txt
```

---

## AWS Services Used

- AWS Lambda
- AWS API Gateway
- Amazon RDS MySQL
- IAM Roles and Permissions
- Amazon VPC
- Security Groups

---

## Future Improvements

- Spotify logo splash screen
- Scrolling text for long song titles
- Environment variable configuration (.env)
- Listening analytics dashboard
- Historical listening statistics
- Multi-user support

---

## Skills Demonstrated

- Python Development
- REST APIs
- AWS Cloud Services
- Serverless Computing
- SQL Databases
- Embedded Systems
- Serial Communication
- System Integration
- API Integration

---

## Author

Daniel Menconi