# -*- coding: utf-8 -*-

USER_STATUS = {
    "0": "禁用",
    "1": "启用",
    "9": "删除",
}
USER_STATUS_RE = {v: k for k, v in USER_STATUS.items()}

MENU_TYPE = {
    "1": "一级菜单",
    "2": "二级菜单",
    "3": "三级菜单",
}
MENU_TYPE_RE = {v: k for k, v in MENU_TYPE.items()}

PASSWORD_ROLE = {
    "num_val": 1, "warn_day": 5, "handle": 1, "lowercase_val": 1, "failure_logon": 5,
    "latest_psw_count": 1, "special_details": "!@#$%^&*()/_+=-", "len_max": 15, "lowercase_len": 0,
    "capital_val": 1, "valid_day": 90, "capital_len": 0, "len_min": 6, "special_len": 0, "special_val": 1
}
