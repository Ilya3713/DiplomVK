import requests
import time
from pprint import pprint

TOKEN = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'
ID_eshmargunov = '171691064'

class VK_user:
  def __init__(self,token,ID):
      self.token=token
      self.ID=ID

  def get_params(self):
      return{
          'access_token':self.token,
          'v':'5.52',
          'user_id': self.ID,
          'order':'hints',
          'name_case' :'nom',
          'ref' :'255',
          'fields' :'nickname'
      }

  def request(self,method,params):
      response = requests.get(
          'https://api.vk.com/method/'+method,
          params=params
      )
      print('.')
      return(response)


  def get_groups(self):
      response = self.request('groups.get',
                              params={
                                  'access_token':self.token,
                                  'v':'5.52',
                                  'user_id':self.ID,
                                  'extended': 1})
      time.sleep(1)
      return(response.json()['response']['items'])
  def get_friends(self):
      params=self.get_params()
      response=self.request(
          'friends.get',
          params=params
      )
      dict_of_fr = response.json()['response']['items']
      friends_list = []
      for friend in dict_of_fr:
          friends_list.append(friend['id'])
      return (friends_list)

def get_friends_group(token,id):
  user = VK_user(token, id)
  friends_list=[]
  groups_list=[]
  friends_groups_ID_list=[]

  for friend_id in user.get_friends():
      friends_list.append(VK_user(token, friend_id))
  for friend in friends_list:
      try:
          groups_list.append(friend.get_groups())
      except:
          continue
  for groups in groups_list:
      for group in groups:
          try:
              friends_groups_ID_list.append(group['id'])
          except:
              continue
  set_of_friend_group_ID=set(friends_groups_ID_list)
  return (set_of_friend_group_ID)

def get_group_id(token, id):
    user = VK_user(token,id)
    list_of_groups_ID = []
    for group in user.get_groups():
        list_of_groups_ID.append(group['id'])
        set_of_groups_ID=set(list_of_groups_ID)
    return (set_of_groups_ID)


if __name__ == '__main__':
  result = []
  eshmargunov = VK_user(TOKEN,ID_eshmargunov)
  result_list = get_group_id(TOKEN,ID_eshmargunov) - get_friends_group(TOKEN,ID_eshmargunov)
  for group in eshmargunov.get_groups():
      if group['id'] in result_list:
          result.append(group)
  pprint(result)
