import vk

class Group:
    def __init__(self, group_id, access_token, max_posts=1100):
        self._api = vk.API(vk.Session(access_token=access_token), v='5.69')
        
        if isinstance(group_id, str):
            group_id = self._api.groups.getById(
                group_id=group_id,
                fields=["id"]
            )[0].get("id")
        
        self._group_id = group_id
        self._owner_id = group_id * -1
        self._max_posts = max_posts
        
        self._posts, self._members = None, None
    
    def _get(self, count: int, get_items: callable, max_number=float("inf")):
        items, offset = True, 0
        while items and offset <= max_number:
            items = get_items(
                offset=offset,
                count=count
            )
            offset = offset + count
            yield from items
    
    def _get_members(self, count=1000, offset=0, fields=("sex", "bdate", "city")):
        return self._api.groups.getMembers(
            group_id=self._group_id,
            count=count,
            offset=offset,
            fields=fields
        ).get("items", [])
    
    def _get_members_count(self):
        return self._api.groups.getMembers(
            group_id=self._group_id,
            count=1
        ).get("count", 0)
        
    def _get_posts(self, count=100, offset=0, filter_="owner"):
        return self._api.wall.get(
            owner_id=self._owner_id,
            count=count,
            offset=offset,
            filter=filter_,
            extended=0,
        ).get("items", [])
    
    def _get_posts_count(self, filter_="owner"):
        return self._api.wall.get(
            owner_id=self._owner_id,
            count=1,
            filter=filter_,
        ).get("count", 0)
 
    def posts(self):
        return self._get_posts_count(), self._get(100, self._get_posts, self._max_posts)

    def members(self):
        return self._get_members_count(), self._get(1000, self._get_members)

    @property
    def owner_id(self):
        return self._owner_id

    @property
    def max_posts(self):
        return self._max_posts
