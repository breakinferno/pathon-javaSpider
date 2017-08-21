package com.cli.ui;

import java.io.BufferedReader;
import java.io.InputStreamReader;

public class SpiderController {
	
	//根据传入的关键字，启动公众号爬虫（正式版本爬虫路径需要修改，仅测试使用）
	/*public static void main(String[] args) {
		SpiderController spiderController = new SpiderController();
		spiderController.spiderGZH("寿险");
	}*/

	public boolean spiderGZH(String keyword){
		
		System.out.println("Start");
		
		GZHThread gt = new GZHThread();
		gt.setKeyword(keyword);
		Thread t = new Thread(gt);
		t.start();
		/*try {
			System.out.println("start");
			String[] arg = new String[] { "python", "E:\\Internship\\pythonSpiders\\version2.0\\spider_2\\gzhspider.py", keyword };
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
		}*/
		System.out.println("End");
		return true;
	}
	
	//根据传入的关键字，启动公众号文章爬虫（正式版本爬虫路径需要修改，仅测试使用）

	public boolean spiderArticle(String keyword){
		
		System.out.println("Start");
		
		ArticleThread at = new ArticleThread();
		at.setKeyword(keyword);
		Thread t = new Thread(at);
		t.start();
		
		/*try {
			System.out.println("start");
			String[] arg = new String[] { "python", "E:\\Internship\\pythonSpiders\\version2.0\\spider_2\\articlespider.py", keyword };
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
		}*/
		System.out.println("End");
		
		return true;
	}

}

/**
 * 公众号爬虫的一个线程
 * @author gaoyue
 * 上午8:57:58
 */
class GZHThread implements Runnable{

	String keyword;
	
	public void setKeyword(String keyword){
		this.keyword = keyword;
	}
	
	@Override
	public void run() {
		// TODO Auto-generated method stub
		try {
			String[] arg = new String[] { "python", "E:\\Internship\\pythonSpiders\\version2\\spider_2\\gzhspider.py", keyword };
			Process pr=Runtime.getRuntime().exec(arg);
			System.out.println("开始执行");
			BufferedReader in= new BufferedReader(new InputStreamReader(pr.getInputStream()));
			String line;
			while((line=in.readLine())!=null){
				System.out.println(line);
			}
			in.close();
			pr.waitFor();
			System.out.println("执行结束");
		} catch (Exception e) {
			// TODO: handle exception
			e.printStackTrace();
		}
	}
	
}

/**
 * 文章爬虫的一个线程
 * @author gaoyue
 * 上午8:58:34
 */
class ArticleThread implements Runnable{

	String keyword;
	
	public void setKeyword(String keyword){
		this.keyword = keyword;
	}
	
	@Override
	public void run() {
		// TODO Auto-generated method stub
		try {
			String[] arg = new String[] { "python", "E:\\Internship\\pythonSpiders\\version2\\spider_2\\articlespider.py", keyword };
			Process pr=Runtime.getRuntime().exec(arg);
			BufferedReader in= new BufferedReader(new InputStreamReader(pr.getInputStream()));
			String line;
			while((line=in.readLine())!=null){
				System.out.println(line);
			}
			in.close();
			pr.waitFor();
		} catch (Exception e) {
			// TODO: handle exception
			e.printStackTrace();
		}
	}
	
}

