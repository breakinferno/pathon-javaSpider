package com.cli.service.impl;

import org.apache.ibatis.session.SqlSession;

import com.cli.bean.Article;
import com.cli.dao.BaseDao;
import com.cli.mapper.ArticleMapper;
import com.cli.mapper.ArticlesMapper;
import com.cli.service.ArticlesService;

public class ArticlesServiceImpl implements ArticlesService {
	BaseDao bd  = new BaseDao();
	SqlSession sqlSession  = bd.getSqlSession();
	ArticlesMapper articlesMapper = sqlSession.getMapper(ArticlesMapper.class);

	@Override
	public boolean insertArticles(Article article) throws Exception {
		boolean right = articlesMapper.insertArticles(article);
		sqlSession.commit();
		return right;
	}

}
