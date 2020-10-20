package org.example.mr.provinceflow;

import java.util.HashMap;

import javax.security.auth.kerberos.KeyTab;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.mapreduce.Partitioner;

/**
 * K2  V2  对应的是map输出kv的类型
 *
 * @author
 */
public class ProvincePartitioner extends Partitioner<Text, FlowBean> {

    public static HashMap<String, Integer> ProvinceDict = new HashMap<String, Integer>();

    static {
        ProvinceDict.put("136", 0);
        ProvinceDict.put("137", 1);
        ProvinceDict.put("138", 2);
        ProvinceDict.put("139", 3);
    }


    @Override
    public int getPartition(Text key, FlowBean value, int numPartitions) {
        String prefix = key.toString().substring(0, 3);
        Integer provinceId = ProvinceDict.get(prefix);
        return provinceId == null ? 4 : provinceId;
    }


}
