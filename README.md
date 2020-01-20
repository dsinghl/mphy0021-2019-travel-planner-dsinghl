# Travelplanner
##### (v0.1.0) Initial development release
A python module to generate timetables, calculate routes, and much more.

## Installation and Usage
----------

### Installation

Travelplanner can be installed by downloading the source directory and running `pip install .` in the root directory.

### Usage

The installation should allow you to begin using travelplanner right away provided you have a bus route and a passengers file.

```
bussimula {route_file} {passengers_file}
```

The route file and passenger files must be `.csv` files.

They should look as follows:

##### Route file
This would be saved as something like `route.csv`
```
1,1,A
1,2,
1,3,
2,3,
2,4,B
...
...
...
```

##### Passengers file
This would be saved as something like `passengers.csv`
```
1,1,2,2,25
0,0,3,4,15
2,2,2,6,25
...
...
...
```

We can then call the travelplanner as follows:
```
bussimula route.csv passengers.csv
```

### Command line options

bussimula has only a few options. You can see them by tunning `bussimula --help`.

```
usage: bussimula [-h] [--speed SPEED] [--saveplots] route_file passenger_file

Travelplanner command line inferface. Used to calculate journeys for
passengers on a bus route.

positional arguments:
  route_file      Route csv file name, for example "route.csv".Use path if
                  file not in current dirrectory.
  passenger_file  Passengers csv file name, for example "passengers.csv". Use
                  path if file not in current dirrectory.

optional arguments:
  -h, --help      show this help message and exit
  --speed SPEED   Accepts number indicating minutes per step.
  --saveplots     (OPTIONAL) Saves two plots of bus load and route in current
                  directory.
```

Using the `--saveplots` options saves two plots that look like the below in current directory.

Bus map - `map.png`           | Bus load - `load.png`
------------------------------|------------------------------
![Bus Map](./images/ex_map.png)| ![Bus Load](images/ex_load.png)


### Roadmap

In the future many features are planned.

* Currently, the package does not consider start time of bus route and passenger journey. Adding this feature will give the possibility to check whether a passenger will be quick enough to get to the required bus stop in time.
* Another bus route could be added so the passenger has an option of which bus to take.

### Contributing

Please see the [contributing documentation](CONTRIBUTING.md).


### Authors and acknowledgement

Thank you to Dr David Pérez-Suárez, Dr Anastasis Georgoulas, and the rest of the MPHY0021 team who provided the base for this package. Thank you for being great teachers and making the project author enjoy the lectures, the author thinks that it was the best coding lecture course he has attended.

### License

See [License](LICENSE.md) file.

### Project status

Currently the development of this project is on hold. 