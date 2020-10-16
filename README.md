
<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Installation](#installation)
* [Usage](#usage)
* [Contributing](#contributing)
* [License](#license)


<!-- ABOUT THE PROJECT -->
## About The Project
This application permits automatic processing of Raster and shapefiles, in order to get relevant statistics related to the raster data (i.e: mean, min, max, std).
This application focuses on pollution/Covid related data processing and vizualisation.
It is composed of two parts:
* Data processing : handled by "dataprocessing.py". This scripts generates excel files containing statistics value based on the raster and shapefile put in the "Rawdata" repository.
* Data vizualisation : Handled by "App.py". This is the main script, it reads the excel files and generate vizualisation components.

### Built With
This project is built using :
* [Python]
* [Dash]
* [Plotly]
<!-- GETTING STARTED -->
## Getting Started
In order to install the repo locally you should follow these instrucitons

### Installation

1. Clone the repo
```sh
git clone https://github.com/ziedsaidd/LISER-Internship-Dashboard-App
```
2. Install all required libraries from the requirements file
```sh
pip install -r requirements.txt
```
3. Launch the app by executing
````sh
python app.py
````
4. To processes new data, it should be added in the appropriate directory in "rawdata" and then execute 
````sh
python dataProcessing.py
````

<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License
This project is still not liscenced 

<!-- CONTACT -->

