from django.test import TestCase

# Create your tests here.
# 首先调用getGoogleAPI获取出Google搜索的数据，拿到数据之后跟数据库数据进行对比，
#       如果数据库存在数据，则返回数据库中的数据放入容器，否则创建数据并直接放进容器中

# 再次请求
# 传一个website参数
#       首先抓取网站本身源码，从中捕获电话及邮箱
#               如果网站本身未捕获到邮箱或者电话则开始Google查询
