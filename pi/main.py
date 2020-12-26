from typing import List
import random
import math
import statistics


class CircleSimulator:

    SIZE = 1

    def simulate(self):
        point = self.generate_point()
        return self.is_point_area(point)

    def generate_point(self):
        return self._generate_random(), self._generate_random()

    def is_point_area(self, point):
        x, y = point
        hypotenuse = math.sqrt(x**2 + y**2)
        return hypotenuse <= self.SIZE

    def _generate_random(self):
        sign = random.choice([-1, 1])
        axis_location = random.random() * self.SIZE
        return axis_location * sign


class SamplerStats:

    def __init__(self, points_inside, size):
        self.points_inside = points_inside
        self.size = size
    
    @property
    def pi(self):
        return 4 * self.points_inside / self.size


class CircleSampler:
    
    def __init__(self, simulator: CircleSimulator):
        self.simulator = simulator

    def sample(self, quantity: int) -> SamplerStats:
        sample = self.generate_sample(quantity)
        return self.evaluate_sample(sample)

    def evaluate_sample(self, sample: List[bool]) -> SamplerStats:
        return SamplerStats(
            points_inside=sample.count(True),
            size=len(sample)
        )

    def generate_sample(self, quantity: int) -> List[bool]:
        simulations = [self.simulator.simulate() for _ in range(quantity)]
        return simulations


class PiRandomEstimator:

    STANDARD_DEVIATION_QUANTITY = 1.96

    def __init__(self, sampler: CircleSampler):
        self.sampler = sampler
        self._pi_samples = []

    def estimate_pi(self, accuracy):
        expected_sigma = accuracy / self.STANDARD_DEVIATION_QUANTITY
        sample_size = 1000
        points_quantity = 5000
        while self.size == 0 or self.sigma >= expected_sigma:
            self.__generate_pi_sample(sample_size, points_quantity)
            points_quantity *= 2
            message = f"PI: {self.mean} +- {self.sigma} at {self.size}"
            print(message)

    @property
    def sigma(self):
        return statistics.stdev(self._pi_samples)

    @property
    def mean(self):
        return statistics.mean(self._pi_samples)

    @property
    def size(self):
        return len(self._pi_samples)

    def __generate_pi_sample(self, sample_quantity, points_quantity):
        for _ in range(sample_quantity):
            stats = self.sampler.sample(points_quantity)
            self._pi_samples.append(stats.pi)


if __name__ == "__main__":
    simulator = CircleSimulator()
    sampler = CircleSampler(simulator)
    estimator = PiRandomEstimator(sampler)
    estimator.estimate_pi(accuracy=0.01)
