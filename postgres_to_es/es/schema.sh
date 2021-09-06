curl -XPUT http://127.0.0.1:9200/filmwork -H 'Content-Type: application/json' -d'
{
  "settings": {
    "refresh_interval": "1s"
  },
  "mappings": {
    "properties": {
      "title": {
        "type": "text"
      },
      "description": {
        "type": "text"
      },
      "rating": {
        "type": "float"
      },
      "type": {
        "type": "text"
      },
      "created": {
        "type": "date"
      },
      "modified": {
        "type": "date"
      },
      "genre_name": {
        "type": "text"
      },
      "persons": {
        "type": "nested",
        "dynamic": "strict",
        "properties": {
          "id": {
            "type": "keyword"
          },
          "first_name": {
            "type": "text"
          },
          "second_name": {
            "type": "text"
          }
        }
      }
    }
  }
}'