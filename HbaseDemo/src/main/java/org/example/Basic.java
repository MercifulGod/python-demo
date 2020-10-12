package org.example;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.*;
import org.apache.hadoop.hbase.client.*;
import org.apache.hadoop.hbase.util.Bytes;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

/**
 * Hello world!
 */
public class Basic {
    public static Configuration conf;

    //获取Configuration对象
    static {
        conf = HBaseConfiguration.create();
        conf.set("hbase.zookeeper.quorum", "127.0.0.1");
        conf.set("hbase.zookeeper.property.clientPort", "2181");
    }

    /**
     * 判断表是否存在
     */
    public static boolean isTableExist(String tableName) throws IOException {
        //　在Hbase中管理、访问表需要先创建HBaseAdmin对象
        HBaseAdmin admin = new HBaseAdmin(conf);
        return admin.tableExists(tableName);
    }

    /**
     * 创建表
     */
    public static void createTable(String tableName, String... columnFamily) throws IOException {
        //　在Hbase中管理、访问表需要先创建HBaseAdmin对象
        HBaseAdmin admin = new HBaseAdmin(conf);
        if (isTableExist(tableName)) {
            System.out.println("表" + tableName + "已存在");
        } else {
            //　创建表属性对象，表名需要转字节
            HTableDescriptor descriptor = new HTableDescriptor(TableName.valueOf(tableName));
            //创建多个列族
            for (String cf : columnFamily) {
                descriptor.addFamily(new HColumnDescriptor(cf));
            }
            //　根据对表的配置，创建表
            admin.createTable(descriptor);
            System.out.println("表" + tableName + "已存在");
        }
    }

    /**
     * 删除表
     */
    public static void dropTable(String tableName, String... columnFamily) throws IOException {
        //　在Hbase中管理、访问表需要先创建HBaseAdmin对象
        HBaseAdmin admin = new HBaseAdmin(conf);
        if (isTableExist(tableName)) {
            admin.disableTable(tableName);
            admin.deleteTable(tableName);
            System.out.println("表" + tableName + "删除成功");
        } else {
            System.out.println("表" + tableName + "不存在");
        }
    }

    /**
     * 向表中插入数据
     */
    public static void addRowData(String tableName, String rowKey, String columnFamily, String column, String value) throws IOException {
        // 创建HTable对象
        HTable hTable = new HTable(conf, tableName);
        // 向表中插入數據
        Put put = new Put(Bytes.toBytes(rowKey));
        // 向put對象中组装对象
        put.add(Bytes.toBytes(columnFamily), Bytes.toBytes(column), Bytes.toBytes(value));
        hTable.put(put);
        hTable.close();
        System.out.println("插入数据成功");
    }

    /**
     * 删除多行数据
     */
    public static void deleteMultiRow(String tableName, String... rows) throws IOException {
        HTable hTable = new HTable(conf, tableName);
        List<Delete> deleteList = new ArrayList<Delete>();
        for (String row : rows) {
            Delete delete = new Delete(Bytes.toBytes(row));
            deleteList.add(delete);
        }
        hTable.delete(deleteList);
        hTable.close();
    }

    /**
     * 获取所有数据
     */
    public static void getAllRows(String tableName) throws IOException {
        HTable hTable = new HTable(conf, tableName);
        //得到用于扫描Region的对象
        Scan scan = new Scan();
        // 使用HTable得到resultScanner实现类的对象
        ResultScanner resultScanner = hTable.getScanner(scan);
        for (Result result : resultScanner) {
            Cell[] cells = result.rawCells();
            for (Cell cell : cells) {
                //得到rowKey
                System.out.println("行健" + Bytes.toString(CellUtil.cloneRow(cell)));
                System.out.println("列族" + Bytes.toString(CellUtil.cloneFamily(cell)));
                System.out.println("行健" + Bytes.toString(CellUtil.cloneQualifier(cell)));
                System.out.println("行健" + Bytes.toString(CellUtil.cloneValue(cell)));
            }
        }
    }

    /**
     * 获取某一行数据
     */
    public static void getRow(String tableName, String rowKey) throws IOException {
        HTable hTable = new HTable(conf, tableName);
        Get get = new Get(Bytes.toBytes(rowKey));
//        get.setMaxVersions(); 显示所有版本
//        get.setTimeStamp(); 显示指定时间戳的版本
        Result result = hTable.get(get);
        for (Cell cell : result.rawCells()) {
            //得到rowKey
            System.out.println("行健" + Bytes.toString(CellUtil.cloneRow(cell)));
            System.out.println("列族" + Bytes.toString(CellUtil.cloneFamily(cell)));
            System.out.println("行健" + Bytes.toString(CellUtil.cloneQualifier(cell)));
            System.out.println("行健" + Bytes.toString(CellUtil.cloneValue(cell)));
        }
    }

    /**
     * 获取某一行指定“列族：列”的数据
     */
    public static void getRowQualifier(String tableName, String rowKey, String family, String qualifier) throws IOException {
        HTable hTable = new HTable(conf, tableName);
        Get get = new Get(Bytes.toBytes(rowKey));
        get.addColumn(Bytes.toBytes(family), Bytes.toBytes(qualifier));
        Result result = hTable.get(get);
        for (Cell cell : result.rawCells()) {
            //得到rowKey
            System.out.println("行健" + Bytes.toString(CellUtil.cloneRow(cell)));
            System.out.println("列族" + Bytes.toString(CellUtil.cloneFamily(cell)));
            System.out.println("行健" + Bytes.toString(CellUtil.cloneQualifier(cell)));
            System.out.println("行健" + Bytes.toString(CellUtil.cloneValue(cell)));
        }
    }

    public static void main(String[] args) {

        try {
            System.out.println("##################################################################");
            System.out.println("表是否存在:" + isTableExist("HbaseDemo"));
            System.out.println("##################创建表################################################");
            createTable("HbaseDemo", "info");
            System.out.println("##################添加数据################################################");
            addRowData("HbaseDemo", "0001", "info", "name", "Tom");
            System.out.println("###################获取单个数据###############################################");
            getRow("HbaseDemo", "0001");
            System.out.println("###################删除表###############################################");
            dropTable("HbaseDemo", "info");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
