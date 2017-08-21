package com.cli.service;

import com.cli.bean.User;

public interface UserService {

	/**
	 * 查询用户是否存在，密码是否正确，用于用户登录时使用
	 * @param user
	 * @return
	 * @throws Exception
	 */
	public User findUser(User user)throws Exception;
	/**
	 * 用户注册时利用用户名查询用户是否存在，
	 * @param u_name
	 * @return
	 * @throws Exception
	 */
	public User findUserByUserName(String u_name)throws Exception;
	
	/**
	 * 用户注册时插入用户信息
	 * @param user
	 * @return
	 * @throws Exception
	 */
	public boolean insertUser(User user)throws Exception;
	
	/**
	 * 删除用户
	 * @param u_name
	 * @return
	 * @throws Exception
	 */
	public boolean deleteUserByUserName(String u_name)throws Exception;
	/**
	 * 更新用户密码
	 * @param user
	 * @return
	 * @throws Exception
	 */
	public boolean updateUserPassword(User user) throws Exception;
	
}
