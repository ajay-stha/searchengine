def get_domain(url):
	if('://' in url):
		val=url.index(':')
		n_st=url[val+3:]
		st_n=url[:val+3]
		try:
			check=n_st[n_st.index('/'):]
			n_st=n_st[:n_st.index('/')+1]
		except:
			n_st=n_st+'/'
			check=''
		base_url=st_n+n_st
		print(base_url)
		return base_url
	elif ('www' in url and '://' not in url):
		try:
			if('/' not in url):
				if('?' in url):
					return url[:index('?')]+'/'
				else:
					return url+'/'
			else:
				base_url=url[:url.index('/')+1]
				print(base_url)
				return base_url
		except:
			return url
	else:
		print(url)
		raise("Invalid url : should begin with http:// or www.")


def integrate_link(base_url,urls):
	ses1=[]
	c=0
	if(isinstance(urls,list)==True):
		for link in urls:
			if(c>=50):
				return ses1
			if(len(link)>1):
				if(link[0:2]=='//'): #later use regx
					link=link[2:]
				if(link[0]=='?'):
					link=base_url[:-1]+link
				elif(link[0]=='/'):
					print(link)
					link=base_url + link[1:]

				ses1.append(link)
				c+=1
		return ses1
	else:
		if(isinstance(urls,str)):
			link=urls
			if(link[0]=='?' or link[0]=='/'):
				try:
					link=base_url + link[1:]
				except IndexError:
					pass
			return link
	return ses1
