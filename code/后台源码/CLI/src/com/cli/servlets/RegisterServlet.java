package com.cli.servlets;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.cli.bean.User;
import com.cli.service.impl.UserServiceImpl;

/**
 * Servlet implementation class RegisterServlet
 */
public class RegisterServlet extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public RegisterServlet() {
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
		String u_name = "致辉";
		String u_password="12345";
		UserServiceImpl userServiceImpl = new UserServiceImpl();
		User user = new User(u_name, u_password);
		
		try {
			if (u_name==null||u_password==null||u_name.equals("")||u_password.equals("")) {
				request.setAttribute("u_name", "用户名和密码不能为空");
				request.getRequestDispatcher("jsp地址").forward(request, response);
			}else {
				if (userServiceImpl.findUserByUserName(u_name)!=null) {
					//用户已经存在。给予提示信息
					request.setAttribute("u_name", "用户已存在");
					request.getRequestDispatcher("jsp地址").forward(request, response);
				}else {
					boolean right = userServiceImpl.insertUser(user);
					if (right) {
						//注册成果
						request.setAttribute("u_name", "注册成功");
						request.getRequestDispatcher("jsp地址").forward(request, response);
					}
				}
			}
			
			
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

}
