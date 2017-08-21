package com.cli.servlets;

import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;


import com.cli.bean.Article;
import com.cli.bean.Page;
import com.cli.bean.WxNum;
import com.cli.service.impl.ArticleServiceImpl;
import com.cli.service.impl.WxNumServiceImpl;
import com.cli.utils.translateObjToJSON;

import net.sf.json.JSONArray;
import net.sf.json.JSONObject;

public class HandleArticle extends HttpServlet {

	/**
	 * The doGet method of the servlet. <br>
	 *
	 * This method is called when a form has its tag value method equals to get.
	 * 
	 * @param request
	 *            the request send by the client to the server
	 * @param response
	 *            the response send by the server to the client
	 * @throws ServletException
	 *             if an error occurred
	 * @throws IOException
	 *             if an error occurred
	 */
	public void doGet(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {

		response.setContentType("text/html");
		PrintWriter out = response.getWriter();
		out.println("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EN\">");
		out.println("<HTML>");
		out.println("  <HEAD><TITLE>A Servlet</TITLE></HEAD>");
		out.println("  <BODY>");
		out.print("    This is ");
		out.print(this.getClass());
		out.println(", using the GET method");
		out.println("  </BODY>");
		out.println("</HTML>");
		out.flush();
		out.close();
	}

	/**
	 * The doPost method of the servlet. <br>
	 *
	 * This method is called when a form has its tag value method equals to
	 * post.
	 * 
	 * @param request
	 *            the request send by the client to the server
	 * @param response
	 *            the response send by the server to the client
	 * @throws ServletException
	 *             if an error occurred
	 * @throws IOException
	 *             if an error occurred
	 */
	public void doPost(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {

		response.setContentType("application/json;charset=utf-8");
		PrintWriter out = response.getWriter();
		String level = request.getParameter("level");
		int page = Integer.parseInt(request.getParameter("page"));
		ArticleServiceImpl articleServiceImpl = new ArticleServiceImpl();
		switch (level) {
		case "all":
			try {
				ArrayList<Article> list = articleServiceImpl.findAllArticle((page-1)*10);
				JSONArray jsonArray = translateObjToJSON.translatArticleList(list);
				JSONObject rt = new JSONObject();
				rt.put("data", jsonArray);
				//System.out.println("total page is "+ wxNumServiceImpl.findAllPage());
				rt.put("totalPage", articleServiceImpl.getAllPageNum());
				
				//����ajax
				out.write(rt.toString());
			} catch (Exception e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
			break;
		case "positive":
			try {
				System.out.println(page);
				ArrayList<Article> list = articleServiceImpl.findArticleByCategory(new Page((page-1)*10,"正"));
				JSONArray jsonArray = translateObjToJSON.translatArticleList(list);
				JSONObject rt = new JSONObject();
				rt.put("data", jsonArray);
				rt.put("totalPage", articleServiceImpl.getAllPageNumInCategory("正"));
				//����ajax
				out.write(rt.toString());
			} catch (Exception e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
			break;
		case "negative":
			try {
				System.out.println(page);
				ArrayList<Article> list = articleServiceImpl.findArticleByCategory(new Page((page-1)*10,"负"));
				JSONArray jsonArray = translateObjToJSON.translatArticleList(list);
				JSONObject rt = new JSONObject();
				rt.put("data", jsonArray);
				rt.put("totalPage", articleServiceImpl.getAllPageNumInCategory("负"));
				//����ajax
				out.write(rt.toString());
			} catch (Exception e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
			break;
		case "balance":
			try {
				ArrayList<Article> list = articleServiceImpl.findArticleByCategory(new Page((page-1)*10,"中"));
				JSONArray jsonArray = translateObjToJSON.translatArticleList(list);
				JSONObject rt = new JSONObject();
				rt.put("data", jsonArray);
				rt.put("totalPage", articleServiceImpl.getAllPageNumInCategory("中"));
				
				//����ajax
				out.write(rt.toString());
			} catch (Exception e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
			break;
		case "search":
			String title = request.getParameter("title");
			try {
				ArrayList<Article> list = articleServiceImpl.findArticleByTitle(title);
				JSONArray jsonArray = translateObjToJSON.translatArticleList(list);
				JSONObject rt = new JSONObject();
				rt.put("data", jsonArray);
				rt.put("totalPage", articleServiceImpl.getAllPageNumInTitle(title));
				
				//����ajax
				out.write(rt.toString());
			} catch (Exception e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
			break;
		default:
			
			break;
		}

		out.flush();
		out.close();
	}

}
