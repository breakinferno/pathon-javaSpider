package com.cli.servlets;

import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;

import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.cli.bean.Page;
import com.cli.bean.WxNum;
import com.cli.service.impl.WxNumServiceImpl;
import com.cli.utils.translateObjToJSON;

import net.sf.json.JSONArray;
import net.sf.json.JSONObject;

public class HandleWxNum extends HttpServlet {

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
		WxNumServiceImpl wxNumServiceImpl = new WxNumServiceImpl();
		switch (level) {
		case "all":
			try {
				ArrayList<WxNum> list = wxNumServiceImpl.findAllWxNum((page-1)*10);
				JSONArray jsonArray = translateObjToJSON.translateWxNumList(list);
				JSONObject rt = new JSONObject();
				rt.put("data", jsonArray);
				System.out.println("total page is "+ wxNumServiceImpl.findAllPage());
				rt.put("totalPage", wxNumServiceImpl.findAllPage());
				
				//����ajax
				out.write(rt.toString());
			} catch (Exception e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
			break;
		case "province":
			try {
				System.out.println(page);
				ArrayList<WxNum> list = wxNumServiceImpl.findWxNumByProLevel(new Page((page-1)*10,"省级"));
				JSONArray jsonArray = translateObjToJSON.translateWxNumList(list);
				JSONObject rt = new JSONObject();
				rt.put("data", jsonArray);
				rt.put("totalPage", wxNumServiceImpl.findAllProLevelPageNum("省级"));
				//����ajax
				out.write(rt.toString());
			} catch (Exception e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
			break;
		default:
			try {
				ArrayList<WxNum> list = wxNumServiceImpl.findWxNumNotProLevel(new Page((page-1)*10,"省级"));
				JSONArray jsonArray = translateObjToJSON.translateWxNumList(list);
				JSONObject rt = new JSONObject();
				rt.put("data", jsonArray);
				rt.put("totalPage", wxNumServiceImpl.findAllNotProLevelPageNum("省级"));
				
				//����ajax
				out.write(rt.toString());
			} catch (Exception e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
			break;
		}

		out.flush();
		out.close();
	}

}
