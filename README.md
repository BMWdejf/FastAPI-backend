# FastAPI 

### Description
REST API for processing data from external chanels 

## Get code
For get this code from repository to your local pc you can use this steps: 

Fork this repository to your Github account or clone this repository to local PC.
```bash
git clone https://github.com/BMWdejf/FastAPI-backend.git
```
Open folder with code in IDE (PyCharm or VSC)

Open terminal window and run this commands:
```bash
python -m venv venv
```
or 
```bash
python3 -m venv venv
```
### Activate Venv

for user which you have MacOs or Linux next step is
```bash
source venv/bin/activate
```
for user which you have Windows 
```bash
.\venv\Scripts\activate
```
You must see "(venv)" in leftside your terminal

## Install packages from requirements
For next step it is important install packages from requirements.txt
```bash
pip install -r requirements.txt
```
after finishing will be testing runing code on localhost server

```bash
hypercorn app.core.main:app --reload
```
if all work correctly open link in your browser

[127.0.0.1:8000](http://127.0.0.1:8000/)

you must get 

```json
{"message":"Hello from FastAPI!"}
```
## Deploy on Railway
if the first tine deploying on Railway.app you need install Railway CLI to your PC.

For more informations following this link [Installing the Railway CLI](https://docs.railway.app/guides/cli)

### Homebrew (macOS)
In a Terminal, enter the following command:
```bash
brew install railway
```
or npm for Windows
```bash
npm i -g @railway/cli
```
if you want to know what commands you can use, enter the following commnad in terminal
```bash
railway --help
```
the first step is to log in to your Railway account
```bash
railway login
```
follow the instructions until successful login.

now you must create a new project 
```bash
railway init -n <your-project-name>
```
now is last step for deploying your first app to Railway.app
```bash
railway up
```
in terminal you must see:
```log
[2024-05-17 18:12:48 +0000] [12] [INFO] Running on http://[::]:7186 (CTRL + C to quit)
```
Now is really the last step. You must generate your public URL address in your app.
Click on your app in Railway dashboard, go to section "Settings" now find section "Networking" and click on the button "Generate domain".
After few times you open the generated link in your browser.