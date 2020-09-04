from tornado.web import url
from apps.user import views

urlpatterns = [
    url("/api/v1/user/add", views.AddUser),
    # url("/api/v1/user/delete", views.DeleteUser),
    url("/api/v1/user/update", views.UpdateUser),
    # url("/api/v1/user/list", views.ListUser),
    # url("/api/v1/user/info", views.InfoUser),
    # url("/api/v1/user/enable", views.EnableUser),
    # url("/api/v1/user/disable", views.DisableUser),
    #
    # url("/api/v1/user/login", views.Login),
    # url("/api/v1/user/password/update", views.PasswordUpdate),
    #
    # url("/api/v1/sys/role/add", views.AddRole),
    # url("/api/v1/sys/role/delete", views.DeleteRole),
    # url("/api/v1/sys/role/update", views.UpdateRole),
    # url("/api/v1/sys/role/list", views.ListRole),
    # url("/api/v1/sys/role/enable", views.EnableRole),
    # url("/api/v1/sys/role/disable", views.DisableRole),
    #
    # # 系统路由权限
    # url("/api/v1/sys/menu/add", views.AddPermission),
    # url("/api/v1/sys/menu/delete", views.DeletePermission),
    # url("/api/v1/sys/menu/update", views.UpdatePermission),
    # url("/api/v1/sys/menu/list", views.ListPermission),
    #
    # # 系统资源权限
    # url("/api/v1/sys/resource/add", views.AddResource),
    # url("/api/v1/sys/resource/delete", views.DeleteResource),
    # url("/api/v1/sys/resource/update", views.UpdateResource),
    # url("/api/v1/sys/resource/list", views.ListResource),
]
