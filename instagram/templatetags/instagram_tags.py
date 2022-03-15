from django import template

register = template.Library()

# 다음과 같은 형식으로 써주면 됨
# def cut(value, arg):
#     """Removes all values of arg from the given string"""
#     return value.replace(arg, '')

@register.filter
def is_like_user(post,user):
  return post.is_like_user(user)
  #인자를 넣어서 반환할 수 있게 됨