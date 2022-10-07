# WinbookBackend Open Source Project

### Technology

    - Python
    - Django
    - Django rest framework
    - Pillow

### Installation

#### Clone the repository

#### Create a virtual environment(optional)

    - Install the Virtual Environment
        `
        python3 -m venv venv
        source venv/bin/activate

        `
    - Run the installation commands below
    - To leave the virtual environment
        `
        deactivate
        `

#### Install the requirements

        `
        pip install -r requirements.txt
        `

#### Setup environment variables

        - Create a .env file in the root directory
        - Add the following variables
            `
            EMAIL_HOST_USER=your_email
            EMAIL_HOST_PASSWORD=your_password
            SITE_URL=http://<your site url>
            `

#### Run the server

            `
            python manage.py runserver
            `
