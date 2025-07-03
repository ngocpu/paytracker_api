@echo off
echo Running STAGING environment
export DOTENV_FILE=.env.staging
set DOTENV_FILE=.env.staging
uvicorn src.main:app --reload