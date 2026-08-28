"""Main orchestrator for the synthetic data generator."""

import argparse
import logging
import sys
from generator.config import PROJECT_CONFIG, SCALE_CONFIGS
from generator.constants import initialize_seeds
from generator.generators.games import generate_games
from generator.generators.app_versions import generate_app_versions
from generator.generators.campaigns import generate_campaigns

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)]
    )

def main():
    setup_logging()
    
    parser = argparse.ArgumentParser(description="NovaPlay Games Synthetic Data Generator")
    parser.add_argument("--scale", type=str, choices=["small", "medium", "portfolio"], default="small", help="Scale of the generation")
    parser.add_argument("--seed", type=int, default=PROJECT_CONFIG["seed"], help="Random seed for deterministic generation")
    args = parser.parse_args()
    
    # 1. Initialize Determinism
    initialize_seeds(args.seed)
    logging.info(f"Initialized generation with seed: {args.seed} and scale: {args.scale}")
    
    # 2. Generate Master Data
    logging.info("Generating games...")
    games = generate_games()
    logging.info(f"Generated {len(games)} games")
    
    logging.info("Generating app versions...")
    app_versions = generate_app_versions(games)
    logging.info(f"Generated {len(app_versions)} app versions")
    
    logging.info("Generating campaigns...")
    campaigns = generate_campaigns(games)
    logging.info(f"Generated {len(campaigns)} campaign records (including historical states)")
    
    logging.info("Sprint A Master Data Generation complete!")

if __name__ == "__main__":
    main()
