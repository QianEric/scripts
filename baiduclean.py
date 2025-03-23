import requests
from bs4 import BeautifulSoup
import time
import re

class TiebaCleaner:
    def __init__(self, tieba_name, bduss_cookie):
        """初始化贴吧名称和用户BDUSS cookie"""
        self.tieba_name = tieba_name
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Cookie': f'BDUSS={bduss_cookie}',
            'Referer': f'https://tieba.baidu.com/f?kw={tieba_name}'
        }
        
    def get_tbs(self):
        """获取操作所需的tbs参数"""
        url = 'http://tieba.baidu.com/dc/common/tbs'
        response = self.session.get(url, headers=self.headers)
        return response.json()['tbs']
    
    def get_thread_list(self, page=1):
        """获取帖子列表"""
        url = f'https://tieba.baidu.com/f?kw={self.tieba_name}&pn={(page-1)*50}'
        response = self.session.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        threads = soup.select('.j_thread_list')
        
        thread_ids = []
        for thread in threads:
            try:
                thread_id = thread['data-tid']
                title = thread.select_one('.j_th_tit').text.strip()
                thread_ids.append({'id': thread_id, 'title': title})
            except:
                continue
        return thread_ids
    
    def is_spam(self, title):
        """判断帖子是否为垃圾贴，可自定义规则"""
        spam_keywords = ['广告', '代购', '刷单', '加微信', '招聘', '推广']  # 可自定义垃圾关键词
        title = title.lower()
        return any(keyword in title for keyword in spam_keywords)
    
    def delete_thread(self, thread_id, tbs):
        """删除指定帖子"""
        url = 'http://tieba.baidu.com/f/commit/thread/delete'
        data = {
            'fid': self.get_fid(),
            'tbs': tbs,
            'tid': thread_id,
            'commit_fr': 'pb',
            'ie': 'utf-8'
        }
        response = self.session.post(url, headers=self.headers, data=data)
        return response.json()
    
    def get_fid(self):
        """获取贴吧的fid"""
        url = f'https://tieba.baidu.com/f?kw={self.tieba_name}'
        response = self.session.get(url, headers=self.headers)
        match = re.search(r'"forum_id":(\d+),', response.text)
        return match.group(1) if match else None
    
    def clean_spam(self, max_pages=5):
        """批量清理垃圾贴"""
        tbs = self.get_tbs()
        deleted_count = 0
        
        for page in range(1, max_pages + 1):
            print(f"正在处理第 {page} 页...")
            threads = self.get_thread_list(page)
            
            for thread in threads:
                if self.is_spam(thread['title']):
                    print(f"发现垃圾贴: {thread['title']}")
                    result = self.delete_thread(thread['id'], tbs)
                    if result.get('no') == 0:
                        print(f"成功删除帖子 ID: {thread['id']}")
                        deleted_count += 1
                    else:
                        print(f"删除失败: {result.get('error')}")
                    time.sleep(1)  # 防止触发频率限制
                    
            time.sleep(2)  # 每页之间稍作停顿
            
        print(f"清理完成，总计删除 {deleted_count} 个垃圾贴")
        
def main():
    # 配置参数
    tieba_name = "输入你的贴吧名称"  # 替换为目标贴吧名称
    bduss_cookie = "输入你的BDUSS cookie"  # 替换为你的BDUSS cookie
    
    # 创建清理器实例并运行
    cleaner = TiebaCleaner(tieba_name, bduss_cookie)
    cleaner.clean_spam(max_pages=5)  # 可调整清理的页面数

if __name__ == "__main__":
    main()