package com.cli.servlets;

import java.io.IOException;
import java.util.ArrayList;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.cli.bean.User;
import com.cli.service.impl.UserServiceImpl;
import com.cli.ui.GetKey;

/**
 * Servlet implementation class LoginServlet
 */
public class LoginServlet extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public LoginServlet() {
        super();
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		response.getWriter().append("Served at: ").append(request.getContextPath());
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		String u_name = request.getParameter("account");
		String u_password=request.getParameter("password");
		
		//转码
		u_name = new String(u_name.getBytes("iso-8859-1"),"utf-8");
		UserServiceImpl userServiceImpl = new UserServiceImpl();
		GetKey getKey = new GetKey();
		
		
		User user = new User(u_name, u_password);
		System.out.println(user);
		try {
			
			if (userServiceImpl.findUser(user)!=null) {
				//登录成果，跳到用户页面
				System.out.println("登录成功");
				ArrayList<String> keyList = getKey.getKeyList();
				request.setAttribute("u_name", u_name);
				request.setAttribute("key1",  keyList.get(0));
				request.setAttribute("key2",  keyList.get(1));
				request.setAttribute("key3",  keyList.get(2));
				request.setAttribute("key4",  keyList.get(3));
				request.getRequestDispatcher("main.jsp").forward(request, response);
			}
			else {
				//用户不存在，给予提示信息
				System.out.println("用户不存在");
//				request.setAttribute("u_name", "用户不存在");
				request.getRequestDispatcher("login.jsp").forward(request, response);
			}
			
			
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

}
