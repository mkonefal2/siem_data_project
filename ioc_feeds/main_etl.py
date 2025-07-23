import yaml
from loguru import logger
from pathlib import Path

from fetchers.blocklist import fetch_blocklist
from fetchers.threatfox import fetch_threatfox
from parsers.blocklist_parser import parse_blocklist
from parsers.threatfox_parser import parse_threatfox
from storage.duckdb_handler import DuckDBHandler


def load_config(path: str) -> dict:
    with open(path, 'r') as f:
        return yaml.safe_load(f)


def run_etl(config_path: str = 'config.yaml'):
    config = load_config(config_path)

    db_handler = DuckDBHandler(
        config['output']['database'],
        config['output'].get('csv_backup')
    )

    records = []

    block_cfg = config['sources'].get('blocklist_de')
    if block_cfg:
        lines = fetch_blocklist(block_cfg['url'])
        records.extend(parse_blocklist(lines, source='blocklist.de'))

    threat_cfg = config['sources'].get('threatfox')
    if threat_cfg:
        data = fetch_threatfox(threat_cfg['url'], threat_cfg.get('api_payload', {}))
        records.extend(parse_threatfox(data, source='threatfox'))

    db_handler.insert_many(records)


def main():
    logger.add('etl.log')
    run_etl(Path(__file__).with_name('config.yaml'))


if __name__ == '__main__':
    main()
