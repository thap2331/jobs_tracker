from datetime import datetime

class ScrapingUtils:

    def title_splitter(self, title: str):
        if not isinstance(title, str):
            return []

        title_list = title.split(';')
        title_list = [i.strip() for  i in title_list]
        titles_seperated_by_dash = [title.replace(' ', '-') for title in title_list]
        title_list.extend(titles_seperated_by_dash)

        return title_list

class PrepCrawlogs:

    def prepare_crawlogs_from_last_crawled(self, data):

        now = datetime.now()
        
        dict_or_list = any([isinstance(data, dict), isinstance(data, list)])
            
        if dict_or_list is False:
            print(f"Data ({data}) is neither a dict nor a list.")
            return
        
        #If data is a list
        are_dict = True
        if isinstance(data, list):
            #all inside should be a dict
            are_dict = all([isinstance(i, dict) for i in data])

        if not are_dict:
            print(f"All data inside a list ({data}) are not a dict.")
            return

        if isinstance(data, list):
            for row in data:
                row["last_attempted_crawl"]=now

        #If data is a dict
        if isinstance(data, dict):
            data["last_attempted_crawl"]=now

            data = [data]
        
        return data
