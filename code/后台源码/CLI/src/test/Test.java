package test;


import com.cli.bean.Article;
import com.cli.bean.IndexDto;
import com.cli.service.impl.ArticleServiceImpl;
import com.cli.service.impl.ArticlesServiceImpl;
import com.cli.service.impl.WxNumServiceImpl;

public class Test {
	public static void main(String[] args) throws Exception {
		ArticleServiceImpl articleServiceImpl = new ArticleServiceImpl();
		WxNumServiceImpl wxNumServiceImpl = new WxNumServiceImpl();
		ArticlesServiceImpl articlesServiceImpl = new ArticlesServiceImpl();
		
		int num = articleServiceImpl.getArticleNumIndex(new IndexDto("中国人寿", "正"));
		System.out.println(num);
		int wxnumNum = wxNumServiceImpl.getGZHNumIndex(new IndexDto("中国人寿", "省级"));
		System.out.println(wxnumNum);
	}

}
