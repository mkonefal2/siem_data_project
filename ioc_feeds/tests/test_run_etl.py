import yaml
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from ioc_feeds import main_etl


def test_run_etl_threatfox_failure(tmp_path, monkeypatch):
    config = {
        'sources': {
            'blocklist_de': {'url': 'dummy', 'type': 'ip'},
            'threatfox': {'url': 'dummy', 'api_payload': {'query': 'get_iocs'}},
        },
        'output': {
            'database': str(tmp_path / 'db.duckdb'),
            'csv_backup': None,
        },
    }
    cfg_path = tmp_path / 'config.yaml'
    cfg_path.write_text(yaml.dump(config))

    inserted = []

    class DummyHandler:
        def __init__(self, db_path, csv_backup=None):
            pass

        def insert_many(self, records):
            inserted.extend(records)

    monkeypatch.setattr(main_etl, 'DuckDBHandler', DummyHandler)
    monkeypatch.setattr(main_etl, 'fetch_blocklist', lambda url: ['1.1.1.1'])
    def failing_fetch(*args, **kwargs):
        raise RuntimeError('fail')
    monkeypatch.setattr(main_etl, 'fetch_threatfox', failing_fetch)

    main_etl.run_etl(str(cfg_path))

    assert len(inserted) == 1
    assert inserted[0]['value'] == '1.1.1.1'
