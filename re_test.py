import re

a = '<img src="https://i10.hoopchina.com.cn/hupuapp/bbs/37443720627879/thread_37443720627879_20180912153233_s_6874855_w_415_h_415_20106.gif" data-w="415" data-h="415">'

rel = re.compile(r'.*\.gif" data-w=.*')

print(rel.match(a))