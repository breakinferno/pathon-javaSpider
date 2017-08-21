package com.cli.bean;

public class Page {

	private int offset;
	private String level;
	

	
	public Page(int offset, String level) {
		super();
		this.offset = offset;
		this.level = level;
	}
	public int getOffset() {
		return offset;
	}
	public void setOffset(int offset) {
		this.offset = offset;
	}

	public String getLevel() {
		return level;
	}
	public void setLevel(String level) {
		this.level = level;
	}

	

	
}
