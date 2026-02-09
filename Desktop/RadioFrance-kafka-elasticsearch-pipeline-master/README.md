# 🎙️ Radio France Streaming Analytics Pipeline with Kafka, Spark and Elastic Stack

A real-time data pipeline for collecting, processing, analyzing, and
visualizing live broadcasts from Radio France stations.

This project demonstrates a complete modern streaming analytics
architecture using Big Data technologies.

---

## 🎯 Features

### 🔄 Real-time Data Collection

- Automatic polling of Radio France GraphQL API every 5 minutes\
- 30+ stations covered (France Inter, France Culture, France Info,
  France Musique, FIP, Mouv', local France Bleu stations)\
- Enriched data: geolocation, broadcast themes\
- Kafka publishing: structured JSON messages to `radiofrance-live`
  topic

### ⚡ Data Processing

- Logstash enrichment and transformation\
- Automatic geocoding for local stations\
- Theme extraction and categorization\
- Elasticsearch indexing optimized for search

### 🧠 Distributed Analytics

- Apache Spark distributed computations\
- Aggregations by station, hour, theme\
- Real-time broadcast calculations\
- Results persisted to Elasticsearch

### 📊 Visualization

- Kibana dashboards with auto-refresh\
- Raw vs analytics indices\
- Geographic mapping for France Bleu stations

---

### Data Flow

1.  **Collection:** Python → Radio France API → Kafka\
2.  **Processing:** Kafka → Logstash → Elasticsearch (raw)\
3.  **Analytics:** Elasticsearch → Spark → Elasticsearch (results)\
4.  **Visualization:** Elasticsearch → Kibana

---

## 📁 Project Structure

    RadioFrance-kafka-elasticsearch-pipeline/
    ├── 📄 docker-compose.yml              # Docker services configuration
    ├── 📄 .env                            # Environment variables template
    ├── 📄 README.md                       # This documentation
    ├── 📄 RADIOFRANCE_API.md              # How to use the Radio France Open API
    ├── 📁 api-collector/                  # Data collection service
    │   ├── 📄 Dockerfile                  # Collector Docker image
    │   ├── 📄 requirements.txt            # Python dependencies
    │   └── 📄 radiofrance_realtime_collector.py  # Main collection script
    ├── 📁 elasticsearch/                  # Elasticsearch configuration
    │   └── 📁 mappings/                   # Index mappings
    │       ├── 📄 radiofrance-mapping.json        # Raw data mapping
    │       └── 📄 radiofrance-analytics-mapping.json  # Analytics results mapping
            📁 queries/                    # Queries to index
    │       ├── 📄 aggs.json               # Aggregation query
    │       └── 📄 fuzzy.json              # Fuzziness query
            └── 📄 n-gram.json             # N-gram query
            └── 📄 temporal-serie.json     # Time serie query
            └── 📄 textual.json            # Textual query
    ├── 📁 logstash/                       # Logstash configuration
    │   └── 📁 pipeline/
    │       └── 📄 radiofrance-live.conf   # Processing pipeline
    └── 📁 spark/                          # Spark jobs and configuration
        ├── 📁 config/
        │   └── 📄 spark_config.py         # Spark session configuration
        └── 📁 jobs/
            └── 📄 spark_corrected_final.py  # Main analytics job (final version)

---

## 🚀 Quick Start

### Prerequisites

- Docker Desktop 20.10+\
- 4GB+ RAM allocated to Docker\
- Git
- Radio France API Key (for testing)

### Installation

```bash
git clone https://github.com/khaledbouabdallah/RadioFrance-kafka-elasticsearch-pipeline.git
cd RadioFrance-kafka-elasticsearch-pipeline
# Edit the .env file with your parameters
```

Start services:

```bash
# Launch all services
docker-compose up -d
# Verify all services are running
docker-compose ps
```

---

## ⚙️ Configuration

Example `.env`:

```env
RADIOFRANCE_API_KEY=your_api_key_here
KAFKA_BOOTSTRAP_SERVERS=kafka:9092
KAFKA_TOPIC=radiofrance-live
POLL_INTERVAL=300
ELASTICSEARCH_HOST=http://elasticsearch:9200
SPARK_MASTER=spark://spark-master:7077
```

---

## 🔧 Detailed Services

- **Zookeeper** -- Kafka coordination\
- **Kafka** -- Streaming broker\
- **Elasticsearch** -- Data storage and search\
- **Kibana** -- Visualization\
- **Logstash** -- Data processing\
- **API Collector** -- Data ingestion\
- **Spark Cluster** -- Distributed analytics

---

## 🌐 Access interfaces

- Kibana : http://localhost:15601
- Spark Master UI : http://localhost:18080
- Elasticsearch : http://localhost:19200
- Spark Worker UI : http://localhost:18081

## 📊 Spark Analytics Job

Manual execution:

```bash
docker exec spark-master /opt/spark/bin/spark-submit \
  --master spark://spark-master:7077 \
  --packages org.elasticsearch:elasticsearch-spark-30_2.12:8.12.0 \
  /opt/spark/jobs/spark_corrected_final.py
```

What the Job Does :

- Loads data from Elasticsearch (index radiofrance-live-\*)

- Cleans and transforms the data

- Calculates statistics:

      +   Total broadcasts per station

      +   Average themes per broadcast

      +   Number of available podcasts

      +   Temporal distribution of broadcasts

- Saves results to Elasticsearch (index radiofrance-analytics\*)

---

## 📈 Kibana Visualization

1.  Create Data Views:
    - `radiofrance-live*`
    - `radiofrance-analytics*`
2.  Build visualizations:
    - Maps\
    - Lens charts\
    - Heatmaps\
    - Tag Cloud\
    - Data Tables
3.  Create dashboard:
    - Auto-refresh: 30s\
    - Time range: Last 1 hour

---

## 🧪 Testing and Validation

### Docker

```bash
# Verify all services are running
docker-compose ps
# Show logs for a specific service
docker-compose logs -f api-collector
```

### Kafka

```bash
# List Kafka topics
docker exec kafka kafka-topics --list --bootstrap-server localhost:9092
```

### Elasticsearch

```bash
# List all indices
curl http://localhost:19200/_cat/indices?v
# Count Radio France documents
curl http://localhost:19200/radiofrance*/_count
# See a sample document
curl http://localhost:19200/radiofrance-live*/_search?size=1&pretty
```

### Spark

```bash
# Run a simple test
docker exec spark-master /opt/spark/bin/spark-submit --version
```

---

## 🔍 Troubleshooting

### Port Already in Use

Modify ports in `docker-compose.yml`.

### No Data in Kibana

- Check time range\
- Verify Data Views\
- Confirm Elasticsearch indices

### Reset Environment

```bash
docker-compose down -v
docker-compose up -d --build
```

---

## 👥 Contributing

1.  Fork the repository\
2.  Create a feature branch\
3.  Commit changes\
4.  Push and open a Pull Request

### Code Standards

- Python: PEP 8\
- Docker best practices\
- Clear Markdown documentation

---

**Author:** Mouad TAHIRI - Khaled BOUABDALLAH
 
lun.  9 févr. 2026 22:04:09
