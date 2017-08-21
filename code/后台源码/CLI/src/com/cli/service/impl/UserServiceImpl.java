package com.cli.service.impl;

import org.apache.ibatis.session.SqlSession;

import com.cli.bean.User;
import com.cli.dao.BaseDao;
import com.cli.mapper.ArticlesMapper;
import com.cli.mapper.UserMapper;
import com.cli.service.UserService;

public class UserServiceImpl implements UserService {

	BaseDao bd  = new BaseDao();
	SqlSession sqlSession  = bd.getSqlSession();
	UserMapper userMapper = sqlSession.getMapper(UserMapper.class);
	@Override
	public User findUser(User user) throws Exception {
		User user2 = userMapper.findUser(user);
		return user2;
	}

	@Override
	public User findUserByUserName(String u_name) throws Exception {
		User user =  userMapper.findUserByUserName(u_name);
		return user;
	}

	@Override
	public boolean insertUser(User user) throws Exception {
		boolean right = userMapper.insertUser(user);
		sqlSession.commit();
		return right;
	}

	@Override
	public boolean deleteUserByUserName(String u_name) throws Exception {
		boolean right = userMapper.deleteUserByUserName(u_name);
		sqlSession.commit();
		return right;
	}

	@Override
	public boolean updateUserPassword(User user) throws Exception {
		boolean right = userMapper.updateUserPassword(user);
		sqlSession.commit();
		return right;
	}

}
