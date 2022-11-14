
class UrlUtils:

    def __init__(self) -> None:
        self.follow_pattern = {
            "do_not_follow_endswith": ['.pdf'],
            "prefix": ['mailto:']
        }
        
    def should_follow(self, link: str):
        do_not_follow_ending = self.follow_pattern.get('do_not_follow_endswith')
        bad_prefixes = self.follow_pattern.get('prefix')

        for bad_ending in do_not_follow_ending:
            if link.endswith(bad_ending):
                return False

        for bad_prefix in bad_prefixes:
            if link.startswith(bad_prefix):
                return False

        return True

    def orgin_normalizer():
        pass

    def path_normalizer():
        pass
