# coding=utf-8
import json
import os
import unittest
from FlaskDemo.apps import create_app

app = create_app()
app.secret_key = os.urandom(24)


class ProtectCheckSituationTest(unittest.TestCase):
    """构造单元测试案例"""

    def setUp(self):
        app.testing = True
        app.app_context().push()
        self.client = app.test_client()

    def tearDown(self):
        "Hook method for deconstructing the test fixture after testing it."
        pass

    def test_base_assets_d_update_insert(self):
        """测试用户名和密码为空的情况"""
        # 模拟客户端发送请求，返回响应对象
        ret = self.client.post("/situation/assets_manager/service/base_assets_d_update_insert", data={})
        # 获取响应体的数据（是json）
        resp = ret.data
        resp = json.loads(resp)
        # 断言
        self.assertIn("code", resp)
        self.assertEqual(resp["code"], 1)

    def test_service_charts_count_assets_info(self):
        """测试资产概况计数"""
        ret = self.client.get("/situation/assets_manager/service/charts?c_type=count_assets_info", data={})
        # 获取响应体的数据（是json）
        resp = ret.data
        resp = json.loads(resp)
        # 断言
        self.assertIn("code", resp)

    def test_service_charts_count_found_dev_by_type(self):
        """测试资产概况计数"""
        ret = self.client.get("/situation/assets_manager/service/charts?c_type=count_found_dev_by_type", data={})
        # 获取响应体的数据（是json）
        resp = ret.data
        resp = json.loads(resp)
        # 断言
        self.assertIn("code", resp)

    def test_assets_type_data_count(self):
        """测试资产概况计数"""
        ret = self.client.get("/situation/assets_manager/service/assets_type_data_count?asset_type=3&data_source=1",
                              data={})
        # 获取响应体的数据（是json）
        resp = ret.data
        resp = json.loads(resp)
        # 断言
        self.assertIn("code", resp)

    def test_assets_type_data_count(self):
        """资源管理/设备资产"""
        ret = self.client.get("/situation/assets_manager/service/assets_type_data_count?asset_type=3&data_source=1",
                              data={})
        # 获取响应体的数据（是json）
        resp = ret.data
        resp = json.loads(resp)
        # 断言
        self.assertIn("code", resp)

    # def test_wrong_username_password(self):
    #     """测试用户名获密码错误的情况"""
    #     # 模拟客户端发送请求，返回响应对象
    #     ret = self.client.post("/login", data={
    #         "username": "admin",
    #         "password": "abc"
    #     })
    #     # 获取响应体的数据（是json）
    #     resp = ret.data
    #     resp = json.loads(resp)
    #     # 断言
    #     self.assertIn("code", resp)
    #     self.assertEqual(resp["code"], 2)
    #
    # def test_login_sucess(self):
    #     """测试登录成功的情况"""
    #     # 模拟客户端发送请求，返回响应对象
    #     ret = self.client.post("/login", data={
    #         "username": "admin",
    #         "password": "python"
    #     })
    #     # 获取响应体的数据（是json）
    #     resp = ret.data
    #     resp = json.loads(resp)
    #     # 断言
    #     self.assertIn("code", resp)
    #     self.assertEqual(resp["code"], 0)


if __name__ == "__main__":
    # 启动测试
    unittest.main()
