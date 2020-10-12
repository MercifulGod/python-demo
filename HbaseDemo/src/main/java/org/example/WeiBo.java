package org.example;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.*;
import org.apache.hadoop.hbase.client.*;
import org.apache.hadoop.hbase.filter.CompareFilter;
import org.apache.hadoop.hbase.filter.RowFilter;
import org.apache.hadoop.hbase.filter.SubstringComparator;
import org.apache.hadoop.hbase.io.compress.Compression;
import org.apache.hadoop.hbase.regionserver.ScannerContext;
import org.apache.hadoop.hbase.util.Bytes;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

public class WeiBo {
    private Configuration conf = HBaseConfiguration.create();
    private static final byte[] TABLE_CONTENT = Bytes.toBytes("weibo:content");
    private static final byte[] TABLE_RELATIONS = Bytes.toBytes("weibo:relations");
    private static final byte[] TABLE_RECEIVE_CONTENT_EMAIL = Bytes.toBytes("weibo:receive_content_email");


    public void initTable() {
        initNamespace();
        createTableContent();
        createTableRelations();
        createTableReceiveContentEmail();
    }

    public void initNamespace() {
        HBaseAdmin admin = null;
        try {
            admin = new HBaseAdmin(conf);
            NamespaceDescriptor weibo = NamespaceDescriptor
                    .create("weibo")
                    .addConfiguration("creator", "Jinji")
                    .addConfiguration("create_time", System.currentTimeMillis() + "")
                    .build();
            admin.createNamespace(weibo);
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (null != admin) {
                try {
                    admin.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }

    }


    /**
     * 创建微博内容表
     * Table Name:weibo:content
     * RowKey: 用户ID_时间戳
     * ColumnFamily:info
     * ColumnLabel:标题 内容 图标URL
     * Version: 1个版本
     */
    public void createTableContent() {
        HBaseAdmin admin = null;
        try {
            admin = new HBaseAdmin(conf);
            //创建表描述
            HTableDescriptor content = new HTableDescriptor(TableName.valueOf(TABLE_CONTENT));
            //创建列族标书
            HColumnDescriptor info = new HColumnDescriptor(Bytes.toBytes("info"));
            //黄建块缓存
            info.setBlockCacheEnabled(true);
            //黄建块缓存大小
            info.setBlocksize(2097152);
            //设置压缩方式
            info.setCompressionType(Compression.Algorithm.BZIP2);
            //设置版本边界
            info.setMaxVersions(1);
            info.setMinVersions(1);
            content.addFamily(info);
            admin.createTable(content);
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (null != admin) {
                try {
                    admin.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    /**
     * 创建微博关系表
     * Table Name:weibo:content
     * RowKey: 用户ID
     * ColumnFamily:attends,fans
     * ColumnLabel:关注用户ID、粉丝用户ID
     * ColumnValue:用户ID
     * Version: 1个版本
     */
    public void createTableRelations() {
        HBaseAdmin admin = null;
        try {
            admin = new HBaseAdmin(conf);
            //创建表描述
            HTableDescriptor relations = new HTableDescriptor(TableName.valueOf(TABLE_RELATIONS));
            //创建列族标书
            HColumnDescriptor attends = new HColumnDescriptor(Bytes.toBytes("attends"));
            //黄建块缓存
            attends.setBlockCacheEnabled(true);
            //黄建块缓存大小
            attends.setBlocksize(2097152);
            //设置压缩方式
            attends.setCompressionType(Compression.Algorithm.BZIP2);
            //设置版本边界
            attends.setMaxVersions(1);
            attends.setMinVersions(1);

            HColumnDescriptor fans = new HColumnDescriptor(Bytes.toBytes("fans"));
            //黄建块缓存
            fans.setBlockCacheEnabled(true);
            //黄建块缓存大小
            fans.setBlocksize(2097152);
            //设置压缩方式
            fans.setCompressionType(Compression.Algorithm.BZIP2);
            //设置版本边界
            fans.setMaxVersions(1);
            fans.setMinVersions(1);

            relations.addFamily(attends);
            relations.addFamily(fans);
            admin.createTable(relations);
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (null != admin) {
                try {
                    admin.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    /**
     * 创建微博收件箱表
     * Table Name:weibo:receive_content_email
     * RowKey: 用户ID
     * ColumnFamily:info
     * ColumnLabel:用户ID-发布微博的人的用户ID
     * ColumnValue:关注的人的微博的RowKey
     * Version: 1000
     */
    public void createTableReceiveContentEmail() {
        HBaseAdmin admin = null;
        try {
            admin = new HBaseAdmin(conf);
            //创建表描述
            HTableDescriptor receiveContentEmail = new HTableDescriptor(TableName.valueOf(TABLE_RECEIVE_CONTENT_EMAIL));
            //创建列族标书
            HColumnDescriptor info = new HColumnDescriptor(Bytes.toBytes("info"));
            //黄建块缓存
            info.setBlockCacheEnabled(true);
            //黄建块缓存大小
            info.setBlocksize(2097152);
            //设置压缩方式
            info.setCompressionType(Compression.Algorithm.BZIP2);
            //设置版本边界
            info.setMaxVersions(1);
            info.setMinVersions(1);

            receiveContentEmail.addFamily(info);
            admin.createTable(receiveContentEmail);
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (null != admin) {
                try {
                    admin.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    /**
     * 发布微博
     * a. 微博内容中数据+1
     * b. 向微博收件箱表中加入微博的RowKey
     */
    public void publishContent(String uid, String content) {
        HConnection connection = null;
        try {
            connection = HConnectionManager.createConnection(conf);
            // a.微博内容添加1条数据，首先获取微博内容表描述
            HTableInterface contentTBL = connection.getTable(TableName.valueOf(TABLE_CONTENT));
            // 组装RowKey
            long timestamp = System.currentTimeMillis();
            String rowKey = uid + "_" + timestamp;

            Put put = new Put(Bytes.toBytes(rowKey));
            put.add(Bytes.toBytes("info"), Bytes.toBytes("content"), timestamp, Bytes.toBytes(content));
            contentTBL.put(put);

            // b. 向微博收件箱中加入发布的RowKey
            // b.1. 查询用户表关系，得到当前用户有那些烦死
            HTableInterface relationsTBL = connection.getTable(TableName.valueOf(TABLE_RELATIONS));
            // b.2 去除目标数据
            Get get = new Get(Bytes.toBytes(uid));
            get.addFamily(Bytes.toBytes("fans"));

            Result result = relationsTBL.get(get);
            List<byte[]> fans = new ArrayList<byte[]>();
            // 遍历去除当前发布微博的用户的所有粉丝数据
            for (Cell cell : result.rawCells()) {
                fans.add(CellUtil.cloneQualifier(cell));
            }
            // 如果该用户没有粉丝，则直接return
            if (fans.size() <= 0) return;

            // 开始操作收件箱
            HTableInterface recTBL = connection.getTable(TableName.valueOf(TABLE_RECEIVE_CONTENT_EMAIL));
            List<Put> puts = new ArrayList<Put>();
            for (byte[] fan : fans) {
                Put fanPut = new Put(fan);
                fanPut.add(Bytes.toBytes("info"), Bytes.toBytes(uid), timestamp, Bytes.toBytes(rowKey));
                puts.add(fanPut);
            }
            recTBL.put(puts);
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (null != connection) {
                try {
                    connection.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    /**
     * 添加关注用户
     * a. 在微博用户关系表中，对当前主动操作的用户添加新的关注的好友
     * b. 在微博用户关系表中，对被关注的用户添加粉丝（当前操作的用户）
     * c. 当前操作用户的微博收件箱添加所关注的用户发布的微博rowKey
     */
    public void addAttends(String uid, String... attends) {
        if (attends == null || attends.length <= 0 || uid == null || uid.length() <= 0) {
            return;
        }
        HConnection connection = null;
        try {
            connection = HConnectionManager.createConnection(conf);
            // 用户关系表操作对象（连接到用户关系表）
            HTableInterface relationsTBL = connection.getTable(TableName.valueOf(TABLE_RELATIONS));
            List<Put> puts = new ArrayList<Put>();
            // a. 在微博用户关系表中，添加新关注的好友
            Put attendPut = new Put(Bytes.toBytes(uid));
            for (String attend : attends) {
                // 为当前用户添加关注的人
                attendPut.add(Bytes.toBytes("attends"), Bytes.toBytes(attend), Bytes.toBytes(attend));
                // b. 为被关注的人，添加粉丝
                Put fansPut = new Put(Bytes.toBytes(attend));
                fansPut.add(Bytes.toBytes("fans"), Bytes.toBytes(uid), Bytes.toBytes(uid));
                // 将所有关注的人一个一个的添加到puts(List) 集合
                puts.add(fansPut);
            }
            puts.add(attendPut);
            relationsTBL.put(puts);


            // c.1 微博收件箱添加关注的用户发布的微博内容的(content)的rowKey
            HTableInterface contentTBL = connection.getTable(TableName.valueOf(TABLE_CONTENT));
            Scan scan = new Scan();
            // 用于存放取出来的关注的人所发布的微博的rowKey
            List<byte[]> rowKeys = new ArrayList<>();
            for (String attend : attends) {
                // 过滤扫描rowKey， 即：前置位匹配被关注的人的uid
                RowFilter filter = new RowFilter(CompareFilter.CompareOp.EQUAL, new SubstringComparator(attend + "_"));
                // 为扫描对象指定过滤规则
                scan.setFilter(filter);
                // 通过扫描对象得到scanner
                ResultScanner result = contentTBL.getScanner(scan);
                // 迭代器遍历扫描出来的结果集
                Iterator<Result> iterator = result.iterator();
                while (iterator.hasNext()) {
                    // 取出每一个符合扫描结果的哪一行数据
                    Result r = iterator.next();
                    for (Cell cell : r.rawCells()) {
                        // 将得到的rowKey放置于集合容器中
                        rowKeys.add(CellUtil.cloneRow(cell));
                    }
                }
            }

            if (rowKeys.size() <= 0) return;


            // 得到微博收件箱表的操作对象
            HTableInterface recTBL = connection.getTable(TableName.valueOf(TABLE_RECEIVE_CONTENT_EMAIL));
            // 用于存放多个关注的用户的发布的多条微博rowKey信息
            List<Put> recPuts = new ArrayList<Put>();
            for (byte[] rk : rowKeys) {
                Put put = new Put(Bytes.toBytes(uid));
                String rowKey = Bytes.toString(rk);
                // 截取UID
                String attendUID = rowKey.substring(0, rowKey.indexOf("_"));
                long timestamp = Long.parseLong(rowKey.substring(rowKey.indexOf("_") + 1));
                // 将微博rowKey添加到指定单元格中
                put.add(Bytes.toBytes("info"), Bytes.toBytes(attendUID), timestamp, rk);
                recPuts.add(put);
            }
            recTBL.put(recPuts);
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (null != connection) {
                try {
                    connection.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    /**
     * 移除（取关）用户
     * a. 在微博用户关系表中，对当前主动操作的用户移除取关的好友
     * b. 在微博用户关系表中，对被取消关注的用户删除粉丝（当前操作的用户）
     * c. 从收件箱中删除取注的用户微博的rowKey
     */
    public void removeAttends(String uid, String... attends) {
        if (attends == null || attends.length <= 0 || uid == null || uid.length() <= 0) {
            return;
        }
        HConnection connection = null;
        try {
            connection = HConnectionManager.createConnection(conf);
            // 在微博用户关系表中，删除已关注的好友
            HTableInterface relationsTBL = connection.getTable(TableName.valueOf(TABLE_RELATIONS));
            // 待删除的用户关系表中的所有数据
            List<Delete> deletes = new ArrayList<>();
            // 当前取关操作者的uid对应的Delete对象
            Delete attendDelete = new Delete(Bytes.toBytes(uid));
            //遍历取关，同时每次取关都要被取关的人的粉丝-1
            for (String attend : attends) {
                attendDelete.deleteColumn(Bytes.toBytes("attends"), Bytes.toBytes(attend));
                Delete fansDelete = new Delete(Bytes.toBytes(attend));
                fansDelete.deleteColumn(Bytes.toBytes("fans"), Bytes.toBytes(uid));
                deletes.add(fansDelete);
            }
            deletes.add(attendDelete);
            relationsTBL.delete(deletes);

            //删除取关的人的微博rowKey从收件箱表中
            HTableInterface recTBL = connection.getTable(TableName.valueOf(TABLE_RECEIVE_CONTENT_EMAIL));

            Delete recDelete = new Delete(Bytes.toBytes(uid));
            for (String attend : attends) {
                recDelete.deleteColumn(Bytes.toBytes("info"), Bytes.toBytes(attend));

            }
            recTBL.delete(recDelete);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    /**
     * 获取微博实际内容
     * a. 从微博收件箱中获取所关注的用户的发布的微博RowKey
     * b. 根据获取的RowKey去微博内容表中得到微博内容
     * c. 将得到的数据封装到Message对象中
     */
    public List<Message> getAttendsContent(String uid) {
        HConnection connection = null;
        try {
            connection = HConnectionManager.createConnection(conf);

            HTableInterface recTBL = connection.getTable(TableName.valueOf(TABLE_RECEIVE_CONTENT_EMAIL));
            // 从收件箱中获得微博的rowKey
            Get get = new Get(Bytes.toBytes(uid));
            // 设置最大版本号
            get.setMaxVersions(5);
            List<byte[]> rowKeys = new ArrayList<byte[]>();
            Result result = recTBL.get(get);
            for (Cell cell : result.rawCells()) {
                rowKeys.add(CellUtil.cloneValue(cell));
            }
            // 根据去除的所有rowKey去微博内容表中检索数据
            HTableInterface contentTBL = connection.getTable(TableName.valueOf(TABLE_CONTENT));
            // 根据rowKey去除对应微博的具体内容
            List<Get> gets = new ArrayList<>();
            for (byte[] rk : rowKeys) {
                Get g = new Get(rk);
                gets.add(g);
            }
            //得到所有的微博内容的result对象
            Result[] results = contentTBL.get(gets);

            List<Message> messages = new ArrayList<>();
            for (Result res : results) {
                for (Cell cell : res.rawCells()) {
                    Message message = new Message();
                    String rowKey = Bytes.toString(CellUtil.cloneRow(cell));

                    String userid = rowKey.substring(rowKey.indexOf("_"));
                    String timestamp = rowKey.substring(rowKey.indexOf("_") + 1);
                    String content = Bytes.toString(CellUtil.cloneValue(cell));
                    message.setContent(content);
                    message.setTimestamp(timestamp);
                    message.setUid(userid);

                    messages.add(message);

                }
            }
            return messages;
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            try {
                connection.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        return null;
    }

    // 测试发布内容
    public void testPublishContent(WeiBo wb) {
        wb.publishContent("0001", "今天买了一包空气，送了点薯片，非常开心");
        wb.publishContent("0001", "今天天气不错");
    }

    // 测试添加关注
    public void testAddAttend(WeiBo wb) {
        wb.publishContent("0008", "准备下课");
        wb.publishContent("0009", "准备关机");
        wb.addAttends("0001", "0008", "0009");
    }

    /**
     * 测试取消关注
     */
    public void testRemoveAttends(WeiBo wb) {
        wb.removeAttends("0001", "0008");
    }

    /**
     * 测试展示内容
     */
    public void testShowMessage(WeiBo wb) {
        List<Message> messages = wb.getAttendsContent("0001");
        for (Message message : messages) {
            System.out.println(message);
        }
    }

    public static void main(String[] args) {
        WeiBo weiBo = new WeiBo();
//        weiBo.initTable();

        weiBo.testPublishContent(weiBo);
        weiBo.testAddAttend(weiBo);
        weiBo.testShowMessage(weiBo);
        weiBo.testRemoveAttends(weiBo);
        weiBo.testShowMessage(weiBo);
    }
}
