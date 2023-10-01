# WinbookBackend Open Source Project
[![.github/workflows/main.yml](https://github.com/team-d3m0n1k/winbookBackend/actions/workflows/main.yml/badge.svg?branch=master)](https://github.com/team-d3m0n1k/winbookBackend/actions/workflows/main.yml)

This is a small social media type project that was developed using the technologies below, and it includes the following sections:

1. Basic login
2. Posts
3. Comments
   and more...


### Technology

    - Python
    - Django
    - Django rest framework
    - Pillow

### Installation

1.  #### Clone the repository

2.  #### Create a virtual environment(optional)

        - Install the Virtual Environment
            ```python
            python3 -m venv venv
            source venv/bin/activate
            ```

        - Run the installation commands below

        - To leave the virtual environment
            ```shell
             deactivate
            ```

3.  #### Install the requirements

            `
            pip install -r requirements.txt
            `

4.  #### Setup environment variables

        - Create a .env file in the root directory
        - Add the following variables
            `
            EMAIL_HOST_USER=your_email
            EMAIL_HOST_PASSWORD=your_password
            SITE_URL=http://<your site url>
            `

5.  #### Run the server

            `
            python manage.py runserver
            `
