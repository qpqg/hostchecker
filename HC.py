try:
	from platform import python_version as v
	from socket import setdefaulttimeout
	from datetime import datetime as dt
	from socket import gethostbyname
	from socket import SOCK_STREAM
	from platform import system as OS
	from socket import AF_INET
	from socket import socket
	from re import findall as f
	from socket import error
	from time import sleep
	from sys import argv
	from sys import exit
except ImportError as e:
	print('[!] Module %s tidak ada bos....'%str(e).split(' ')[-1])
	exit(1)
d = {
	'hos':'',
	'met':'',
	'pro':'',
	'pay':'',
	'tim':'',
	}
hpp = 0
ppp = 0
mpp = 0
jml = ''
info = '''\rk###                                                           ###
#   \rh mmmmm  mmmmm  mmmmm  m    m   mm   mm   m  mmmm  m    m   \rk #
#   \rh #   "#   #    #   "# ##  ##   ##   #"m  # #"   "  #  #    \rk #
#   \rh #mmm#"   #    #mmmm" # ## #  #  #  # #m # "#mmm    ##     \rk #
#   \rh #        #    #   "m # "" #  #mm#  #  # #     "#  m""m    \rk #
#   \rh #      mm#mm  #    " #    # #    # #   ## "mmm#" m"  "m   \rk #
#                                                               #
#    \rm*\rkName   : \rhHostCek.py, python2, versi 0.1                  \rk #
#    \rm*\rkBy     : \rmPIRMANSX                                        \rk #
#    \rm*\rkDate   : \rhSenin 25 sep 2017                               \rk #
#    \rm*\rkGithub : \rhhttps://github.com/pirmansx                      \rk#
###                                                           ###'''
setting = '''
# Name : HostCek.py python2 versi 0.1
# By   : PIRMANSX
# BH : https://github.com/pirmansx
# Date : senin 25 sep 2017
*file setting HostCek.py*
*ket*
** 'hos' adalah calon bug tambah ';' jika cek host ganda...ato lebih
       contoh : hos=host000.com;host001.net
** 'met' adalah method tambah ';' jika cek method ganda....ato lebih
       contoh : met=GET;DELETE
** 'pro' adalah proxy:port tambah ';' jika cek proxy ganda....
       contoh : pro=111.222.333.444:1234;000.999.888.777:8080
** 'pay' adalah payload ... dimana ...
      [m] adalah method
      [h] adalah host
      [cr] adalah '\\r'
      [lf] adalah '\\n'
      [crlf] adalah '\\r\\n'
      *jika belum mahir ane saranin jangan di ubah...
** 'tim' adalah waktu habis(time out) dalam satuan detik.
      contoh: tim=3
####################################
hos=fb.com
met=PUT;GET;POST;HEAD;PATCH;TRACE;DELETE;OPTIONS;CONNECT
pro=10.8.3.8:8080
pay=[m] http://[h]/ HTTP/1.1[crlf]Host: [h][crlf][crlf]
tim=5
####################################
'''
def main():
	global d,hpp,ppp,mpp,jml
	hos = []
	pro = []
	met = []
	tamp('\rk'+'#'*65)
	tamp(info)
	tamp('\rk'+'#'*65)
	jeda(0.1)
	getset()
	cekpay()
	tamp('\rh[+]\rk payload__\rm#\rc'+d['pay'])
	tamp('\rh[+]\rk methode__\rm#\rc'+d['met'])
	tamp('\rh[+]\rk proxy____\rm#\rc'+d['pro'])
	tamp('\rh[+]\rk time out_\rm#\rc'+d['tim'])
	tamp('\rh[+] cek semua host...')
	setdefaulttimeout(int(d['tim']))
	d['pay'] = d['pay'].replace('[cr]','\r')
	d['pay'] = d['pay'].replace('[lf]','\n')
	d['pay'] = d['pay'].replace('[crlf]','\r\n')
	c = ''
	for h in d['hos'].split(';'):
		if len(h) != 0:
			if cek(h) == 1:
				if len(h) > hpp:hpp = len(h)
				hos.append(h)
	tamp('\rh[+] cek selesai...')
	if len(hos) == 0:
		tamp('\rm[!] tidak ada host yang aktif...')
		tamp('\rk'+'#'*65)
		exit(1)
	tamp('\rh[+] list host aktif...')
	for h in hos:
			tamp('\rb==> \rk'+h)
	tamp('\rh[+] cek semua respon host...')
	waktu0 = dt.now()
	for p in d['pro'].split(';'):
			p = p.replace(' ','')
			if len(p) != 0:
				if len(p) > ppp:ppp = len(p)
				pro.append(p)
	for m in d['met'].split(';'):
			m = m.replace(' ','')
			if len(m) != 0:
				if len(m) > mpp:mpp = len(m)
				met.append(m)
	jml = str(len(pro)*len(met)*len(hos))
	i = 1
	for h in hos:
		for m in met:
			for p in pro:
				pay = d['pay'].replace('[h]',h)
				pay = pay.replace('[m]',m)
				get(pay,p,h,m,str(i))
				i += 1
	waktu1 = dt.now()
	tamp('\rh[+] waktu yang di perlukan adalah')
	tamp('\rh[+] \rk'+str(waktu1-waktu0).split('.')[0])
	tamp('\rk'+'#'*65)
def jeda(i):
	try:
		sleep(i)
	except KeyboardInterrupt:
		tamp('\r\rm[!] Batal....')
		exit(1)
def cek(hos):
	try:
		try:
			ip = gethostbyname(hos)
		except KeyboardInterrupt:
			tamp('\r\rm[!] Batal....')
			exit(1)
		tamp('\rb==> \rk'+hos[:37]+'\r0'+'_'*(40-len(hos[:37]))+'\rk[\rh%s\rk]'%(' '*(15-len(ip))+ip))
		return 1
	except error:
		tamp('\rb==> \rk'+hos[:37]+'\r0'+'_'*(40-len(hos[:37]))+'\rk[\rmxxx.xxx.xxx.xxx\rk]')
		return 0
	except KeyboardInterrupt:
		tamp('\r\rm[!] batal..')
		tamp('\rk'+'#'*65)
		exit(1)
def get(pay,pro,h,m,i):
	dat = ''
	try:
		s = socket(AF_INET,SOCK_STREAM)
		s.connect((pro.split(':')[0],int(pro.split(':')[1])))
		s.send(pay)
		r = s.recv(4096)
		s.close()
		dat = r
		if len(dat) != 0:
			dat = dat.split('\r\n\r\n')[0]
			red = dat.find('Location')
			if red != -1:
				red = dat.split('Location: ')[1]
				red = red.split('\r\n')[0]
			else:
				red = 0
			dat = dat.split('\r\n')[0]
			if dat.find('HTTP/') != -1:
				dat = dat[9:]
			tampil('\rh'+dat.upper().replace(' ','_')+'\r0',h,pro,m,red,i)
		else:
			tampil('\rmRESPONE_0\r0',h,pro,m,0,i)
	except error as e:
		if str(e).find('] ') != -1:
			tampil('\rm'+str(str(e).split('] ')[1]).upper().replace(' ','_')+'\r0',h,pro,m,0,i)
		else:
			tampil('\rm'+str(e).upper().replace(' ','_')+'\r0',h,pro,m,0,i)
	except KeyboardInterrupt:
		tamp('\r\rm[!] batal...')
		tamp('\rk'+'#'*65)
		exit(1)
def getset():
	global d
	arg = argv[0].split('/')
	if len(arg) > 1:
		ps = argv[0].replace(arg[-1],'')
		ps += 'setting.txt'
	else:
		ps = 'setting.txt'
	s = 0
	get = lambda x,y:x.replace(y,'')
	try:
		file = open(ps,'r').readlines()
	except:
		tamp('\rm[!] file setting.txt tidak ada...! \n[!] pastikan file dalam satu directory(%s)...\n\rh[+] membuat file setting.txt'%ps)
		try:
			open(ps,'w').write(setting)
		except:
			tamp('\rm[!] gagal membuat file')
		tamp('\rk'+'#'*65)
		exit(1)
	for i in file:
		i = i.replace('\n','')
		for y in d:
			if i.find(y+'=') == 0:
				d[y] = get(i.replace('=',''),y)
	for i in d:
		if len(d[i]) == 0:
			tamp('\rb==>\rk '+i+'='+' \rmtidak ada....')
			s = 1
	if s == 1:
		tamp('\rm[!] file setting kurang lengkap...')
		tamp('\rk'+'#'*65)
		exit(1)
def cekpay():
	global d
	e = 0
	format = ['[h]','[m]','[cr]','[lf]','[crlf]']
	fmt = f(r'(\[.*?\])',d['pay'])
	for i in fmt:
		if i not in format:
			tamp('\rm==> \rk'+i+' \rmformat tidak di dukung....')
			e = 1
	if e == 1:
		tamp('\rm[!] payload error....')
		tamp('\rk'+'#'*65)
		exit(1)
def tampil(r,h,p,m,s,i):
	global hpp,ppp,mpp
	rpp = 26
	if len(r) > rpp:rpp = len(r)
	h = ('\rp%s\r0'%h)+'\rP'+'_'*(hpp-len(h))
	m = ('\rh%s\r0'%m)+'\rP'+'_'*(mpp-len(m))
	p = ('\rc%s\r0'%p)+'\rP'+'_'*(ppp-len(p))
	r = r+'\rP'+'_'*(rpp-len(r))
	if s == 0:
		s = '\rh'+str(s)
	else:
		s = '\rk'+str(s)
	per = '0'*(len(jml)-len(i))
	per = per+i
	tamp('\rb==> \rk[\rh%s\rk/\rh%s\rk]%s__%s__%s__%s__%s'%(per,jml,h,m,p,r,s))
def tamp(x):
	w = {
		'm':31,
		'h':32,
		'k':33,
		'b':34,
		'p':35,
		'c':36,
		'P':37}
	for i in w:
		x=x.replace('\r%s'%i,'\033[%s;1m'%w[i])
		x+='\033[0m'
	x=x.replace('\r0','\033[0m')
	print x
if __name__ == '__main__':
	if v().split('.')[0] != '2':
		print('[!] kamu menggunakan python versi %s silahkan menggunakan versi 2.x.x'%v().split(' ')[0])
		exit(1)
	if OS().upper() != 'LINUX':
		print('[!] kamu menggunakan %s silahkan menggunakan linux'%OS().upper())
		exit(1)
	main()
else:
	print('[!] ini bukan module toyol')
	exit(1)