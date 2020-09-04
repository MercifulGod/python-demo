# coding=utf-8
from __future__ import print_function, unicode_literals

import operator
import unittest
from datetime import datetime
from time import sleep
from elasticsearch.helpers import bulk, scan
from elasticsearch_dsl import connections, Document, Completion, Text, Long, Keyword, analyzer, token_filter, Date, \
    Integer, MetaField, Float, Object, Search, Q

ES_CONNECTION_KEY = 'es'

connections.create_connection(ES_CONNECTION_KEY, hosts=['localhost'], timeout=20)
es = connections.get_connection(ES_CONNECTION_KEY)


class Person(Document):
    id = Keyword()
    name = Keyword()
    age = Integer()
    create_time = Date(doc_values=True, format="dateOptionalTime")
    desc = Keyword(index=False, doc_values=True)

    class Meta:
        # all = MetaField(enabled=False)
        dynamic = MetaField('false')

    class Index:
        name = "person"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}


class Article(Document):
    name = Keyword()
    create_time = Date(doc_values=True, format="dateOptionalTime")
    desc = Keyword(index=False, doc_values=True)

    class Meta:
        dynamic = MetaField('false')

    class Index:
        name = "article"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}


class EntityTest(unittest.TestCase):
    def setUp(self):
        es.indices.delete(index=Person._index._name, ignore=[400, 404])
        Person.init(using=es)

    def tearDown(self):
        es.indices.delete(index=Person._index._name, ignore=[400, 404])

    def test_save(self):
        # 添加方式一:
        Person(id="1", name="张三", age=13, create_time=datetime.now(), desc="desc").save(using=es)
        Person._index.refresh(using=es)  # 手动refresh

        # 添加方式二:
        p = Person(id="2", name="李四")
        p.age = 14
        p.desc = "desc"
        p.create_time = "2013-10-10 23:40:00"
        p.save(refresh=True, using=es)

        s = Search(using=es, index=Person._index._name)
        res = s.execute()
        self.assertEqual("张三", res.hits[0].name)
        self.assertEqual("李四", res.hits[1].name)

    def test_delete(self):
        person = Person(id="1", name="唐僧", age=66, create_time=datetime.now(), desc="desc", meta={'id': 42})
        self.assertEqual(42, person.meta.id)
        person.save(using=es)

        # 插入几条测试数据
        Person(id="2", name="张三", age=15, create_time="2013-09-10 23:40:00").save(using=es)
        Person(id="3", name="李四", age=16, create_time="2013-10-10 23:40:00").save(using=es)
        Person(id="4", name="王五", age=17, create_time="2013-11-10 23:40:00").save(using=es)
        Person._index.refresh(using=es)

        # 单个删除
        p = Person.get(id=42, using=es, ignore=[400, 404])
        p.delete(using=es)
        self.assertIsNone(Person.get(id=42, using=es, ignore=[400, 404]))  # 添加ignore, 否则当没有该文档时,会抛出异常

        # 批量删除方式一
        s = Search(using=es, index=Person._index._name).filter('term', name="张三")
        res = s.delete()
        self.assertEqual(1, res.deleted)

        # 批量删除方式二
        s = Search(using=es, index=Person._index._name).filter('term', name="李四")
        res = [hit for hit in scan(es, query=s.to_dict(), index=Person._index._name)]
        for r in res:   r['_op_type'] = 'delete'
        bulk(es, res, params={"refresh": 'true'})

        # 验证结果
        total = Search(using=es, index=Person._index._name).count()
        self.assertEqual(1, total)

    def test_search(self):
        person = Person(id="1", name="唐僧", age=11, create_time=datetime.now(), desc="desc", meta={'id': 42})
        person.save(using=es)

        Person(id="2", name="张三", age=12, create_time="2013-09-10 23:40:00").save(using=es)
        Person(id="3", name="李四", age=13, create_time="2013-10-10 23:40:00").save(using=es)
        Person(id="4", name="王五", age=14, create_time="2013-11-10 23:40:00").save(using=es)
        Person._index.refresh(using=es)

        # 通过ID获取文档
        doc = Person.get(id=42, using=es, ignore=[400, 404])
        self.assertEqual("唐僧", doc.name)

        # 查询方式一
        s = Search(using=es, index=Person._index._name)
        res = s.query('bool', filter=[Q('term', name="张三")]).execute()
        self.assertEqual("张三", res.hits[0].name)

        # 查询方式二
        res = Person.search(using=es).filter('term', name='李四').execute()
        self.assertEqual("李四", res.hits[0].name)

        # 分页查询
        offset, limit = 1, 2
        hits = Person.search(using=es)[offset:offset + limit].execute().hits
        total = hits.total.value
        self.assertEqual("张三", hits[0].name)
        self.assertEqual("李四", hits[1].name)
        self.assertEqual(2, len(hits))
        self.assertEqual(4, total)

        # 查询响应结果
        res = Person.search(using=es)[offset:offset + limit].execute()
        for h in res:
            print(h.to_dict())

        # 计数查询 + 链式查询
        total = Person.search(using=es).filter('term', name='李四').filter('term', age=13).count()
        self.assertEqual(1, total)

        # 范围查询
        s = Person.search(using=es)
        total = s.filter(Q("range", **{"age": {"gt": 11}}) & Q("range", **{"age": {"lt": 18}})).count()
        self.assertEqual(3, total)

        # 按时间过滤，可以直接使用 date/datetime 对象，或者 13 位的毫秒时间戳
        # 不建议用时间字符串。如果要用字符串，需要在字符串后面添加 +800 时区信息，比如 yyyy-mm-ddT+0800 或
        # yyyy-mm-ddTHH:MM:SS+0800

        # 基本的聚合操作
        s = Person.search(using=es)
        s.aggs.bucket("per_name", 'terms', field="name", **{"size": 10000})
        res = s.execute()
        for item in res.aggregations.per_name.buckets:
            print(item.key, item.doc_count)

        # 较为完整的聚合示范, 双层聚合
        s = Search(using=es, index=Person._index._name)
        s.aggs.bucket("per_name", 'terms', field="name", **{"size": 10000}) \
            .bucket("per_age", 'terms', field="age", **{"size": 10000})
        res = s.execute()
        for item in operator.getitem(res.aggregations, "per_name").buckets:
            print(item.key, item.doc_count)
            for sub_item in operator.getitem(item, "per_age").buckets:
                print(sub_item.key, sub_item.doc_count)

        # 时间聚合
        s = Search(using=es, index=Person._index._name)
        s.aggs.bucket("per_month", 'date_histogram', field="create_time", **{"interval": "month", "min_doc_count": "1"})
        res = s.execute()
        for item in res.aggregations.per_month.buckets:
            print(item.key, item.doc_count)

        # max聚合
        s = Search(using=es, index=Person._index._name)
        s.aggs.metric("max_age", 'max', field="age")
        res = s.execute()
        self.assertEqual(float(14), res.aggregations.max_age.value)

        # bucket聚合 和 metric聚合双层聚合
        s = Search(using=es, index=Person._index._name)
        s.aggs.bucket("per_name", 'terms', field="name", **{"size": 10000}) \
            .metric("max_age", 'max', field="age")
        res = s.execute()
        for item in res.aggregations.per_name.buckets:
            max_age = item.max_age.get("value")
            print(item.key, item.doc_count, max_age)

    def test_update(self):
        person = Person(id="1", name="唐僧", age=66, create_time="2013-09-10 23:40:00", desc="desc", meta={'id': 42})
        res = person.save(using=es)
        self.assertEqual("created", res)

        # 更新方式一
        person = Person.get(id=42, using=es, ignore=[400, 404])
        person.name = "唠叨的唐僧"
        person.save(refresh=True, using=es)

        # 更新方式二
        doc = es.get(index=Person._index._name, ignore=404, id=42)
        person = Person.from_es(doc)
        person.age = 88
        person.save(refresh=True, using=es)

        # 更新方式三
        current_time = datetime.now()
        person.update(create_time=current_time, using=es)

        sleep(3)  # 则必须等待ES自动refresh, 否则查询的结果为空
        total = Person.search(using=es).filter('term', name='唠叨的唐僧') \
            .filter('term', age=88).filter('term', create_time=current_time).count()
        self.assertEqual(1, total)

    def test_bulk_update(self):
        Person(id="2", name="张三", age=12, create_time="2013-09-10 23:40:00").save(using=es)
        Person(id="3", name="李四", age=13, create_time="2013-10-10 23:40:00").save(using=es)
        Person(id="4", name="王五", age=14, create_time="2013-11-10 23:40:00").save(using=es)
        Person._index.refresh(using=es)
        s = Person.search(using=es).filter('term', name="张三")
        res = [hit for hit in scan(es, query=s.to_dict(), index=Person._index._name)]
        for r in res:
            source = r['_source']
            source.update({"name": "唐僧"})
            r['_source'] = {"doc": source}
            r['_op_type'] = 'update'
        bulk(es, res, params={"refresh": 'true'})
        total = Person.search(using=es).filter('term', name="唐僧").count()
        self.assertEqual(1, total)

    def test_scan(self):
        Person(id="2", name="张三", age=12, create_time="2013-09-10 23:40:00").save(using=es)
        Person(id="3", name="李四", age=13, create_time="2013-10-10 23:40:00").save(using=es)
        Person(id="4", name="王五", age=14, create_time="2013-11-10 23:40:00").save(using=es)
        Person._index.refresh(using=es)
        count = 0
        for hit in Person.search(using=es).filter('term', name="张三").scan():
            self.assertEqual("张三", hit.name)
            count += 1
        self.assertEqual(1, count)

    def test_like_filter(self):
        Person(id="2", name="张三", age=12, create_time="2013-09-10 23:40:00").save(using=es)
        Person(id="3", name="李四", age=13, create_time="2013-10-10 23:40:00").save(using=es)
        Person(id="4", name="王五", age=14, create_time="2013-11-10 23:40:00").save(using=es)
        Person._index.refresh(using=es)
        total = Person.search(using=es).filter(Q("regexp", **{"name": ".*"})).count()
        self.assertEqual(3, total)

    def test_prefix_filter(self):
        Person(id="2", name="张三", age=12, create_time="2013-09-10 23:40:00").save(using=es)
        Person(id="3", name="李四", age=13, create_time="2013-10-10 23:40:00").save(using=es)
        Person(id="4", name="王五", age=14, create_time="2013-11-10 23:40:00").save(using=es)
        Person._index.refresh(using=es)
        total = Person.search(using=es).filter(Q("prefix", **{"name": "张"})).count()
        self.assertEqual(1, total)

    def test_wildcard_filter(self):
        Person(id="2", name="张三", age=12, create_time="2013-09-10 23:40:00").save(using=es)
        Person(id="3", name="李四", age=13, create_time="2013-10-10 23:40:00").save(using=es)
        Person(id="4", name="王五", age=14, create_time="2013-11-10 23:40:00").save(using=es)
        Person._index.refresh(using=es)
        total = Person.search(using=es).filter(Q("wildcard", **{"name": "*" + str("五") + "*"})).count()
        self.assertEqual(1, total)

    def test_exists_filter(self):
        Person(name="李四", age=15).save(using=es)
        Person(name="张三").save(using=es)
        Person._index.refresh(using=es)
        total = Person.search(using=es).filter(Q("exists", **{"field": "name"})).count()
        self.assertEqual(2, total)

        total = Person.search(using=es).filter(Q("exists", **{"field": "age"})).count()
        self.assertEqual(1, total)

    def test_filter_with_id(self):
        Person(name="李四", age=15).save(using=es)
        Person(name="张三").save(using=es)
        Person._index.refresh(using=es)
        s = Search(using=es, index=Person._index._name).filter(Q("terms", **{"name": ["李四", "张三"]}))
        total = s.execute().hits.total.value
        self.assertEqual(2, total)

    def test_search_order_by(self):
        Person(name="李四", age=15).save(using=es)
        Person(name="1张三", age=13).save(using=es)
        Person(name="2张三", age=13).save(using=es)
        Person._index.refresh(using=es)
        s = Search(using=es, index=Person._index._name).sort("age", "-name")
        hits = s.execute().hits
        self.assertEqual("2张三", hits[0].name)
        self.assertEqual("1张三", hits[1].name)
        self.assertEqual(15, hits[2].age)

    def test_search_with_multiple_index(self):
        es.indices.delete(index=Person._index._name, ignore=[400, 404])
        es.indices.delete(index=Article._index._name, ignore=[400, 404])
        try:
            Person.init(using=es)
            Article.init(using=es)
            Person(name="李四").save(using=es, refresh=True)
            Article(name="李四").save(using=es, refresh=True)
            indexes = [Person._index._name, Article._index._name]
            total = Search(using=es, index=indexes).filter('term', name="李四").count()
            self.assertEqual(2, total)
        finally:
            es.indices.delete(index=Person._index._name, ignore=[400, 404])
            es.indices.delete(index=Article._index._name, ignore=[400, 404])

    def test_search_with_or_filter(self):
        Person(name="李四", age=15).save(using=es)
        Person(name="张三", age=18).save(using=es)
        Person._index.refresh(using=es)
        s = Search(using=es, index=Person._index._name).filter(
            Q("term", **{"name": "李四"}) & Q("term", **{"age": 15}) |
            Q("term", **{"name": "张三"}) & Q("term", **{"age": 18})
        )
        hits = s.execute().hits
        self.assertEqual(2, hits.total.value)

    def test_aggregate_with_same_level_buckets(self):
        Person(name="张三", age=15, create_time="2013-09-10 23:40:00").save(using=es)
        Person(name="李四", age=16, create_time="2013-10-10 23:40:00").save(using=es)
        Person(name="王五", age=17, create_time="2013-11-10 23:40:00").save(using=es)
        Person._index.refresh(using=es)

        res = Person.search(using=es).filter('term', name='李四').execute()
        self.assertEqual("李四", res.hits[0].name)

        # 下面三个聚合都是同级的
        s = Search(using=es, index=Person._index._name)
        s.aggs.bucket('per_name', 'terms', field="name", **{"size": 10000})
        s.aggs.bucket('per_age', 'terms', field="age", **{"size": 10000})
        s.aggs.bucket('per_create_time', 'terms', field="create_time", **{"size": 10000})
        res = s.execute().hits

        # terms(event_type) 是顶级的聚合，后面两个同为第二级聚合
        s = Search(using=es, index=Person._index._name)
        aggs = s.aggs.bucket("per_name", 'terms', field="name", **{"size": 10000})
        aggs.bucket("per_age", 'terms', field="age", **{"size": 10000})
        aggs.bucket("per_create_time", 'terms', field="create_time", **{"size": 10000})
        res = s.execute()


# curl -X DELETE "localhost:9200/test-suggest?pretty"

if __name__ == "__main__":
    # 启动测试
    unittest.main()
