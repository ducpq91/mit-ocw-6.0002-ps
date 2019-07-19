# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: 
# Collaborators (discussion):
# Time:

import pylab
import re

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    models = []
    for deg in degs:
        model = pylab.polyfit(x, y, deg)
        models.append(model)
    print(models)
    return models

def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    assert isinstance(y, pylab.ndarray)
    assert isinstance(estimated, pylab.ndarray)
    assert len(y) == len(estimated)

    mean_y = y.mean()
    res_ss = ((y - estimated) ** 2).sum()
    tot_ss = ((y - mean_y) ** 2).sum()
    r2 = 1 - (res_ss / tot_ss)

    return r2

def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """

    for m in models:
        # below code in comment only works for degree <= 2; does not work for degree > 2, not sure why...
        # order = 0
        # estimate = 0
        # while len(m) > order:
        #     estimate += m[len(m) - 1 - order] * (x ** order)
        #     order += 1
        #     print(estimate)
        estimate = pylab.polyval(m, x)
        r2 = r_squared(y, estimate)

        pylab.plot(x, y, "bo", x, estimate, '-r')
        pylab.xlabel("Year")
        pylab.ylabel("Degree Celsius")
        if len(m) == 2:
            pylab.title("R-square = {}, Degree = {}, \nSE-over-slope = {}".format(round(r2, 3), len(m) - 1,
                                                                               se_over_slope(x, y, estimate, m)))
        else:
            pylab.title("R-square = {}, Degree = {}".format(round(r2, 3), len(m) - 1))
        pylab.show()

def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    year_avg = []
    for year in years:
        city_avg = []
        for city in multi_cities:
            avg = climate.get_yearly_temp(city, year).mean()
            city_avg.append(avg)
        year_avg.append(pylab.mean(city_avg))
    return pylab.array(year_avg)

def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    moving_avg = []
    for i in range(len(y)):
        start = i - window_length + 1
        if start >= 0:
            mov_avg = pylab.mean(y[start:(i+1)])
        else:
            mov_avg = pylab.mean(y[0:(i+1)])
        moving_avg.append(mov_avg)

    return pylab.array(moving_avg)

def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    assert len(y) == len(estimated)

    value = pylab.sqrt(((y - estimated) ** 2).mean())
    return value

def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    yearly_std = []

    for year in years:
        city_temp = 0
        for city in multi_cities:
            city_temp += climate.get_yearly_temp(city, year)
        daily_avg = city_temp / len(multi_cities)
        year_std = pylab.std(daily_avg)
        yearly_std.append(year_std)

    return pylab.array(yearly_std)

def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """

    for m in models:
        # below code in comment only works for degree <= 2; does not work for degree > 2, not sure why...
        # order = 0
        # estimate = 0
        # while len(m) > order:
        #     estimate += m[len(m) - 1 - order] * (x ** order)
        #     order += 1
        #     print(estimate)
        estimate = pylab.polyval(m, x)
        rmse_val = rmse(y, estimate)

        pylab.plot(x, y, "bo", x, estimate, '-r')
        pylab.xlabel("Year")
        pylab.ylabel("Degree Celsius")
        pylab.title("RMSE = {}, Degree = {}".format(round(rmse_val, 3), len(m) - 1))
        pylab.show()

if __name__ == '__main__':

    # pass

    # Part A.4
    all_data = Climate("data.csv")

    # data_day = []
    # for year in TRAINING_INTERVAL:
    #     data_day.append(all_data.get_daily_temp("NEW YORK", 1, 10, year))
    # data_day_arr = pylab.array(data_day)
    # model = generate_models(TRAINING_INTERVAL, data_day_arr, [1])
    # evaluate_models_on_training(pylab.array(TRAINING_INTERVAL), data_day_arr, model)

    # Part B

    # data_year = []
    # for year in TRAINING_INTERVAL:
    #     data_year.append(all_data.get_yearly_temp("NEW YORK", year).mean())
    # data_year_arr = pylab.array(data_year)
    # model1 = generate_models(TRAINING_INTERVAL, data_year_arr, [1])
    # evaluate_models_on_training(pylab.array(TRAINING_INTERVAL), data_year_arr, model1)

    # data_cities_yearly = gen_cities_avg(all_data, CITIES, list(TRAINING_INTERVAL))
    # model2 = generate_models(TRAINING_INTERVAL, data_cities_yearly, [1])
    # evaluate_models_on_training(pylab.array(TRAINING_INTERVAL), data_cities_yearly, model2)
    # Part C
    # mov_avg_natl = moving_average(data_cities_yearly, 5)
    # model3 = generate_models(TRAINING_INTERVAL, mov_avg_natl, [1])
    # evaluate_models_on_training(pylab.array(TRAINING_INTERVAL), mov_avg_natl, model3)

    # Part D.2
    # model4 = generate_models(TRAINING_INTERVAL, mov_avg_natl, [1,2,20])
    # evaluate_models_on_training(pylab.array(TRAINING_INTERVAL), mov_avg_natl, model4)
    #
    # data_cities_yearly_1015 = gen_cities_avg(all_data, CITIES, list(TESTING_INTERVAL))
    # mov_avg_natl_1015 = moving_average(data_cities_yearly_1015, 5)
    # evaluate_models_on_testing(pylab.array(TESTING_INTERVAL), mov_avg_natl_1015, model4)

    # Part E
    std_dev_6109 = gen_std_devs(all_data, CITIES, TRAINING_INTERVAL)
    mov_avg_std_dev_6109 = moving_average(std_dev_6109, 5)
    model5 = generate_models(TRAINING_INTERVAL, mov_avg_std_dev_6109, [1])
    evaluate_models_on_training(pylab.array(TRAINING_INTERVAL), mov_avg_std_dev_6109, model5)
