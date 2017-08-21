package com.cli.ui;

public class Tool {
	int pageSize=10;
	public int getPage(int allrow){
		if((allrow%pageSize)==0)
			return allrow/pageSize;
		else
			return allrow/pageSize +1;
	}

}
