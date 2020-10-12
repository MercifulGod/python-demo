package org.example;

import java.io.File;
import java.io.IOException;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class WordCountDriver {
    public static void main(String[] args) throws IOException, ClassNotFoundException, InterruptedException {
        //1获取配置信息以及封装任务
        Configuration configuration = new Configuration();
        Job job = Job.getInstance(configuration);
        //2设置jar加载路径
        job.setJarByClass(WordCountDriver.class);
        //3设置map和reduce类
        job.setMapperClass(WordCountMapper.class);
        job.setReducerClass(WordCountReducer.class);
        //4设置map输出
        job.setMapOutputKeyClass(Text.class);
        job.setMapOutputValueClass(IntWritable.class);
        //5设置最终输出kv类型
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);

        //6设置输入和输出路径 (本地测试)
        File input = new File("src/main/resources/input");
        File output = new File("src/main/resources/output");
        FileInputFormat.setInputPaths(job, new Path(input.getAbsolutePath()));
        FileOutputFormat.setOutputPath(job, new Path(output.getAbsolutePath()));
        // (集群测试)
//        FileInputFormat.setInputPaths(job, new Path(args[0]));
//        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        //7提交
        boolean result = job.waitForCompletion(true);
        System.exit(result ? 0 : 1);
    }
}