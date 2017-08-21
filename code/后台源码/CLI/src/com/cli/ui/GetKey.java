package com.cli.ui;

import java.util.ArrayList;

import com.cli.bean.IndexDto;
import com.cli.service.impl.ArticleServiceImpl;
import com.cli.service.impl.WxNumServiceImpl;

public class GetKey {
	
	public ArrayList<String> getKeyList(){
		WxNumServiceImpl wxNumServiceImpl  = new WxNumServiceImpl();
		ArticleServiceImpl articleServiceImpl = new ArticleServiceImpl();
		
		String key1 = "";
		String key2 = "";
		String key3 = "";
		String key4 = "";
		
		IndexDto indexDto1 = new IndexDto();
		indexDto1.setKeyword("国寿");
		IndexDto indexDto2 = new IndexDto();
		indexDto2.setKeyword("中国人寿");
		IndexDto indexDto3 = new IndexDto();
		indexDto3.setKeyword("人寿");
		IndexDto indexDto4 = new IndexDto();
		indexDto4.setKeyword("寿险");
		
		try {
			indexDto1.setLevel("省级");
			key1 = key1+wxNumServiceImpl.getGZHNumIndex(indexDto1)+";";
			indexDto1.setLevel("市级");
			key1 = key1+wxNumServiceImpl.getGZHNumIndex(indexDto1)+";";
			indexDto1.setLevel("县区级");
			key1 = key1+wxNumServiceImpl.getGZHNumIndex(indexDto1)+";";
			indexDto1.setLevel("个人");
			key1 = key1+wxNumServiceImpl.getGZHNumIndex(indexDto1)+";";
			indexDto1.setLevel("");
			key1 = key1+wxNumServiceImpl.getGZHNumIndex(indexDto1)+";";
			
			indexDto1.setLevel("中");
			key1 = key1+articleServiceImpl.getArticleNumIndex(indexDto1)+";";
			indexDto1.setLevel("负");
			key1 = key1+articleServiceImpl.getArticleNumIndex(indexDto1)+";";
			indexDto1.setLevel("正");
			key1 = key1+articleServiceImpl.getArticleNumIndex(indexDto1)+";";
			indexDto1.setLevel(null);
			key1 = key1+articleServiceImpl.getArticleNumIndex(indexDto1);
			
			
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		try {
			indexDto2.setLevel("省级");
			key2 = key2+wxNumServiceImpl.getGZHNumIndex(indexDto2)+";";
			indexDto2.setLevel("市级");
			key2 = key2+wxNumServiceImpl.getGZHNumIndex(indexDto2)+";";
			indexDto2.setLevel("县区级");
			key2 = key2+wxNumServiceImpl.getGZHNumIndex(indexDto2)+";";
			indexDto2.setLevel("个人");
			key2 = key2+wxNumServiceImpl.getGZHNumIndex(indexDto2)+";";
			indexDto2.setLevel("");
			key2 = key2+wxNumServiceImpl.getGZHNumIndex(indexDto2)+";";
			
			indexDto2.setLevel("中");
			key2 = key2+articleServiceImpl.getArticleNumIndex(indexDto2)+";";
			indexDto2.setLevel("负");
			key2 = key2+articleServiceImpl.getArticleNumIndex(indexDto2)+";";
			indexDto2.setLevel("正");
			key2 = key2+articleServiceImpl.getArticleNumIndex(indexDto2)+";";
			indexDto2.setLevel(null);
			key2 = key2+articleServiceImpl.getArticleNumIndex(indexDto2);
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		try {
			indexDto3.setLevel("省级");
			key3 = key3+wxNumServiceImpl.getGZHNumIndex(indexDto3)+";";
			indexDto3.setLevel("市级");
			key3 = key3+wxNumServiceImpl.getGZHNumIndex(indexDto3)+";";
			indexDto3.setLevel("县区级");
			key3 = key3+wxNumServiceImpl.getGZHNumIndex(indexDto3)+";";
			indexDto3.setLevel("个人");
			key3 = key3+wxNumServiceImpl.getGZHNumIndex(indexDto3)+";";
			indexDto3.setLevel("");
			key3 = key3+wxNumServiceImpl.getGZHNumIndex(indexDto3)+";";
			
			indexDto3.setLevel("中");
			key3 = key3+articleServiceImpl.getArticleNumIndex(indexDto3)+";";
			indexDto3.setLevel("负");
			key3 = key3+articleServiceImpl.getArticleNumIndex(indexDto3)+";";
			indexDto3.setLevel("正");
			key3 = key3+articleServiceImpl.getArticleNumIndex(indexDto3)+";";
			indexDto3.setLevel(null);
			key3 = key3+articleServiceImpl.getArticleNumIndex(indexDto3);
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		try {
			indexDto4.setLevel("省级");
			key4 = key4+wxNumServiceImpl.getGZHNumIndex(indexDto4)+";";
			indexDto4.setLevel("市级");
			key4 = key4+wxNumServiceImpl.getGZHNumIndex(indexDto4)+";";
			indexDto4.setLevel("县区级");
			key4 = key4+wxNumServiceImpl.getGZHNumIndex(indexDto4)+";";
			indexDto4.setLevel("个人");
			key4 = key4+wxNumServiceImpl.getGZHNumIndex(indexDto4)+";";
			indexDto4.setLevel("");
			key4 = key4+wxNumServiceImpl.getGZHNumIndex(indexDto4)+";";
			
			indexDto4.setLevel("中");
			key4 = key4+articleServiceImpl.getArticleNumIndex(indexDto4)+";";
			indexDto4.setLevel("负");
			key4 = key4+articleServiceImpl.getArticleNumIndex(indexDto4)+";";
			indexDto4.setLevel("正");
			key4 = key4+articleServiceImpl.getArticleNumIndex(indexDto4)+";";
			indexDto4.setLevel(null);
			key4 = key4+articleServiceImpl.getArticleNumIndex(indexDto4);
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		ArrayList<String> list = new ArrayList<String>();
		list.add(key1);
		list.add(key2);
		list.add(key3);
		list.add(key4);
		
		
		return list;
		
	}
//	
//	
//	public static void main(String[] args) {
//		GetKey getKey = new GetKey();
//		ArrayList<String> list=getKey.getKey();
//		
//		System.out.println(list.get(0));
//		System.out.println(list.get(1));
//		System.out.println(list.get(2));
//		System.out.println(list.get(3));
//		
//	}
	
}
