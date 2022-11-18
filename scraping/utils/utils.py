
class ScrapingUtils:

    def title_splitter(self, title: str):
        if not isinstance(title, str):
            return []

        title_list = title.split(';')
        title_list = [i.strip() for  i in title_list]
        titles_seperated_by_dash = [title.replace(' ', '-') for title in title_list]
        title_list.extend(titles_seperated_by_dash)

        return title_list