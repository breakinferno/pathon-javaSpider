package com.cli.bean;

public class IndexDto {

	private String keyword;
	private String level;
	
	
	public IndexDto() {
		super();
	}
	public IndexDto(String keyword, String level) {
		super();
		this.keyword = keyword;
		this.level = level;
	}
	public String getKeyword() {
		return keyword;
	}
	public void setKeyword(String keyword) {
		this.keyword = keyword;
	}
	public String getLevel() {
		return level;
	}
	public void setLevel(String level) {
		this.level = level;
	}
	
	@Override
	public String toString() {
		return "IndexDto [keyword=" + keyword + ", level=" + level + "]";
	}
}
