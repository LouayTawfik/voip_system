# VOIP Call System

A Python-based voice call streaming application that enables two-way communication using Twilio. This project allows you to initiate phone calls and record messages through a simple command-line interface.

## Features

- Make outbound calls to any phone number
- Play custom messages to call recipients
- Record responses from recipients
- Store call details and recordings in a Django database
- Simple command-line interface

## Technologies Used

- Python 3.10+
- Django 4.2+
- Twilio API for voice calls


## Prerequisites

- Python 3.10+
- Twilio account with:
  - Account SID
  - Auth Token
  - Twilio phone number
 
## Installation

### Option 1: Local Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/LouayTawfik/voip_system.git
   cd voip_system

2. Create and activate a virtual environment:
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:
  pip install -r requirements.txt

4. Configure environment variables:
   export TWILIO_ACCOUNT_SID="your_account_sid"
   export TWILIO_AUTH_TOKEN="your_auth_token"
   export TWILIO_PHONE_NUMBER="your_twilio_number"

5. Apply database migrations:
   python3 manage.py migrate


## Usage
## Making Call
Use the voice_call_app.py script to initiate a call:
# Basic usage with just a phone number
python call_handler.py +15551234567

# Providing a custom message
python call_handler.py -n +15551234567 -m "Hello, this is a test message."


## Command-line Arguments
* -n, --number: Phone number to call (with country code)
* -m, --message: Custom message to play during the call
   
