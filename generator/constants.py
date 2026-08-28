"""Global constants and deterministic seeding for the generator."""

import random
import numpy as np
from faker import Faker

from generator.config import PROJECT_CONFIG

# Deterministic seeding based on config
SEED = PROJECT_CONFIG["seed"]

def initialize_seeds(seed=SEED):
    """Initialize all random number generators with a fixed seed."""
    random.seed(seed)
    np.random.seed(seed)
    Faker.seed(seed)

fake = Faker()
