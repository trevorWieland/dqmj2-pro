#include "context.h"
void native_main_02092380(SocketView *socket)
{
    ConnectionView *context=socket->ssl;
    u8 *buffer=native_data_021cfd0c(131);
    s32 length;
    if(!buffer){context->state=9;return;}
    buffer[0]=20;buffer[1]=3;buffer[2]=0;buffer[3]=0;buffer[4]=1;buffer[5]=1;
    native_fn_02008d78(context->send_sequence,0,8);
    buffer[6]=22;buffer[7]=3;buffer[8]=0;buffer[9]=0;buffer[10]=40;
    buffer[11]=20;buffer[12]=0;buffer[13]=0;buffer[14]=36;
    native_fn_02008e0c(&context->md5live,&context->md5tmp,88);
    native_fn_02091a68(context,buffer+15,0);
    native_fn_02008e0c(&context->md5tmp,&context->md5live,88);
    native_fn_02008e0c(&context->sha1live,&context->sha1tmp,92);
    native_fn_02091afc(context,buffer+31,0);
    native_fn_02008e0c(&context->sha1tmp,&context->sha1live,92);
    native_fn_02091f98(context,buffer+11,40);
    length=native_fn_02091de0(context,buffer+6);
    native_fn_0208db64(buffer,length+6,0,0,socket);
    native_data_021cfd38(buffer);
}
