package com.cli.mapper;

import java.util.ArrayList;

import com.cli.bean.Article;
import com.cli.bean.IndexDto;
import com.cli.bean.Page;

public interface ArticleMapper {
	/**
	 * ����article_id��������
	 * @param article_id
	 * @return
	 * @throws Exception
	 */
	public Article findArticleById(int article_id) throws Exception;
	
	/**
	 * ��ѯ��ҳ��
	 * @return
	 * @throws Exception
	 */
	public int getAllPageNum() throws Exception;
	/**
	 * ��ѯ���е�����
	 * @param offset
	 * @return
	 * @throws Exception
	 */
	public ArrayList<Article> findAllArticle(int offset) throws Exception;
	/**
	 *��ѯ������������ҳ��
	 * @param title
	 * @return
	 * @throws Exception
	 */
	public int getAllPageNumInTitle(String title) throws Exception;
	/**
	 * ����titleģ����ѯ����
	 * @param title
	 * @return
	 * @throws Exception
	 */
	public ArrayList<Article> findArticleByTitle(String title) throws Exception;
	/**
	 * ����article_id����category����
	 * @param article
	 * @return
	 * @throws Exception
	 */
	public boolean updateCategoryById(Article article) throws Exception;
	
	/**
	 * ��ȡ���йؼ���
	 * @return
	 * @throws Exception
	 */
	public ArrayList<String> getKeyWord() throws Exception;
	/**
	 * ��������article_id ɾ������
	 * @param article_id
	 * @return
	 * @throws Exception
	 */
	public boolean deleteArticle (int article_id)throws Exception;
	
	/**
	 * ��ȡ�������ҳ��
	 * @param title
	 * @return
	 * @throws Exception
	 */
	public int getAllPageNumInCategory(String category) throws Exception;
	/**
	 * �������������������
	 * @param page
	 * @return
	 * @throws Exception
	 */
	public ArrayList<Article> findArticleByCategory(Page page) throws Exception;
	/**
	 * 
	 * 查询文章各级别的总数
	 * @param indexDto
	 * @return
	 * @throws Exception
	 */
	public int getArticleNumIndex(IndexDto indexDto) throws Exception;
	
}
