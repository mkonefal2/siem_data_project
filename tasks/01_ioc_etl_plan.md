

##  **Moduł pobierania IoC (ETL – Extract)**

### 📌 Cel modułu:

**Automatyczne pozyskanie danych o wskaźnikach kompromitacji (IoC)** z różnych publicznych źródeł OSINT, ich normalizacja oraz zapis do ustandaryzowanej struktury bazy danych.

---

## 🛠️ **Szczegółowa checklista techniczna**:

### 🔸 1. **Konfiguracja źródeł danych (config.yaml)**

* [ ] Przygotuj plik konfiguracyjny (`config.yaml`):

  ```yaml
  sources:
    blocklist_de:
      url: "https://lists.blocklist.de/lists/all.txt"
      type: "ip"
    threatfox:
      url: "https://threatfox-api.abuse.ch/api/v1/"
      api_payload:
        query: "get_iocs"
        days: 1
      # Optional API key or custom headers
      api_key: "YOUR_API_KEY"
      headers:
        Accept: "application/json"
      type: "json"
    nvd:
      url: "https://services.nvd.nist.gov/rest/json/cves/2.0"
      type: "json"
  output:
    database: "./database/ioc_data.duckdb"
    csv_backup: "./database/ioc_backup.csv"
  ```

---

### 🔸 2. **Automatyczne pobieranie danych**

* [ ] Zaimplementuj klasy/funkcje dla każdego źródła:

  **Przykładowy pseudokod**:

  ```python
  def fetch_blocklist(url):
      response = requests.get(url)
      return response.text.splitlines()

  def fetch_threatfox(url, payload, headers=None):
      response = requests.post(url, json=payload, headers=headers)
      return response.json()['data']

  def fetch_nvd_cve(url):
      response = requests.get(url)
      return response.json()['vulnerabilities']
  ```

* [ ] Obsłuż błędy HTTP (retry, logging)

---

### 🔸 3. **Standaryzacja i parsowanie danych**

Utwórz jedną wspólną strukturę danych:

| Pole         | Opis                                           | Przykład                 |
| ------------ | ---------------------------------------------- | ------------------------ |
| type         | Typ IoC (`ip`, `domain`, `url`, `hash`, `cve`) | `"ip"`                   |
| value        | Wartość IoC                                    | `"185.203.119.177"`      |
| source       | Źródło pochodzenia IoC                         | `"blocklist.de"`         |
| threat\_type | Typ zagrożenia (opcjonalnie z danych)          | `"ssh_bruteforce"`       |
| timestamp    | Data pozyskania IoC                            | `"2025-07-23T10:00:00Z"` |

* [ ] Zaimplementuj parsery specyficzne dla źródeł:

  * Blocklist.de (`txt` → `"ip"`)
  * ThreatFox (`json` → `"ip", "url", "hash"`)
  * NVD CVE (`json` → `"cve"`)

Przykładowy ustandaryzowany wynik parsowania:

```json
{
    "type": "ip",
    "value": "185.203.119.177",
    "source": "blocklist.de",
    "threat_type": "ssh_bruteforce",
    "timestamp": "2025-07-23T10:00:00Z"
}
```

---

### 🔸 4. **Wzbogacanie IoC (opcjonalne)**

* [ ] Wzbogacenie danych geolokalizacją (`geoip2`):

  ```json
  "geo": {
    "country": "RU",
    "continent": "Europe",
    "city": "Moscow"
  }
  ```
* [ ] Tagi zagrożeń (opcjonalnie): `"tags": ["bruteforce", "ssh"]`

---

### 🔸 5. **Zapis danych**

* [ ] Zapis do bazy danych DuckDB lub PostgreSQL:

  ```python
  import duckdb
  conn = duckdb.connect('./database/ioc_data.duckdb')

  conn.execute("""
      CREATE TABLE IF NOT EXISTS ioc (
          type VARCHAR, 
          value VARCHAR, 
          source VARCHAR, 
          threat_type VARCHAR, 
          timestamp TIMESTAMP, 
          country VARCHAR
      )
  """)

  conn.execute("""
      INSERT INTO ioc VALUES (?, ?, ?, ?, ?, ?)
  """, [data['type'], data['value'], data['source'], data['threat_type'], data['timestamp'], data['geo']['country']])
  ```

* [ ] Opcjonalny backup danych w CSV:

  ```python
  df.to_csv('./database/ioc_backup.csv', mode='a', header=False)
  ```

---

### 🔸 6. **Automatyzacja procesu**

* [ ] Zautomatyzuj pobieranie danych w regularnych odstępach czasu (`schedule`):

  ```python
  schedule.every(60).minutes.do(run_ioc_etl_pipeline)
  ```
* [ ] Ewentualnie użyj Airflow w przyszłości.

---

### 🔸 7. **Logowanie i monitoring**

* [ ] Loguj szczegółowo każdy etap ETL (`loguru`, `logging`):

  ```python
  from loguru import logger

  logger.info("Pobrano {} rekordów z blocklist.de", len(records))
  logger.error("Błąd podczas pobierania: {}", e)
  ```
* [ ] Dodaj metryki dla monitoringu procesu (liczba IoC, czas wykonania).

---

### 🔸 8. **Testy modułu**

* [ ] Zaimplementuj testy jednostkowe (pytest) dla parserów danych:

  ```python
  def test_blocklist_parser():
      sample_data = "185.203.119.177\n192.168.1.1"
      assert parse_blocklist(sample_data) == ["185.203.119.177", "192.168.1.1"]
  ```
* [ ] Test integracyjny (pobranie ➝ parsowanie ➝ zapis do DuckDB).

---

### 🔸 9. **Konteneryzacja (opcjonalnie)**

* [ ] Dockerfile z Pythonem + DuckDB/PostgreSQL
* [ ] docker-compose.yml do szybkiego uruchomienia lokalnego środowiska

---

### 🗂 **Finalna struktura tego modułu**

```
/ioc_feeds/
├── fetchers/
│   ├── blocklist.py
│   ├── threatfox.py
│   └── nvd.py
├── parsers/
│   ├── blocklist_parser.py
│   ├── threatfox_parser.py
│   └── nvd_parser.py
├── enrichments/
│   └── geoip.py
├── storage/
│   └── duckdb_handler.py
├── tests/
│   ├── test_fetchers.py
│   └── test_parsers.py
├── config.yaml
└── main_etl.py
```

