from ioc_feeds.parsers.blocklist_parser import parse_blocklist
from ioc_feeds.parsers.threatfox_parser import parse_threatfox


def test_parse_blocklist():
    lines = ["1.1.1.1", "2.2.2.2"]
    records = parse_blocklist(lines)
    assert len(records) == 2
    assert records[0]["value"] == "1.1.1.1"
    assert records[0]["type"] == "ip"


def test_parse_threatfox():
    data = [
        {"ioc_type": "ip", "ioc": "3.3.3.3", "malware": "test"},
        {"ioc_type": "url", "ioc": "http://malicious.com"},
    ]
    records = parse_threatfox(data)
    assert len(records) == 2
    assert records[0]["source"] == "threatfox"
