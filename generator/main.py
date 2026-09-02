"""Main orchestrator for the synthetic data generator."""

import argparse
import logging
import sys
from generator.config import PROJECT_CONFIG, SCALE_CONFIGS
from generator.constants import initialize_seeds
from generator.generators.games import generate_games
from generator.generators.app_versions import generate_app_versions
from generator.generators.campaigns import generate_campaigns
from generator.generators.installs import generate_installs
from generator.generators.game_events import generate_game_events
from generator.generators.iap_purchases import generate_iap_purchases
from generator.generators.ad_impressions import generate_ad_impressions
from generator.generators.ua_spend import generate_ua_spend
from generator.utils.dq_injection import inject_dq_issues
from generator.utils.writers import write_csv, write_json_batches
from generator.utils.manifest import create_manifest
from generator.validators.validation_runner import run_validation
import os

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
    
    # 3. Generate Player Population
    logging.info("Generating installs...")
    installs = generate_installs(games, app_versions, campaigns, args.scale)
    logging.info(f"Generated {len(installs)} installs")
    
    # 4. Generate Engagement
    logging.info("Generating game events...")
    game_events = generate_game_events(installs, app_versions)
    logging.info(f"Generated {len(game_events)} game events")
    
    # 5. Generate Monetization & Marketing
    logging.info("Generating IAP purchases...")
    iap = generate_iap_purchases(installs, game_events)
    logging.info(f"Generated {len(iap)} IAP purchases")
    
    logging.info("Generating ad impressions...")
    ads = generate_ad_impressions(installs, game_events)
    logging.info(f"Generated {len(ads)} ad impressions")
    
    logging.info("Generating UA spend...")
    ua = generate_ua_spend(campaigns, installs)
    logging.info(f"Generated {len(ua)} UA spend records")
    
    datasets = {
        "installs": installs,
        "game_events": game_events,
        "iap_purchases": iap,
        "ad_impressions": ads,
        "ua_spend": ua
    }
    
    # 6. Inject DQ
    logging.info("Injecting Controlled Data Quality issues...")
    datasets, dq_stats = inject_dq_issues(datasets)
    logging.info(f"DQ Injected: {dq_stats}")
    
    # 7. Write Data
    logging.info("Writing Master Data...")
    # Convert Game, AppVersion, Campaign objects to dicts for CSV writer
    write_csv([g.__dict__ for g in games], "games", "games.csv")
    write_csv([v.__dict__ for v in app_versions], "app_versions", "app_versions.csv")
    write_csv([c.__dict__ for c in campaigns], "campaigns", "campaigns.csv")
    
    logging.info("Writing Transactional Data...")
    # Group by date based on install_time and event_time (and late arrivals)
    write_json_batches(datasets["installs"], "installs", date_field="install_time")
    write_json_batches(datasets["game_events"], "game_events", date_field="event_time")
    write_json_batches(datasets["iap_purchases"], "iap_purchases", date_field="purchase_time")
    write_json_batches(datasets["ad_impressions"], "ad_impressions", date_field="event_time")
    write_csv(datasets["ua_spend"], "ua_spend", "ua_spend.csv")
    
    # 8. Manifest & 9. Validation
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    logging.info("Creating generation manifest...")
    dataset_counts = {
        "games": len(games),
        "app_versions": len(app_versions),
        "campaigns": len(campaigns),
        "installs": len(datasets["installs"]),
        "game_events": len(datasets["game_events"]),
        "iap_purchases": len(datasets["iap_purchases"]),
        "ad_impressions": len(datasets["ad_impressions"]),
        "ua_spend": len(datasets["ua_spend"])
    }
    
    # Use seed as generation ID for determinism
    generation_id = f"run_seed_{args.seed}_{args.scale}"
    
    create_manifest(generation_id, args.seed, args.scale, dataset_counts, dq_stats, base_dir)
    
    logging.info("Running validation suite...")
    report = run_validation(datasets, dq_stats, base_dir)
    logging.info(f"Validation completed. Status: {report['status']}")
    
    logging.info("Data Generation Phase 3 complete!")

if __name__ == "__main__":
    main()
