package com.cli.dao;

import java.io.IOException;
import java.io.InputStream;

import org.apache.ibatis.io.Resources;
import org.apache.ibatis.session.SqlSession;
import org.apache.ibatis.session.SqlSessionFactory;
import org.apache.ibatis.session.SqlSessionFactoryBuilder;

public class BaseDao {
	
	InputStream inputStream = null;
	public SqlSession getSqlSession(){
		SqlSession sqlSession = null;
		String resource = "mybaties-config.xml";
		try {
			//获取输入流
			inputStream  = Resources.getResourceAsStream(resource);
			//创建工厂
			SqlSessionFactory sqlSessionFactory=new SqlSessionFactoryBuilder().build(inputStream);
			//获取SqlSession对象
			sqlSession = sqlSessionFactory.openSession();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		
		return sqlSession;
		
		
		
	}

}
