# ICT3102 Team 1

## Quick Start
- Clone this repo
`git clone https://github.com/lemonjin1997/ICT3102_TEAM1/`

- Change folder
`cd ICT3102_TEAM1/`

- Install pipenv
`python -m pip install pipenv`

- Install required dependencies
`pipenv install`

- Activate virtual environment
`pipenv shell`

- Start the Flask server
`python application.py`

Go to `http://127.0.0.1:5000/` to view the web application

## CI/CD Pipeline

A CI/CD pipeline has been setup with Github Actions to deploy the web application to AWS Elastic Beanstalk. 

See `main.yml` for more information on the CI/CD workflow.

Visit `http://ict3102flaskapplication-env.eba-fzac9weh.ap-southeast-1.elasticbeanstalk.com/` to view the deployed web application

