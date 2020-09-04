# -*- coding: utf-8 -*-
from xenadmin.db.assets_manager.models import Company


class CompanyHelper(object):

    @staticmethod
    def get_id_to_name(db_session):
        ret = db_session.query(Company.id, Company.name).all()
        return {row.id: row.name for row in ret}
