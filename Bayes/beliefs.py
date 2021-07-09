#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import utils


class Belief(object):
    """
    Belief class used to track the belief distribution based on the sensing
    evidence we have so far.
    Arguments:
        size (int): the number of rows/columns in the grid

    Attributes:
        open (set of tuples):  set containing all the positions that have not
            been observed so far.
        current_distribution (dictionary): probability distribution based on
            the evidence acquired so far.
            The keys of the dictionary are the possible grid positions
            The values represent the (conditional) probability that the
            treasure is found at that position given the evidence (sensor data)
            accumulated so far.
    """
    def __init__(self, size):
        # Initially all positions are open - have not been observed
        self.open = {(x, y) for x in range(size)
                     for y in range(size)}
        # Initialize to a uniform distribution
        self.current_distribution = {pos: 1 / (size ** 2) for pos in self.open}

    def get_beliefs(self):
        """
        Accessor method for the belief distribution
        Note: to be used in treasurehunt.py only for a cleaner interface
        You do not need to use it inside the Belief class.
        :return:
          dictionary representing the belief distribution given the evidence
          accumulated so far.
        """
        return self.current_distribution


    def update(self, color, sensor_position, model):
        """
        Update the belief distribution based on new evidence:  our agent
        detected the given color at sensor location: sensor_position.
        :param color: (string) color detected
        :param sensor_position: (tuple) position of the sensor
        :param model (Model object) models the relationship between the
             treasure location and the sensor data
        :return: None
        """

        for position in self.current_distribution:
            self.current_distribution[position] *= model.pcolorgivendist(color, utils.manhattan_distance(position, sensor_position))

            # normalize: we must divide by the sum of all possible values
        for position in self.current_distribution:
            self.current_distribution[position] = self.current_distribution[position] / sum(self.current_distribution.values())

            # remove sensor_position from the open set using .remove
        self.open.remove(sensor_position)


        

    def recommend_sensing(self):
        """
        Recommend where we should take the next measurement in the grid.
        The position should be the most promising unobserved location.
        If all remaining unobserved locations have a probability of 0, return
        the unobserved location that is closest to the (observed) location with
        the highest probability.

        :return: tuple representing the position where we should take the
           next measurement
        """

        open_prob = {p: self.current_distribution[p] for p in self.open}

        # Get the open position with the best probability
        best = max(open_prob, key=lambda p: open_prob[p])

        # check if all open probabilities are 0
        if self.current_distribution[best] == 0:
            observed_max = max(self.current_distribution.keys(), key=lambda p: self.current_distribution[p])
            second_best = utils.closest_point(observed_max, self.open)
            return second_best
        return best