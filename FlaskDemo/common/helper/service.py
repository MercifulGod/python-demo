import logging

from flask import g
from sqlalchemy import func


class CommonService(object):
    """
    公共方法类
    """

    @staticmethod
    def add_record(model_table=None, record=None):
        """
        新增信息
        :param model_table 模型类
        :param record: 记录字典
        """
        db_session = g.pg_db
        try:
            obj = model_table()
            for key, value in record.items():
                if key is not None:
                    setattr(obj, key, value)
            obj = db_session.merge(obj)
            db_session.commit()
            return obj
        except Exception as e:
            db_session.rollback()
            logging.error("添加记录失败：{}".format(e))
            raise e

    @staticmethod
    def add_records(table_name=None, records=None):
        """
        批量添加
        :param table_name:
        :param records:
        :return:
        """
        db_session = g.pg_db
        try:
            db_session.bulk_insert_mappings(table_name, records)
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            raise e

    @staticmethod
    def bulk_add_record(table_name=None, records=None):
        """批量添加用户
         :param table_name:
        :param records: []
        """
        try:
            db_session = g.pg_db
            assess_tasks = []
            table_labels = [item for item in table_name.__dict__.keys() if not item.startswith('_')]
            table_labels.remove('id')
            for item in records:
                obj = table_name()
                for key in table_labels:
                    setattr(obj, key, item.get(key, None))
                assess_tasks.append(obj)
            db_session.add_all(assess_tasks)
            db_session.commit()
        except Exception as e:
            g.pg_db.rollback()
            raise e

    @staticmethod
    def save_by_obj(obj=None):
        """
        更新信息
        :param obj: 数据对象
        """
        db_session = g.pg_db
        try:
            obj = db_session.merge(obj)
            db_session.commit()
            return obj
        except Exception as e:
            db_session.rollback()
            logging.error("更新记录失败：{}".format(e))
            raise e

    @staticmethod
    def del_by_ids(table_name=None, ids=None):
        """
        根据id批量删除对象
        :param table_name:
        :param ids:
        :return:
        """
        if not ids:
            return
        db_session = g.pg_db
        try:
            db_session.query(table_name).filter(getattr(table_name, "id").in_(ids)).delete(synchronize_session=False)
            db_session.commit()
        except Exception as e:
            raise e

    @staticmethod
    def update_by_obj(obj=None, record=None):
        """
        更新信息
        :param obj: 数据对象
        :param record: 记录详情
        """
        db_session = g.pg_db
        try:
            for key, value in record.items():
                if key is not None:
                    setattr(obj, key, value)
            db_session.merge(obj)
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            logging.error("更新记录失败：{}".format(e))
            raise e

    @staticmethod
    def update_by_attrs(table_name=None, filters=None, param=None):
        db_session = g.pg_db
        try:
            db_session.query(table_name).filter(*filters).update(param, synchronize_session=False)
            db_session.commit()
        except Exception as e:
            db_session.rollback()
            raise e

    @staticmethod
    def get_by_id(table_name=None, id_=None):
        """
        通过ID获取对象
        :param table_name:
        :param id_:
        :return:
        """
        db_session = g.pg_db
        try:
            obj = db_session.query(table_name).filter(getattr(table_name, "id") == id_).first()
            return obj
        except Exception as e:
            raise e

    @staticmethod
    def list_by_filter(table_name=None, filters=None, params=None):
        db_session = g.pg_db
        total = db_session.query(func.count(table_name.id)).filter(*filters).scalar()
        page = int(params.get("page", 1))
        size = int(params.get("size", 10))
        if (page - 1) * size >= total and page > 1:
            page -= 1
        query = db_session.query(table_name).filter(*filters)
        if "order_by" in params:
            query = query.order_by(params.get("order_by"))
        instances = query.offset((page - 1) * size).limit(size).all()
        ret = [item.to_dict() for item in instances]
        return {"page": page, "size": size, "data": ret, "total": total}

    @staticmethod
    def list_select_by_filter(select=None, filters=None):
        db_session = g.pg_db
        objs = db_session.query(*select).filter(*filters).all()
        objs = [item._asdict() for item in objs]
        return objs
