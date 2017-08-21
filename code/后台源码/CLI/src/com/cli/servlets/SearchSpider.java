package com.cli.servlets;

import java.io.IOException;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.cli.ui.SpiderController;

/**
 * Servlet implementation class SearchSpider
 */
@WebServlet("/SearchSpider")
public class SearchSpider extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public SearchSpider() {
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
		// TODO Auto-generated method stub
		String input = request.getParameter("value");
		String type = request.getParameter("type");
		SpiderController spiderController = new SpiderController();
		
		
		switch(type){
		case "article":
			//文章
			spiderController.spiderArticle(input);
			break;
		case "wxnum":
			//公众号
			spiderController.spiderGZH(input);
			break;
		default:
			//默认错误
		}
	}

}
