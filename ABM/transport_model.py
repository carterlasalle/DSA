import mesa
import numpy as np
from collections import deque

class CommuterAgent(mesa.Agent):
    """Optimized CommuterAgent class."""
    
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        # Location attributes
        self.home_location = (0, 0)  # Will be randomly assigned
        self.work_location = (0, 0)  # Will be randomly assigned
        self.current_location = self.home_location
        
        # Agent preferences (initialized with some randomness but more realistic distributions)
        self.environmental_preference = np.random.beta(2, 5)  # Most people moderately care
        self.comfort_preference = np.random.beta(3, 2)  # Most people prefer comfort
        self.cost_sensitivity = np.random.beta(2, 2)  # Varied cost sensitivity
        self.time_sensitivity = np.random.beta(3, 2)  # Most people care about time
        
        # Physical constraints
        self.max_walk_distance = 2.0  # km
        self.max_bike_distance = 8.0  # km
        
        # Current state
        self.transport_mode = None
        self.commute_distance = 0
        self.commute_time = 0
        self.commute_cost = 0
        self.satisfaction = 0
        self.trips_made = 0
        
        # Use smaller data structures for memory efficiency
        self.mode_experiences = {
            mode: deque(maxlen=20) for mode in ['car', 'public_transit', 'bike', 'walk']
        }

    def get_experience_factor(self, mode):
        """Optimized experience calculation."""
        experiences = self.mode_experiences[mode]
        if not experiences:
            return 0.5
        return sum(experiences) / len(experiences)  # Faster than np.mean for small lists

    def calculate_utility(self, mode):
        """Optimized utility calculation."""
        if mode == 'walk' and self.commute_distance > self.max_walk_distance:
            return float('-inf')
        if mode == 'bike' and self.commute_distance > self.max_bike_distance:
            return float('-inf')
            
        conditions = self.model.get_conditions(self, mode)
        
        # Combine calculations to reduce operations
        utility = (
            (1 - conditions['cost'] / self.model.max_cost) * self.cost_sensitivity * 0.3 +
            (1 - conditions['time'] / self.model.max_time) * self.time_sensitivity * 0.3 +
            conditions['comfort'] * self.comfort_preference * 0.2 +
            conditions['environmental_impact'] * self.environmental_preference * 0.1 +
            self.get_experience_factor(mode) * 0.1
        )
        
        return utility * (1 - self.model.weather_condition if mode in ['bike', 'walk'] else 1)

    def update_experience(self):
        """Update experience with current mode based on trip satisfaction."""
        # Calculate satisfaction based on actual vs expected utility
        expected_utility = self.calculate_utility(self.transport_mode)
        actual_conditions = self.model.get_conditions(self, self.transport_mode)
        actual_utility = expected_utility * (
            1 - self.model.traffic_level if self.transport_mode == 'car' else 1
        )
        
        satisfaction = (actual_utility / expected_utility) if expected_utility > 0 else 0
        self.mode_experiences[self.transport_mode].append(satisfaction)

    def choose_transport(self):
        """Choose transportation mode based on highest utility with some randomness."""
        utilities = {
            'car': self.calculate_utility('car'),
            'public_transit': self.calculate_utility('public_transit'),
            'bike': self.calculate_utility('bike'),
            'walk': self.calculate_utility('walk')
        }
        
        # Add some randomness to choices (exploration)
        exploration_rate = max(0.1, 1.0 / (1.0 + self.trips_made * 0.1))
        if self.random.random() < exploration_rate:
            self.transport_mode = self.random.choice(list(utilities.keys()))
        else:
            self.transport_mode = max(utilities, key=utilities.get)

    def step(self):
        """Make transportation choice and update experiences."""
        old_mode = self.transport_mode
        self.choose_transport()
        
        # Update statistics
        conditions = self.model.get_conditions(self, self.transport_mode)
        self.commute_time = conditions['time']
        self.commute_cost = conditions['cost']
        self.trips_made += 1
        
        # Update experience if not first trip
        if old_mode:
            self.update_experience()

class TransportationModel(mesa.Model):
    """Model of transportation choices in a city."""
    
    def __init__(self, N, width, height):
        super().__init__()
        self.num_agents = N
        self.grid = mesa.space.MultiGrid(width, height, True)
        self.schedule = mesa.time.RandomActivation(self)
        
        # Time tracking
        self.hour = 7
        self.minute = 0
        
        # Dynamic parameters
        self.gas_price = 3.50
        self.transit_fare = 2.50
        self.base_traffic_level = 0.3
        self.traffic_level = self.base_traffic_level
        self.weather_condition = 0.0
        self.max_cost = 20.0
        self.max_time = 120.0
        
        # Cache for performance
        self._mode_counts = {
            'car': 0,
            'public_transit': 0,
            'bike': 0,
            'walk': 0
        }
        self._total_time = 0
        self._total_cost = 0
        
        # Rolling window for mode history (last 100 steps)
        self.mode_history = deque(maxlen=100)
        
        # Create agents
        for i in range(self.num_agents):
            agent = CommuterAgent(i, self)
            home_x, home_y = self.get_random_location()
            work_x, work_y = self.get_work_location(home_x, home_y)
            
            agent.home_location = (home_x, home_y)
            agent.work_location = (work_x, work_y)
            agent.current_location = agent.home_location
            agent.commute_distance = np.sqrt(
                (work_x - home_x) ** 2 + (work_y - home_y) ** 2
            ) * 0.5
            
            self.grid.place_agent(agent, agent.home_location)
            self.schedule.add(agent)
        
        # Data collection - only collect essential metrics
        self.datacollector = mesa.DataCollector(
            model_reporters={
                "Car_Users": lambda m: m._mode_counts['car'],
                "Transit_Users": lambda m: m._mode_counts['public_transit'],
                "Bike_Users": lambda m: m._mode_counts['bike'],
                "Walk_Users": lambda m: m._mode_counts['walk'],
                "Average_Commute_Time": lambda m: m._total_time / m.num_agents if m.num_agents > 0 else 0,
                "Average_Commute_Cost": lambda m: m._total_cost / m.num_agents if m.num_agents > 0 else 0
            }
        )

    def get_random_location(self):
        """Get a random location on the grid."""
        return (
            self.random.randrange(self.grid.width),
            self.random.randrange(self.grid.height)
        )

    def get_work_location(self, home_x, home_y):
        """Get a work location with realistic distance distribution."""
        # Use a log-normal distribution for commute distances
        distance = np.random.lognormal(1.5, 0.5)
        angle = self.random.random() * 2 * np.pi
        
        dx = int(distance * np.cos(angle))
        dy = int(distance * np.sin(angle))
        
        # Ensure coordinates are within grid
        work_x = (home_x + dx) % self.grid.width
        work_y = (home_y + dy) % self.grid.height
        
        return work_x, work_y

    def update_time(self):
        """Update time of day."""
        self.minute += 1
        if self.minute >= 60:
            self.minute = 0
            self.hour += 1
        if self.hour >= 24:
            self.hour = 0

    def update_conditions(self):
        """Update dynamic conditions like traffic and weather."""
        # Update traffic based on time of day
        rush_hour_factor = self.get_rush_hour_factor()
        random_factor = 0.1 * (self.random.random() - 0.5)
        self.traffic_level = min(1.0, max(0.1,
            self.base_traffic_level * rush_hour_factor + random_factor
        ))
        
        # Update weather randomly
        if self.random.random() < 0.1:  # 10% chance to change weather
            self.weather_condition = min(1.0, max(0.0,
                self.weather_condition + 0.2 * (self.random.random() - 0.5)
            ))

    def get_rush_hour_factor(self):
        """Calculate traffic factor based on time of day."""
        hour = self.hour + self.minute / 60.0
        
        # Morning rush hour (7-9 AM)
        if 7 <= hour < 9:
            return 2.0
        # Evening rush hour (4-6 PM)
        elif 16 <= hour < 18:
            return 2.0
        # Late night (11 PM - 5 AM)
        elif hour < 5 or hour >= 23:
            return 0.5
        # Normal hours
        else:
            return 1.0

    def get_weather_penalty(self):
        """Get weather penalty for outdoor modes."""
        return self.weather_condition

    def update_cached_counts(self):
        """Update cached counts efficiently."""
        # Reset counters
        self._mode_counts = {mode: 0 for mode in self._mode_counts}
        self._total_time = 0
        self._total_cost = 0
        
        # Single pass through agents
        for agent in self.schedule.agents:
            if agent.transport_mode:
                self._mode_counts[agent.transport_mode] += 1
                self._total_time += agent.commute_time
                self._total_cost += agent.commute_cost

    def get_conditions(self, agent, mode):
        """Calculate conditions for a given transport mode - with caching."""
        distance = agent.commute_distance
        rush_factor = self.get_rush_hour_factor()
        
        # Cache key for conditions
        cache_key = (distance, rush_factor, self.traffic_level, self.weather_condition)
        
        # Check if conditions are cached
        if hasattr(self, '_conditions_cache'):
            if cache_key in self._conditions_cache:
                return self._conditions_cache[cache_key][mode]
        else:
            self._conditions_cache = {}
        
        # Calculate conditions
        conditions = {
            'car': {
                'cost': self.gas_price * (distance * 0.1),
                'time': distance * (1 + self.traffic_level * rush_factor),
                'comfort': 0.8 - (0.3 * self.traffic_level),
                'environmental_impact': 0.2
            },
            'public_transit': {
                'cost': self.transit_fare,
                'time': distance * 1.5 * rush_factor,
                'comfort': 0.5,
                'environmental_impact': 0.7
            },
            'bike': {
                'cost': 0.1 * distance,
                'time': distance * 2,
                'comfort': 0.4 * (1 - self.weather_condition),
                'environmental_impact': 0.9
            },
            'walk': {
                'cost': 0,
                'time': distance * 4,
                'comfort': 0.3 * (1 - self.weather_condition),
                'environmental_impact': 1.0
            }
        }
        
        # Cache the results
        self._conditions_cache[cache_key] = conditions
        
        # Clear cache if it gets too large
        if len(self._conditions_cache) > 1000:
            self._conditions_cache.clear()
        
        return conditions[mode]

    def step(self):
        """Advance the model by one step."""
        self.update_time()
        self.update_conditions()
        
        # Clear conditions cache if weather or traffic changes significantly
        if hasattr(self, '_conditions_cache'):
            self._conditions_cache.clear()
        
        # Update agents
        self.schedule.step()
        
        # Update cached counts
        self.update_cached_counts()
        
        # Collect data
        self.datacollector.collect(self)