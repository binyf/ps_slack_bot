#%%
import requests
from bs4 import BeautifulSoup
import re
for i in range(16,31):
        j = 1
        p_list = []
        while True:
                res = requests.get('https://solved.ac/problems/level/'+str(i),params='page='+str(j))
                soup = BeautifulSoup(res.text, 'html.parser')
                a = soup.find_all('div', {'class':'Paginationstyles__PageIndicator-sc-bdna5c-0 Paginationstyles__PageIndicatorCurrent-sc-bdna5c-1 fiXRLB eGsWbp'})
                if a == []:
                        break
                values = []
                for tag in soup.find_all('span'):
                        if len(str(tag)) <= 18:
                                values.append(str(tag))
                for k in range(len(values)):
                        values[k] = re.sub(r'[^0-9]','',values[k])
                values = [v for v in values if v!='']
                p_list.extend(values)
                j += 1
        f = open('./problems/'+str(i)+'.txt','w')
        f.write(' '.join(p_list))
        f.close
        print(i, p_list)
# %%
