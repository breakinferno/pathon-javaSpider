package com.cli.utils;

import java.util.ArrayList;

import net.sf.json.JSONArray;
import net.sf.json.JSONObject;

import com.cli.bean.Article;
import com.cli.bean.WxNum;

public class translateObjToJSON {
	
	public static JSONObject translateWxNum(WxNum wxNum){
		JSONObject jsob = new JSONObject();
		jsob.put("wx_num", wxNum.getWx_num());
		jsob.put("wx_num_link", wxNum.getWx_num_link());
		jsob.put("wx_num_name", wxNum.getWx_num_name());
		jsob.put("fun_into", wxNum.getFun_into());
		jsob.put("authentication", wxNum.getAuthentication());
		jsob.put("pubarticle", wxNum.getPubarticle());
		jsob.put("add_time", wxNum.getAdd_time());
		jsob.put("level", wxNum.getLevel());
		jsob.put("wx_num_img_link", wxNum.getWx_num_img());
		return jsob;
	}
	
	public static JSONObject translateArticle(Article article){
		JSONObject jsob = new JSONObject();
		jsob.put("article_id", article.getArticle_id());
		jsob.put("article_title", article.getArticle_title());
		jsob.put("article_url", article.getArticle_url());
		jsob.put("article_abstract", article.getArticle_abstract());
		jsob.put("article_time", article.getArticle_time());
		jsob.put("article_gzh_name", article.getArticle_gzh_name());
		jsob.put("article_gzh_url", article.getArticle_gzh_url());
		jsob.put("category", article.getCategory());
		jsob.put("article_gzh_headimg", article.getArticle_gzh_headimg());
		jsob.put("add_time", article.getAdd_time());
		jsob.put("admin_confirm", article.getAdmin_confirm());
		jsob.put("keyword", article.getKeyword());
		return jsob;
	}
	
	
	public static JSONArray translateWxNumList(ArrayList<WxNum> list){
		JSONArray jsonArray = new JSONArray();
		for(WxNum wxNum : list){
			jsonArray.add(translateWxNum(wxNum));
		}
		return jsonArray;
	}
	
	public static JSONArray translatArticleList(ArrayList<Article> list){
		JSONArray jsonArray = new JSONArray();
		for(Article article : list){
			jsonArray.add(translateArticle(article));
		}
		return jsonArray;
	}
}
