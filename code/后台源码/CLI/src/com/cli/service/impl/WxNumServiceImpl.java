package com.cli.service.impl;

import java.util.ArrayList;

import org.apache.ibatis.session.SqlSession;

import com.cli.bean.IndexDto;
import com.cli.bean.Page;
import com.cli.bean.WxNum;
import com.cli.dao.BaseDao;
import com.cli.mapper.WxNumMapper;
import com.cli.service.WxNumService;
import com.cli.ui.Tool;

public class WxNumServiceImpl implements WxNumService {

	Tool tool= new Tool();
	BaseDao bd  = new BaseDao();
	SqlSession sqlSession  = bd.getSqlSession();
	WxNumMapper wxNumMapper = sqlSession.getMapper(WxNumMapper.class);
	@Override
	public ArrayList<WxNum> findAllWxNum(int offset) throws Exception{
		ArrayList<WxNum> list = wxNumMapper.findAllWxNum(offset);
		return list;
	}
	@Override
	public ArrayList<WxNum> findWxNumByProLevel(Page page) throws Exception {
		ArrayList<WxNum> list = wxNumMapper.findWxNumByProLevel(page);
		return list;
	}
	@Override
	public boolean updateLinkByWxNum(WxNum wxNum) throws Exception {
		boolean right= wxNumMapper.updateLinkByWxNum(wxNum);
		sqlSession.commit();
		return right;
		
	}
	@Override
	public boolean updateLevelByWxNum(WxNum wxNum) throws Exception {
		boolean right= wxNumMapper.updateLevelByWxNum(wxNum);
		sqlSession.commit();
		return right;
	}
	@Override
	public ArrayList<WxNum> findWxNumNotProLevel(Page page) throws Exception {
		ArrayList<WxNum> list = wxNumMapper.findWxNumNotProLevel(page);
		return list;
	}
	@Override
	public int findAllPage() throws Exception {
		int allrow = wxNumMapper.findAllPage();
		return tool.getPage(allrow);
	}
	@Override
	public int findAllProLevelPageNum(String level) throws Exception {
		int allrow = wxNumMapper.findAllProLevelPageNum(level);
		return tool.getPage(allrow);
	}
	@Override
	public int findAllNotProLevelPageNum(String level) throws Exception {
		int allrow = wxNumMapper.findAllNotProLevelPageNum(level);
		return tool.getPage(allrow);
	}
	@Override
	public boolean deleteWxNum(String wx_num) throws Exception {
		boolean right = wxNumMapper.deleteWxNum(wx_num);
		sqlSession.commit();
		return right;
	}
	@Override
	public int getGZHNumIndex(IndexDto indexDto) throws Exception {
		int num = wxNumMapper.getGZHNumIndex(indexDto);
		
		return num;
	}

}
