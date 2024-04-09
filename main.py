import os
import sys
import base64
import glob
import requests
import openai
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

# Initialize logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# TODO: Enhance error handling and add retry logic for network requests.
def generate_response(prompt: str) -> str:
    """Generate a response from OpenAI based on the given prompt."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are an AI that generates content."},
                      {"role": "user", "content": prompt}],
            max_tokens=500,
            n=1,
            temperature=0.8,
        )
        message = response.choices[0].message['content'].strip()
        logging.info(f"Generated response for prompt '{prompt}' successfully.")
        return message
    except Exception as e:
        logging.error(f"Error generating response: {e}")
        return None

def generate_blog_content(title: str) -> str:
    """Generate blog content based on a given title."""
    return generate_response(f"Write a blog post about {title}.")

def upload_image_to_wordpress(image_path: str) -> int:
    """Upload an image to WordPress and return its ID."""
    with open(image_path, 'rb') as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')

    headers = {
        "Authorization": f"Bearer {os.environ['JWT_TOKEN']}",
        'Content-Type': 'image/jpeg',
        'Content-Disposition': f'attachment; filename="{os.path.basename(image_path)}"'
    }

    response = requests.post(f"http://{os.environ['WP_HOST']}/wp-json/wp/v2/media", headers=headers, data=image_data)
    if response.status_code == 201:
        logging.info(f"Image '{image_path}' uploaded successfully to WordPress.")
        return response.json()['id']
    else:
        logging.error(f"Error uploading image: {response.text}")
        return None

def create_wordpress_post(title: str, content: str, upload_id: int) -> None:
    """Create a new post on WordPress with the given title, content, and image."""
    post_data = {
        "title": title,
        "content": content,
        "status": "publish",
        'featured_media': upload_id,
    }
    headers = {
        "Authorization": f"Bearer {os.environ['JWT_TOKEN']}",
        "Content-Type": "application/json"
    }
    response = requests.post(f"http://{os.environ['WP_HOST']}/wp-json/wp/v2/posts", headers=headers, json=post_data)
    if response.status_code == 201:
        logging.info(f"Blog post '{title}' created successfully on WordPress.")
    else:
        logging.error(f"Error creating post: {response.text}")

def get_environment_variables() -> dict:
    """Get necessary environment variables from the user."""
    env_vars = {}
    for var in ['TITLE', 'DL_PATH', 'JWT_TOKEN', 'WP_HOST', 'TOKEN_URL', 'WP_USER', 'WP_PASS', 'CD_PATH', 'IMG']:
        env_vars[var] = input(f"Please enter the value for {var}: ")
    logging.info("Environment variables set successfully.")
    return env_vars

def download_image_from_unsplash(search_term: str, download_path: str) -> str:
    """Download an image from Unsplash based on a search term and return its path."""
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--ignore-certificate-errors")

    with webdriver.Chrome(service=webdriver.chrome.service.Service(os.environ['CD_PATH']), options=options) as driver:
        driver.get('https://unsplash.com')
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@title="Search Unsplash"]')))
        search_box.send_keys(search_term + Keys.ENTER)

        download_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[@title="Download photo"]')))
        download_button.click()

        WebDriverWait(driver, 10).until(lambda d: len(glob.glob(f"{download_path}*.jpg")) > 0)

    image_path = max(glob.glob(f"{download_path}*"), key=os.path.getctime)
    logging.info(f"Image from Unsplash downloaded successfully to {image_path}.")
    return image_path

def main():
    """Main function to get environment variables, generate content, download an image, upload the image, and create
    a post."""
    env_vars = get_environment_variables()
    title = env_vars['TITLE']
    dl_path = env_vars['DL_PATH']

    content = generate_blog_content(title)
    if not content:
        logging.error("Error generating content.")
        sys.exit(1)

    image_path = download_image_from_unsplash(env_vars['IMG'], dl_path)
    upload_id = upload_image_to_wordpress(image_path)
    if not upload_id:
        logging.error("Error uploading image.")
        sys.exit(1)

    create_wordpress_post(title, content, upload_id)

# Execute the main function if the script is run directly
if __name__ == '__main__':
    main()
