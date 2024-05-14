# Trello-to-Telegram Webhook 🪝


This project aims to set up webhooks for both Telegram and Trello. 
When users interact with the bot, their usernames and names will be stored in the database. 
Moreover, it enables connectivity to the Trello API, facilitating the creation of tables with necessary columns. 
Furthermore, the webhook functionality ensures that users receive notifications via the Telegram bot whenever cards are moved, 
along with details about the source and destination column.

## Stack Used

- API domain: FastAPI
- Telegram bot: aiogram
- Database connection: asyncpg
- Environment variable management: python-dotenv
- HTTP requests: requests
- Additional technologies: ngrok, Docker

## Get Started

To get started with this project, follow the next steps:

1. Clone the repository to your local machine:
```bash
git clone https://github.com/aLEKS-e3/trello-telegram-webhook.git
```

2. Set up a virtual environment and install the required dependencies using pip:
```bash
python -m venv venv
source venv/bin/activate # For linux/macos
venv\Scripts\activate # For windows
pip install -r requirements.txt
```

3. Create a .env file in the project directory based on the provided .env.sample file:
```bash
cp .env.sample .env
```

4. Edit the .env file and provide your Telegram and Trello credentials. 


You can obtain a bot token by creating a new bot using the BotFather on Telegram.
To integrate with Trello, you'll first need to obtain your application key. You can do this by logging into Trello and visiting https://trello.com/1/appKey/generate.

## Project Setup Guide

**Note: For the following steps, ensure you have Docker and ngrok installed.**

### 1. Prepare the Environment
- Pull the PostgreSQL image with Docker:
```bash
docker pull <postgres:image> 
```

- Start a proxy server on port 8000 with ngrok:
```bash
ngrok http 8000
```

### 2. Run the FastAPI Server Locally
- Launch the local FastAPI server using the following command:
```bash
fastapi dev webhook.py
```

### 3. Final Setup
- Execute the main script to complete the setup:
```bash
python main.py
```

Now, you're all set to utilize your Telegram bot in conjunction with your Trello board!
