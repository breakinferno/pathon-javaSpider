package com.cli.mapper;

import com.cli.bean.Article;
import com.mysql.jdbc.EscapeTokenizer;

public interface ArticlesMapper {

	public boolean insertArticles(Article article) throws Exception;
}
