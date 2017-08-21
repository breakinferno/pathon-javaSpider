package com.cli.ui;

import java.io.BufferedReader;
import java.io.InputStreamReader;

public class UpdateURL {
	
	//更新某一篇文章的URL
	public boolean updateArticleURL(Integer articleId){
		
		try {
			System.out.println("start");
			String[] arg = new String[] { "python", "E:\\Internship\\pythonSpiders\\version2\\spider_2\\clickUpdateArticleURL.py", String.valueOf(articleId)};
			Process pr=Runtime.getRuntime().exec(arg);
			BufferedReader in= new BufferedReader(new InputStreamReader(pr.getInputStream()));
			String line;
			while((line=in.readLine())!=null){
				System.out.println(line);
			}
			in.close();
			pr.waitFor();
			System.out.println("end");
		} catch (Exception e) {
			// TODO: handle exception
			e.printStackTrace();
			return false;
		}
		
		return true;
	}
	

	public boolean updateGZHURL(String wx_num){
		
		try {
			System.out.println("start");
			String[] arg = new String[] { "python", "E:\\Internship\\pythonSpiders\\version2\\spider_2\\clickUpdateGzhURL.py", wx_num };
			Process pr=Runtime.getRuntime().exec(arg);
			BufferedReader in= new BufferedReader(new InputStreamReader(pr.getInputStream()));
			String line;
			while((line=in.readLine())!=null){
				System.out.println(line);
			}
			in.close();
			pr.waitFor();
			System.out.println("end");
		} catch (Exception e) {
			// TODO: handle exception
			e.printStackTrace();
			return false;
		}
		
		return true;
	}

}
