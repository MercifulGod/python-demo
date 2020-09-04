#### 文档导航
elasticsearch (7.9.1)客户端： https://elasticsearch-py.readthedocs.io/  
elasticsearch-dsl (7.2.1)： https://elasticsearch-dsl.readthedocs.io/en/latest/persistence.html  
ES7.9官方文档：https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html  

####  ZkConfig.java
``` commandline
curl -X GET "localhost:9200/person/_search?pretty" -H 'Content-Type: application/json' -d'
{
    "query": {
        "bool": {
            "filter": [
                {
                    "term": {
                        "desc": "desc"
                    }
                }
            ]
        }
    }
}
'
```

