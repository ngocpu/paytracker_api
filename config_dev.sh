@echo off
echo Running DEVELOPMENT environment
export DOTENV_FILE=.env.development
set DOTENV_FILE=.env.development
uvicorn src.main:app --reload


