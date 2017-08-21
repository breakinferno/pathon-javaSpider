package com.cli.bean;

public class Article {

	private int article_id;
	private String article_title;
	private String article_url;
	private String article_abstract;
	private String article_time;
	private String article_gzh_name;
	private String article_gzh_url;
	private String article_gzh_headimg;
	private String category;
	private String add_time;
	private int admin_confirm;
	private String keyword;
	
	
	public Article() {
		super();
	}
	

	public Article(int article_id, String category ) {
		super();
		this.article_id = article_id;
		this.category = category;
	}




	public Article(String article_title, String article_url,
			String article_abstract, String article_time,
			String article_gzh_name, String article_gzh_url,
			String article_gzh_headimg, String category, String add_time,
			int admin_confirm, String keyword) {
		super();
		this.article_title = article_title;
		this.article_url = article_url;
		this.article_abstract = article_abstract;
		this.article_time = article_time;
		this.article_gzh_name = article_gzh_name;
		this.article_gzh_url = article_gzh_url;
		this.article_gzh_headimg = article_gzh_headimg;
		this.category = category;
		this.add_time = add_time;
		this.admin_confirm = admin_confirm;
		this.keyword = keyword;
	}
	public int getArticle_id() {
		return article_id;
	}
	public void setArticle_id(int article_id) {
		this.article_id = article_id;
	}
	public String getArticle_title() {
		return article_title;
	}
	public void setArticle_title(String article_title) {
		this.article_title = article_title;
	}
	public String getArticle_url() {
		return article_url;
	}
	public void setArticle_url(String article_url) {
		this.article_url = article_url;
	}
	public String getArticle_abstract() {
		return article_abstract;
	}
	public void setArticle_abstract(String article_abstract) {
		this.article_abstract = article_abstract;
	}
	public String getArticle_time() {
		return article_time;
	}
	public void setArticle_time(String article_time) {
		this.article_time = article_time;
	}
	public String getArticle_gzh_name() {
		return article_gzh_name;
	}
	public void setArticle_gzh_name(String article_gzh_name) {
		this.article_gzh_name = article_gzh_name;
	}
	public String getArticle_gzh_url() {
		return article_gzh_url;
	}
	public void setArticle_gzh_url(String article_gzh_url) {
		this.article_gzh_url = article_gzh_url;
	}
	public String getArticle_gzh_headimg() {
		return article_gzh_headimg;
	}
	public void setArticle_gzh_headimg(String article_gzh_headimg) {
		this.article_gzh_headimg = article_gzh_headimg;
	}
	public String getCategory() {
		return category;
	}
	public void setCategory(String category) {
		this.category = category;
	}
	public String getAdd_time() {
		return add_time;
	}
	public void setAdd_time(String add_time) {
		this.add_time = add_time;
	}
	public int getAdmin_confirm() {
		return admin_confirm;
	}
	public void setAdmin_confirm(int admin_confirm) {
		this.admin_confirm = admin_confirm;
	}
	public String getKeyword() {
		return keyword;
	}
	public void setKeyword(String keyword) {
		this.keyword = keyword;
	}
	@Override
	public String toString() {
		return "Article [article_id=" + article_id + ", article_title="
				+ article_title + ", article_url=" + article_url
				+ ", article_abstract=" + article_abstract + ", article_time="
				+ article_time + ", article_gzh_name=" + article_gzh_name
				+ ", article_gzh_url=" + article_gzh_url
				+ ", article_gzh_headimg=" + article_gzh_headimg
				+ ", category=" + category + ", add_time=" + add_time
				+ ", admin_confirm=" + admin_confirm + ", keyword=" + keyword
				+ "]";
	}
	
	
}
