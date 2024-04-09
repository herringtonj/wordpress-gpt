
# Wordpress GPT

**Create a WordPress blog post using the OpenAI gpt-3.5-turbo model.** Streamlined Blogging with OpenAI and WordPress. Wordpress GPT integrates OpenAI's GPT-3.5 Turbo with WordPress to auto-generate and publish blog posts. Using AI, it creates articles from your title and pairs them with images from Unsplash for a complete blogging experience.

## Prerequisites

- Python 3.x
- WordPress installation with the REST API enabled

    >[Amazon Lightsail WordPress Tutorial](https://lightsail.aws.amazon.com/ls/docs/en_us/articles/amazon-lightsail-tutorial-launching-and-configuring-wordpress)
- [Chrome](https://www.google.com/chrome/). Ensure you have it installed.
- [Chromedriver](https://chromedriver.chromium.org/downloads). Download the version compatible with your Chrome. Note: For Mac users, Chromedriver can be easily installed using `brew install chromedriver` if you have Homebrew installed.

    > Chromedriver version must be compatible with the installed version of Chrome
    
- [OpenAI API key](https://platform.openai.com/account/api-keys)

## Installation

1. **Clone** the repository:

     `git clone https://github.com/jherrin/openBlog.git`

2. **Install** the required Python packages: 

    `pip install -r requirements.txt` which contains all the necessary Python packages.

**Note for Mac users:** If you face any permission issues with Chromedriver, you might need to grant it necessary permissions. Navigate to System Preferences -> Security & Privacy and allow Chromedriver to run.

## Configuration

### Environment Configuration

For local development and to ensure the secure handling of API keys and sensitive information, this project uses a `.env` file to store environment variables. Please follow the steps below to set up your environment correctly:

1. **Create a `.env` file** in the root directory of the project.

2. **Add the necessary environment variables** to the `.env` file. Here's an example template you can start with:

```env
# OpenAI API key
OPENAI_API_KEY="your_openai_api_key_here"

# WordPress configuration
WP_HOST="your_wordpress_host_here"
JWT_TOKEN="your_jwt_token_here"

# Selenium Chrome Driver Path
CD_PATH="/path/to/your/chromedriver"

# Image download path
DL_PATH="/path/to/image/download/directory"

# Blog post title and image search term
TITLE="Your Default Blog Post Title"
IMG="Your Image Search Term"
```

Please replace the placeholder values with your actual configuration details. 

3. **Install `python-dotenv`** to automatically load the variables from your `.env` file into your Python environment. You can do this by running:

```
pip install python-dotenv
```

Or, ensure that `python-dotenv` is listed in your `requirements.txt` file and install all dependencies:

```
pip install -r requirements.txt
```

4. **Accessing Environment Variables in Python**: In your Python code, you can load and access these environment variables as follows:

```python
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables
openai_api_key = os.getenv('OPENAI_API_KEY')
```

This setup ensures that your sensitive information is kept out of version-controlled files and makes it easier to configure different environments.

## Usage/Examples

To create a new blog post, simply run:

```python
python openBlog.py
``` 

The script will prompt you for any missing configuration values.
