
# Read data from API

A program that get data from an https://openweathermap.org API and send it to ThingBoard



## Before using the program

<<<<<<< HEAD
- To get your api key go to https://openweathermap.org and create an acount for free
=======
- To get your api key go to https://openweathermap.org and create an acount for free
>>>>>>> 33c82d82d1a143e61e77e386f6987d29d0a470f3
- To get your access token, go to https://thingsboard.io and create an account for free
- in thingsboard -> Entites -> Devices section click '+' to add an new device and enter necessary informations
- after that you should copy your access token
- in your cloned repository, create a file .env
- add the following information
```
api_key=<your_API_KEY_from_openweather>
tb_token=<your_access_token>
```

## Run Locally

Clone the project

```bash
  git clone https://github.com/hepona/ReadDataFromAPI
```

Go to the project directory

```bash
  cd ReadDataFromAPI
```

Install the following libraries

```bash
  pip install requests
  pip install python-dotenv
  pip install paho-mqtt
  pip install jsonlib
```

Run the program
```bash
  ./ReadDataFromAPI.py <city>
```
or
```bash
  python3 ReadDataFromAPI.py <city>
<<<<<<< HEAD
```
=======
```

>>>>>>> 33c82d82d1a143e61e77e386f6987d29d0a470f3
