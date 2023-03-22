import re
from ipaddress import IPv6Interface

def remove_space(line):
    return line.replace(" ", "")

def remove_semicolon(line):
    return line.replace(";", "")

terms=[]
with open("aclv6-inbound-original",'r') as file:
    for number, line in enumerate(file):
        if 'term' in line:
            terms.append(number)
#print(terms)

t = 0
#print(terms[t])
t_length = len(terms) - 2
#print(terms[t_length])

file_num = 1

while t <= t_length:
    t_low = terms[t]
    t_high = terms[t+1]
    #print(t_low, t_high)
    t_high_less1 = t_high - 1
    t+=1
    with open("aclv6-inbound-original",'r') as file:
        x = file.readlines()[t_low:t_high_less1]
        term = x[0]
        term_name=term.strip().split(' ')
        #print(term_name[1])
        with open('term%s' % file_num , 'w') as f:
            for i in x:
                f.write(i)
        file_num+=1
     
maxfile_num = file_num-1
file_num = 1

while file_num <= maxfile_num:
    src_add_num = 999999999
    dst_add_num = 999999999
    src_port = 999999999
    dst_port = 999999999
    proto = 999999999
    tcp_est = 'no'
    frag = 'no'
    src_list = []
    dst_list = []
    hop = 'no'

#GET THE NAME OF THE TERM IN THE JUNOS ACL
    with open("term%s" %file_num,'r') as file:
        for line in file:
            if 'term' in line:
                term_name=line.strip().split(' ')

#GET THE LINE NUMBER CONTAINING SOURCE-ADDRESS
    with open("term%s" %file_num,'r') as file:
        for number, line in enumerate(file):
            if 'source-address' in line:
                src_add_num = number

#GET THE LINE AT THE END OF THE DESTINATION-ADDRESSES        
    with open("term%s" %file_num,'r') as file:
        for number, line in enumerate(file):
            if '}' in line:
                src_add_end = number
                break

#PRINT THE OBJECT-GROUP NAME
    if src_add_num == 999999999:
        pass
        src_add_obj="any"
    else:
        print("object-group network ipv6 src-net-"+term_name[1])
        src_add_obj="net-group src-net-"+term_name[1]


#PRINT THE LIST OF SOURCE-ADDRESSES
    with open("term%s" %file_num,'r') as file:
        for number, line in enumerate(file):
            if src_add_num < number < src_add_end:     
                no_space = remove_space(line)
                inter = remove_semicolon(no_space)
                inter = inter.split('\n')
                inter = inter[0]
                interface = IPv6Interface(inter)
                print(interface.network)
    print("!")

#GET THE LINE NUMBER CONTAINING DESTINATION-ADDRESS
    with open("term%s" %file_num,'r') as file:
        for number, line in enumerate(file):
            if 'destination-address' in line:
                dst_add_num = number

#GET THE LINE NUMBER AT THE END OF THE DESTINATION-ADDRESSES
    with open("term%s" %file_num,'r') as file:
        for number, line in enumerate(file):
            if '}' in line:
                dst_add_end = number
                if dst_add_end > dst_add_num:
                    break

#PRINT THE OBJECT-GROUP NAME
    if dst_add_num == 999999999:
        pass
        dst_add_obj="any"
    else:
        print("object-group network ipv6 dst-net-"+term_name[1])
        dst_add_obj="net-group dst-net-"+term_name[1]

#PRINT THE LIST OF DESTINATION ADDRESSES
    with open("term%s" %file_num,'r') as file:
        for number, line in enumerate(file):
            if dst_add_num < number < dst_add_end:
                no_space = remove_space(line)
                inter = remove_semicolon(no_space)
                inter = inter.split('\n')
                inter = inter[0]
                interface = IPv6Interface(inter)
                print(interface.network)
    print("!")

#GET PROTOCOL
    with open("term%s" %file_num,'r') as file:
        for line in file:
            if 'next-header' in line:
                protocol=line.strip().split(' ')
                proto=remove_semicolon(protocol[1])

#GET SOURCE-PORT NUMBER(S)
    with open("term%s" %file_num,'r') as file:
        for line in file:
            if 'source-port' in line:
                source_port=line.strip().split(' ')
                src_port=remove_semicolon(source_port[1])
                if src_port == '[':
                    src_list=source_port[:-1]
                    src_list=src_list[+2:]
                    index=0
                    for src in src_list:
                        index+=1
                        if '-' in src:
                            src_port_sub_range=src.split('-')
                            src_port_sub_low=src_port_sub_range[0]
                            src_port_sub_high=src_port_sub_range[1]
                            src_list[index-1]='range %s %s' %(src_port_sub_low, src_port_sub_high)

#PRINT THE OBJECT-GROUP NAME
    if src_port == 999999999:
        pass
    else:
        print("object-group port src-port-"+term_name[1])
        src_port_obj="port-group src-port-"+term_name[1]

#PRINT THE PORT NUMBERS
    if src_port == 999999999:
        pass
    elif len(src_list) > 0:
        for src in src_list:
            if "range" in src:
                print(src)
            else:
                print("eq",src)
    elif '-' in src_port:
        src_port_range=src_port.split('-')
        src_port_low=src_port_range[0]
        src_port_high=src_port_range[1]
        print(" range",src_port_low,src_port_high)
    else:
        print(' eq',src_port)

    print("!")

#GET DESTINATION-PORT NUMBER(S)
    with open("term%s" %file_num,'r') as file:
        for line in file:
            if 'destination-port' in line:
                dest_port=line.strip().split(' ')
                dst_port=remove_semicolon(dest_port[1])
                if dst_port == '[':
                    dst_list=dest_port[:-1]
                    dst_list=dst_list[+2:]
                    index=0
                    for dst in dst_list:
                        index+=1
                        if '-' in dst:
                            dst_port_sub_range=dst.split('-')
                            dst_port_sub_low=dst_port_sub_range[0]
                            dst_port_sub_high=dst_port_sub_range[1]
                            dst_list[index-1]='range %s %s' %(dst_port_sub_low, dst_port_sub_high)


#PRINT THE OBJECT-GROUP NAME
    if dst_port == 999999999:
        pass
    else:
        print("object-group port dst-port-"+term_name[1])
        dst_port_obj="port-group dst-port-"+term_name[1]    

#PRINT THE PORT NUMBERS
    if dst_port == 999999999:
        pass
    elif len(dst_list) > 0:
        for dst in dst_list:
            if "range" in dst:
                print(dst)
            else:
                print("eq",dst)

    elif '-' in dst_port:
        dst_port_range=dst_port.split('-')
        dst_port_low=dst_port_range[0]
        dst_port_high=dst_port_range[1]
        print(" range",dst_port_low,dst_port_high)
    else:
        print(' eq',dst_port)

    print("!")

#CHECK IF THE TERM IS A PERMIT OR A DENY
    with open("term%s" %file_num,'r') as file:
        for line in file:
            if "discard" in line:
                action='deny'
                break
            else:
                action='permit'

    if proto == 'icmpv6':
        with open("term%s" %file_num,'r') as file:
            for line in file:
                if "icmp-type" in line:
                    if "[" in line:
                        icmp_type=line.split('[')
                        icmp_type=icmp_type[1].split(']')
                        icmp_type=icmp_type[0].split(' ')
                        icmp_type=icmp_type[:-1]
                        icmp_type=icmp_type[+1:]
                        for i in icmp_type:
                            print('ipv6 access-list ACLv6-INBOUND',action,proto,src_add_obj,dst_add_obj,i)
                    else:
                        icmp_type=line.split(';')
                        icmp_type=icmp_type[0].split(' ')
                        icmp_typel=(len(icmp_type))-1
                        i=icmp_type[icmp_typel]
                        print('ipv6 access-list ACLv6-INBOUND',action,proto,src_add_obj,dst_add_obj,i)

    if proto == 'tcp':
        with open("term%s" %file_num,'r') as file:
            for line in file:
                if "tcp-established" in line:
                    tcp_est='established'

    if proto == 'fragment':
        frag='fragments'
        proto='ipv6'

    if proto == 'hop-by-hop':
        hop='hop'
        proto='ipv6'


    if proto == 999999999:
        if frag == 'fragments':
            print('ipv6 access-list ACLv6-INBOUND',action,"ipv6",src_add_obj,dst_add_obj,"fragments")
        else:
            print('ipv6 access-list ACLv6-INBOUND',action,"ipv6",src_add_obj,dst_add_obj)
    elif proto == 'icmpv6':
        pass
    elif (dst_port == 999999999 and src_port == 999999999):
        if tcp_est == 'established':
            print('ipv6 access-list ACLv6-INBOUND',action,proto,src_add_obj,dst_add_obj,"established")
        elif frag == 'fragments':
            print('ipv6 access-list ACLv6-INBOUND',action,proto,src_add_obj,dst_add_obj,"fragments")
        elif hop == 'hop':
            print('ipv6 access-list ACLv6-INBOUND',action,proto,src_add_obj,dst_add_obj,"hop-by-hop")   
        else:
            print('ipv6 access-list ACLv6-INBOUND',action,proto,src_add_obj,dst_add_obj)
    elif dst_port == 999999999:
        if tcp_est == 'established':
            print('ipv6 access-list ACLv6-INBOUND',action,proto,src_add_obj,src_port_obj,dst_add_obj,"established")
        elif frag == 'fragments':
            print('ipv6 access-list ACLv6-INBOUND',action,proto,src_add_obj,src_port_obj,dst_add_obj,"fragments")
        elif hop == 'hop':
            print('ipv6 access-list ACLv6-INBOUND',action,proto,src_add_obj,src_port_obj,dst_add_obj,"hop-by-hop")
        else:
            print('ipv6 access-list ACLv6-INBOUND',action,proto,src_add_obj,src_port_obj,dst_add_obj)
    elif src_port == 999999999: 
        if tcp_est == 'established':
            print('ipv6 access-list ACLv6-INBOUND',action,proto,src_add_obj,dst_add_obj,dst_port_obj,"established")
        elif frag == 'fragments':
            print('ipv6 access-list ACLv6-INBOUND',action,proto,src_add_obj,dst_add_obj,dst_port_obj,"fragments")
        elif hop == 'hop':
            print('ipv6 access-list ACLv6-INBOUND',action,proto,src_add_obj,dst_add_obj,dst_port_obj,"hop-by-hop")
        else:
            print('ipv6 access-list ACLv6-INBOUND',action,proto,src_add_obj,dst_add_obj,dst_port_obj)
    else:
        if tcp_est == 'established':
            print('ipv6 access-list ACLv6-INBOUND',action,proto,src_add_obj,src_port_obj,dst_add_obj,dst_port_obj,"established")
        elif frag == 'fragments':
            print('ipv6 access-list ACLv6-INBOUND',action,proto,src_add_obj,src_port_obj,dst_add_obj,dst_port_obj,"fragments")
        elif hop == 'hop':
            print('ipv6 access-list ACLv6-INBOUND',action,proto,src_add_obj,src_port_obj,dst_add_obj,dst_port_obj,"hop-by-hop")
        else:
            print('ipv6 access-list ACLv6-INBOUND',action,proto,src_add_obj,src_port_obj,dst_add_obj,dst_port_obj)
    
    file_num+=1
