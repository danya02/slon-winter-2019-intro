#!/usr/bin/python3
import init
import logging
logging.basicConfig(level=logging.DEBUG)
l=logging.getLogger(__name__)
class Person:
    def __init__(self, user_id, friends_recursion=0,no_update_self=False):
        self.id=user_id
        self.first_name=...
        self.last_name=...
        self.screen_name=...
        self.friends=...
        if not no_update_self:
            self.update_self()
        if friends_recursion>0:
            self.update_friends(friends_recursion)
    def update_self(self):
        l.debug('Hitting VK for info on user id_{}...'.format(self.id))
        try:
            obj = init.api.users.get(user_ids=self.id,fields='screen_name')[0]
            self.first_name=obj['first_name']
            self.last_name=obj['last_name']
            self.screen_name=obj['screen_name']
        except init.vk_api.VkApiError:
            l.exception('Failed to get info for user id_{}!'.format(self.id))
    def update_friends(self, depth=0):
        l.info('Updating friends with depth {}!'.format(depth))
        l.debug('Looking at friends of user id_{}...'.format(self.id))
        try:
            for i in init.api.friends.get(user_id=self.id,fields='screen_name')['items']:
                p=Person(i['id'],depth-1,True)
                if self.friends is ...:
                    self.friends=[]
                if 'deactivated' not in i:
                    p.first_name=i['first_name']
                    p.last_name=i['last_name']
                    p.screen_name=i['screen_name']
                    self.friends.append(p)
        except init.vk_api.VkApiError:
            l.exception('Getting friends failed!')
    def print_recursive(self,started_from,limit_depth=None,current_depth=0):
        if current_depth==limit_depth:
            print(f'{" "*current_depth}{self.first_name} {self.last_name} (@{self.screen_name}, id_{self.id}).')
            return 0
        print(f'{" "*current_depth}{self.first_name} {self.last_name} (@{self.screen_name}, id_{self.id})' + (f' has {len(self.friends) if isinstance(self.friends, list) else "an unknown number of"} friend{"" if isinstance(self.friends, list) and len(self.friends)==1 else "s"}{":" if isinstance(self.friends, list) and len(self.friends)>0 else "."}' if self.friends is not ... else '.'))
        if isinstance(self.friends, list) and len(self.friends)>0:
            for i in self.friends:
                i.print_recursive(started_from,limit_depth if self.id not in started_from else current_depth+1, current_depth+1)

    def test_paradox(self):
        l.info(f'{self.first_name} {self.last_name} (@{self.screen_name}, id_{self.id}) has {len(self.friends)} friend{"" if len(self.friends)==1 else "s"}.')
        s=0
        c=0
        for i in self.friends:
            if i.friends is not ...:
                s+=len(i.friends)
                c+=1
        l.info(f'Of those, the friend counts could be acquired for {c} friends.')
        l.info(f'In total, those friends have {s} friends including the origin.')
        avg=s/c
        l.info(f'This results in {avg} friends per friend, which is {"more" if avg>len(self.friends) else "less"} than the origin\'s friend count.')
        l.warn(f'The paradox {"checks out" if avg>len(self.friends) else "does not check out"}.')

if __name__=='__main__':
    me = Person(input('Your ID:'),2)
    s=[]
    me.print_recursive(s)
    me.test_paradox()
    
