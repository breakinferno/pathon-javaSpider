package com.cli.service.impl;

import java.util.ArrayList;

import org.apache.ibatis.session.SqlSession;

import com.cli.bean.Article;
import com.cli.bean.IndexDto;
import com.cli.bean.Page;
import com.cli.dao.BaseDao;
import com.cli.mapper.ArticleMapper;
import com.cli.mapper.WxNumMapper;
import com.cli.service.ArticleService;
import com.cli.ui.Tool;

public class ArticleServiceImpl implements ArticleService {

	Tool tool = new Tool();
	BaseDao bd  = new BaseDao();
	SqlSession sqlSession  = bd.getSqlSession();
	ArticleMapper articleMapper = sqlSession.getMapper(ArticleMapper.class);
	@Override
	public ArrayList<Article> findAllArticle(int offset) throws Exception {
		// TODO Auto-generated method stub
		ArrayList<Article> list = articleMapper.findAllArticle(offset);
		return list;
	}
	@Override
	public ArrayList<Article> findArticleByTitle(String title) throws Exception {
		ArrayList<Article> list = articleMapper.findArticleByTitle(title);
		return list;
	}
	@Override
	public int getAllPageNum() throws Exception {
		int allrow = articleMapper.getAllPageNum();
		return tool.getPage(allrow);
	}
	@Override
	public int getAllPageNumInTitle(String title) throws Exception {
		int allrow = articleMapper.getAllPageNumInTitle(title);
		return tool.getPage(allrow);
	}
	@Override
	public boolean updateCategoryById(Article article) throws Exception {
		boolean right = articleMapper.updateCategoryById(article);
		sqlSession.commit();
		return right;
	}
	@Override
	public ArrayList<String> getKeyWord() throws Exception {
		ArrayList<String> list = articleMapper.getKeyWord();
		return list;
	}
	@Override
	public boolean deleteArticle(int article_id) throws Exception {
		boolean right = articleMapper.deleteArticle(article_id);
		sqlSession.commit();
		return right;
	}
	@Override
	public int getAllPageNumInCategory(String category) throws Exception {
		int allrow = articleMapper.getAllPageNumInCategory(category);
		return tool.getPage(allrow);
	}
	@Override
	public ArrayList<Article> findArticleByCategory(Page page) throws Exception {
		ArrayList<Article> list = articleMapper.findArticleByCategory(page);
		return list;
	}
	@Override
	public Article findArticleById(int article_id) throws Exception {
		Article article = articleMapper.findArticleById(article_id);
		return article;
	}
	@Override
	public int getArticleNumIndex(IndexDto indexDto) throws Exception {
		int num = articleMapper.getArticleNumIndex(indexDto);
		return num;
	}

}
