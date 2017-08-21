package com.cli.bean;

public class WxNum {

	private String wx_num;
	private String wx_num_link;
	private String wx_num_name;
	private String wx_num_img;
	private String fun_into;
	private String authentication;
	private String pubarticle;
	private String add_time;
	private String level;
	private String keyword;
	
	
	public WxNum() {
		super();
	}
	
	public WxNum(String wx_num) {
		super();
		this.wx_num = wx_num;
	}



	/**
	 * 用于更新微信公众号连接
	 * @param wx_num
	 * @param wx_num_link
	 */
	public WxNum(String wx_num, String wx_num_link,String level) {
		super();
		this.wx_num = wx_num;
		this.wx_num_link = wx_num_link;
		this.level = level;
	}
	
	public WxNum(String wx_num, String wx_num_link, String wx_num_name,
			String wx_num_img, String fun_into, String authentication,
			String pubarticle, String add_time, String level, String keyword) {
		super();
		this.wx_num = wx_num;
		this.wx_num_link = wx_num_link;
		this.wx_num_name = wx_num_name;
		this.wx_num_img = wx_num_img;
		this.fun_into = fun_into;
		this.authentication = authentication;
		this.pubarticle = pubarticle;
		this.add_time = add_time;
		this.level = level;
		this.keyword = keyword;
	}


	public String getWx_num() {
		return wx_num;
	}
	public void setWx_num(String wx_num) {
		this.wx_num = wx_num;
	}
	public String getWx_num_link() {
		return wx_num_link;
	}
	public void setWx_num_link(String wx_num_link) {
		this.wx_num_link = wx_num_link;
	}
	public String getWx_num_name() {
		return wx_num_name;
	}
	public void setWx_num_name(String wx_num_name) {
		this.wx_num_name = wx_num_name;
	}
	
	public String getWx_num_img() {
		return wx_num_img;
	}


	public void setWx_num_img(String wx_num_img) {
		this.wx_num_img = wx_num_img;
	}


	public String getFun_into() {
		return fun_into;
	}
	public void setFun_into(String fun_into) {
		this.fun_into = fun_into;
	}
	public String getAuthentication() {
		return authentication;
	}
	public void setAuthentication(String authentication) {
		this.authentication = authentication;
	}
	public String getPubarticle() {
		return pubarticle;
	}
	public void setPubarticle(String pubarticle) {
		this.pubarticle = pubarticle;
	}
	public String getAdd_time() {
		return add_time;
	}
	public void setAdd_time(String add_time) {
		this.add_time = add_time;
	}
	public String getLevel() {
		return level;
	}
	public void setLevel(String level) {
		this.level = level;
	}
	public String getKeyword() {
		return keyword;
	}
	public void setKeyword(String keyword) {
		this.keyword = keyword;
	}


	@Override
	public String toString() {
		return "WxNum [wx_num=" + wx_num + ", wx_num_link=" + wx_num_link
				+ ", wx_num_name=" + wx_num_name + ", wx_num_img=" + wx_num_img
				+ ", fun_into=" + fun_into + ", authentication="
				+ authentication + ", pubarticle=" + pubarticle + ", add_time="
				+ add_time + ", level=" + level + ", keyword=" + keyword + "]";
	}
	
	
	
	
}
