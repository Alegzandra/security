from subprocess import *
from socket import *
from visual import *

prose = label() # initially blank text

def check_list_for_start(list,prefix):
    """will return the index of the element starting with prefix"""
    index = 0
    while index<len(list)-1:
        if list[index].startswith(prefix):
            return index
        index = index+1
    return len(list)

def traceroute(ipd):
    """tracert in cmd"""
    output = check_output(["tracert", ipd])
    output_route = output.splitlines()
    iph = gethostname()
    route.append(iph)
    index = 4
    while index<len(output_route)-2:
        ip = output_route[index].split('  ').pop()
        if ip[-1]!='.':
            route.append(ip)
        index=index+1
    printroute()
    prose.text=''

def printroute():
    """this function creates spheres at network hops"""
    index=len(hosts)
    iph=gethostname()
    traces=route.count(iph)-1
    start=index-1
    while index < len(route):
        hosts.append([sphere(radius=0.2,color =(1,0,0), pos=((index-5),0,0)),arrow(pos=((index-5),0,0)), label(pos=((index-5),0,0), text=route[index],yoffset=2,height=8)])
        index = index+1

def clicksphere(evt):
    """when clicking the first sphere will run netstat, for the next ones nmap, which must be downloaded from nmap.org"""
    target_host = evt.pick
    ports_pos = evt.project(normal=(0,0,1))
    if ports_pos and target_host:
        for index in range(len(hosts)):
            if hosts[index][0] == target_host:
                hosts[index][0].color = color.blue
                target_ip=hosts[index][2].text.split()[0]
                print 's-a apasat pe bila',index,', ', hosts[index][2].text
                if index == 1:
                    netstat(target_ip,ports_pos)
                else:
                    nmap(target_ip,ports_pos)

def netstat(target_ip,ports_pos):
    output = check_output(["netstat","-a","-p","TCP"])
    print 'netstat',output
    label(pos=ports_pos,text=output,height=8,yoffset=-5)
    
def nmap(target_ip,ports_pos):
    output = check_output(["nmap","-sS",target_ip])
    output_port = output.splitlines()
    ports = list()
    index = check_list_for_start(output_port,"Host is up")+1
    while index<len(output_port)-1:
        port = output_port[index]
        if port=='':
            break
        ports.append(port)
        index = index+1
    print output
    label(pos=ports_pos,text='\n'.join(ports),height=8,yoffset=-2)

def keyInput(evt):
    s = evt.key
    if len(s) == 1:
        if s == '\n':
            traceroute(prose.text)
        else:
            prose.text += s # append new character
    elif ((s == 'backspace' or s == 'delete') and
            len(prose.text)) > 0:
        if evt.shift:
            prose.text = '' # erase all text
        else:
            prose.text = prose.text[:-1] # erase letter

route = list()
hosts = list()
host_ip = gethostname()
hosts.append([label(text='insert web address here',yoffset=20,line=false)])
scene.bind('keydown', keyInput)
scene.bind('click', clicksphere)


