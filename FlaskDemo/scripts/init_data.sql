
-- 添加用户
INSERT INTO "public"."user" ("id", "name", "age", "hobby", "desc","status") VALUES (1, '用户名',18, ARRAY['看书', '听音乐'], 'desc',  1);

-- 添加角色
INSERT INTO "public"."role" ("id", "name", "menu_ids", "user_id", "role_type","role_category") VALUES (1, '系统管理员','NULL', 0, 1,  1);


-- 增加测试菜单
INSERT INTO "public"."app_menu_perm" ("id", "pid", "name", "type", "status", "path") VALUES (10, 1, '一级菜单', '1', 1, 'NULL');
INSERT INTO "public"."app_menu_perm" ("id", "pid", "name", "type", "status", "path") VALUES (1001, 10, '二级菜单01', '2', 1, 'NULL');
INSERT INTO "public"."app_menu_perm" ("id", "pid", "name", "type", "status", "path") VALUES (1002, 10, '二级菜单02', '2', 1, 'NULL');
INSERT INTO "public"."app_menu_perm" ("id", "pid", "name", "type", "status", "path") VALUES (1003, 10, '二级菜单03', '2', 1, 'NULL');
INSERT INTO "public"."app_menu_perm" ("id", "pid", "name", "type", "status", "path") VALUES (100101, 1001, '三级菜单01', '3', 1, 'NULL');
INSERT INTO "public"."app_menu_perm" ("id", "pid", "name", "type", "status", "path") VALUES (100102, 1001, '三级菜单02', '3', 1, 'NULL');


-- 添加角色与权限对应关系
INSERT INTO "public"."user_role_perm" ("id", "role_id", "node_permission", "data_permission", "user_id") VALUES (10, 1, '10', 'NULL',  0);
INSERT INTO "public"."user_role_perm" ("id", "role_id", "node_permission", "data_permission", "user_id") VALUES (1001, 1, '1001', 'NULL',  0);
INSERT INTO "public"."user_role_perm" ("id", "role_id", "node_permission", "data_permission", "user_id") VALUES (1002, 1, '1002', 'NULL',  0);
INSERT INTO "public"."user_role_perm" ("id", "role_id", "node_permission", "data_permission", "user_id") VALUES (1003, 1, '1003', 'NULL',  0);
INSERT INTO "public"."user_role_perm" ("id", "role_id", "node_permission", "data_permission", "user_id") VALUES (100101, 1, '100101', 'NULL',  0);
INSERT INTO "public"."user_role_perm" ("id", "role_id", "node_permission", "data_permission", "user_id") VALUES (100102, 1, '100102', 'NULL',  0);