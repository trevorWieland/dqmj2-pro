from wave20261105_socket_thumb_next_eighteenth_models import fixtures,scenario


def selected(name,maximum=4,predicate=None,**fields):
    out=[]
    for ordinal,f in enumerate(fixtures(name)):
        if not all(f.get(k)==v for k,v in fields.items()):continue
        if predicate is not None and not predicate(f,scenario(name,f,ordinal)):continue
        out.append(f)
        if len(out)>=maximum:break
    return out


def cases():
    return [
     ('0208ff04','lost-requested-IP-cache','native_data_021d1544==0','native_data_021d1544!=0',1,selected('0208ff04',requested=0)),
     ('0208ff04','wrong-cleanup-delay','native_fn_02006b7c(100)','native_fn_02006b7c(99)',1,selected('0208ff04',waits=1)),
     ('0208ff04','lost-zero-cleanup-success','if(result>=0)','if(result>0)',1,selected('0208ff04',result=0)),
     ('0208ff04','wrong-owned-LAN-gate','if(!native_data_020de7cc->lan28)','if(native_data_020de7cc->lan28)',1,selected('0208ff04',result=0,lan=False)),
     ('0208ff04','lost-config-reset','native_data_020de7cc=0','native_data_020de7cc=(ConfigView *)1',1,selected('0208ff04',result=0)),
     ('0208ff70','wrong-close-pending-bit','state(socket,16)','state(socket,8)',1,selected('0208ff70',predicate=lambda f,p:f['count'] and f['skip'])),
     ('0208ff70','lost-cached-list-IRQ','native_fn_02008008(enable)','native_fn_02008008(0)',1,selected('0208ff70')),
     ('0208ff70','wrong-closed-object','native_fn_0208fcb0((int)socket)','native_fn_0208fcb0(0)',1,selected('0208ff70',predicate=lambda f,p:any(a['address']==0x0208fcb0 for a in p['actions']))),
     ('0208ff70','lost-trash-empty-check','native_data_021d15b0==0','native_data_021d15b0!=0',1,selected('0208ff70',count=0)),
     ('0208ffdc','lost-fresh-UDP-send','native_fn_0208fc90(native_data_021d154c)','native_fn_0208fc90(0)',1,selected('0208ffdc',udp=True,allResult=0,mutate=True)),
     ('0208ffdc','lost-global-UDP-reset','native_data_021d154c=0','native_data_021d154c=1',1,selected('0208ffdc',udp=True,allResult=0,closed=1)),
     ('0208ffdc','wrong-scavenger-null','native_fn_0208b568(0)','native_fn_0208b568((void *)1)',1,selected('0208ffdc',udp=False,scavenge=1)),
     ('0209026c','wrong-owner-pointer','return next;','return &t->next7C;',1,selected('0209026c',count=2,target=1)),
     ('02090294','lost-signed-invalid-socket','((int)socket<=0)','((u32)socket==0)',1,selected('02090294',value=0xffffffff)),
     ('020902f0','wrong-bind-port-endian','SWAP16(address->port2)','address->port2',1,selected('020902f0',port=0x1234)),
     ('020902f0','wrong-bind-socket-word','native_fn_0208ef98(value,','native_fn_0208ef98(0,',1,selected('020902f0')),
     ('02090310','wrong-connect-IP-endian','SWAP32(address->address4)','address->address4',1,selected('02090310',ip=0x12345678)),
     ('02090350','wrong-read-flags','length,0,0,0','length,0,0,1',1,selected('02090350')),
     ('02090378','lost-zero-recv-success','result>=0 && from','result>0 && from',1,selected('02090378',result=0,null=False)),
     ('02090378','wrong-recv-port-endian','SWAP16(port)','port',1,selected('02090378',result=7,null=False)),
     ('02090378','wrong-recv-IP-endian','SWAP32(ip)','ip',1,selected('02090378',result=7,null=False)),
     ('020903d0','wrong-write-flags','length,0,0,0','length,0,0,1',1,selected('020903d0')),
     ('020903f8','wrong-send-port-endian','SWAP16(address->port2)','address->port2',1,selected('020903f8',null=False,port=0x1234)),
     ('020903f8','wrong-send-null-port','port=0;ip=0','port=1;ip=0',1,selected('020903f8',null=True)),
     ('020904ec','wrong-invalid-name-error','return -39','return -38',1,selected('020904ec',null=True)),
     ('020904ec','wrong-sockaddr-size','address->length0=sizeof(AddressView)','address->length0=4',1,selected('020904ec',null=False)),
     ('020904ec','lost-zero-IP-port-reset','localPort=0;','localPort=1;',1,selected('020904ec',null=False,ip=0)),
     ('02090554','wrong-host-ID-endian','(long)SWAP32(host)','(long)host',1,selected('02090554',ip=0x12345678)),
     ('02090580','wrong-second-DNS-source','SWAP32(*second)','SWAP32(*first)',1,selected('02090580',alias=False,predicate=lambda f,p:f['ip']!=f['ip2'])),
     ('02090608','wrong-allocator-name','allocateC(0,total)','allocateC(1,total)',1,selected('02090608')),
     ('02090608','wrong-header-size','size+sizeof(s32)','size+sizeof(s32)+4',1,selected('02090608',null=False)),
     ('02090608','lost-stored-allocation-size','memory[0]=total','memory[0]=total+1',1,selected('02090608',null=False)),
     ('02090624','wrong-release-name','release4(0,','release4(1,',1,selected('02090624',null=False)),
     ('02090624','wrong-release-size','(void *)memory,memory[0]','(void *)memory,memory[0]+1',1,selected('02090624',null=False)),
     ('0209063c','wrong-DHCP-flag-equality','config->flagC==1','config->flagC!=0',1,selected('0209063c',flag=2)),
     ('0209063c','wrong-startup-IP-order','SWAP32(config->address10)','config->address10',1,selected('0209063c',index=2)),
     ('0209063c','wrong-command-maximum','commandMax20=64','commandMax20=63',1,selected('0209063c')),
     ('0209063c','wrong-MTU-source','mtu30=config->mtu2C','mtu30=config->window30',1,selected('0209063c')),
     ('0209063c','wrong-window-source','window34=config->window30','window34=config->mtu2C',1,selected('0209063c'))]
