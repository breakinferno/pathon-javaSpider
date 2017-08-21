package com.cli.service;

import java.util.ArrayList;

import com.cli.bean.IndexDto;
import com.cli.bean.Page;
import com.cli.bean.WxNum;

public interface WxNumService {
	
	/**
	 * ��ѯ������
	 * @param page
	 * @return
	 * @throws Exception
	 */
	public int findAllPage() throws Exception;

	/*
	 * ��ѯȫ��
	 */
	public ArrayList<WxNum> findAllWxNum(int offset) throws Exception;
	/**
	 * ��ѯʡ����ҳ��
	 * @param page
	 * @return
	 * @throws Exception
	 */
	public int findAllProLevelPageNum(String level) throws Exception;
	/**
	 * ��ѯʡ��
	 * @param page
	 * @return
	 * @throws Exception
	 */
	public ArrayList<WxNum> findWxNumByProLevel(Page page) throws Exception;
	/**
	 * ��ѯ��ʡ����ҳ��
	 * @param page
	 * @return
	 * @throws Exception
	 */
	public int findAllNotProLevelPageNum(String level) throws Exception;
	/**
	 * ��ѯ��ʡ��
	 * @param page
	 * @return
	 * @throws Exception
	 */
	public ArrayList<WxNum> findWxNumNotProLevel(Page page) throws Exception;
	/**
	 * ��������
	 * @param wxNum
	 * @return
	 * @throws Exception
	 */
	public boolean updateLinkByWxNum( WxNum wxNum) throws Exception;
	/**
	 * �޸ĵȼ�
	 * @param wxNum
	 * @return
	 * @throws Exception
	 */
	public boolean updateLevelByWxNum( WxNum wxNum) throws Exception;
	/**
	 * ɾ��΢�ź�
	 * @param wxNum
	 * @return
	 * @throws Exception
	 */
	public boolean deleteWxNum( String wx_num) throws Exception;
	/**
	 * 查询个级别公众号的总数
	 * @param indexDto
	 * @return
	 * @throws Exception
	 */
	public int getGZHNumIndex(IndexDto indexDto) throws Exception;
}
