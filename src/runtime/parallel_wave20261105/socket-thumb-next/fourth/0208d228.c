#include "context.h"
void native_main_0208d228(IPHeader *ip,DatagramHeader *packet,u32 bytes)
{
    u32 level;
    ThreadView *thread;
    if(packet->checksum6 && native_fn_0208bbac(packet,bytes,ip,17))return;
    level=native_fn_02007ff4();
    for(thread=native_data_020e33e4.list8;thread;thread=thread->next68){
        SocketView *socket=thread->socketA4;
        if(!socket || !socket->owner0 || socket->state8!=10 || socket->localA!=host16(packet->destination2))continue;
        if(socket->remote18 && socket->remote18!=host16(packet->source0))continue;
        if(socket->address1C && socket->address1C!=0xffffffff && socket->address1C!=host32(ip->sourceC))continue;
        socket->localIP14=host32(ip->destination10);
        if(!socket->address1C){socket->address1C=host32(ip->sourceC);socket->remote18=host16(packet->source0);}
        if(socket->size44)break;
        bytes-=8;
        if(bytes>socket->capacity3C)socket->size44=socket->capacity3C;
        else socket->size44=bytes;
        native_fn_02008e0c(packet+1,socket->buffer40,socket->size44);
        if(socket->kind4==3){socket->kind4=0;native_fn_0200698c(socket->owner0);}
        else if(socket->callback38 && socket->callback38(socket->buffer40,socket->size44,socket))socket->size44=0;
        break;
    }
    native_fn_02008008(level);
}
