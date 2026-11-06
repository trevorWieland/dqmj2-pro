#include "context.h"
void native_main_02092b50(SocketView *socket)
{
    u8 temporary[27];
    ConnectionView *context=socket->ssl;
    if(context->state==8){
        temporary[0]=21;temporary[1]=3;temporary[2]=0;temporary[3]=0;
        temporary[4]=2;temporary[5]=1;temporary[6]=0;
        native_fn_0208db64(temporary,native_fn_02091de0(context,temporary),0,0,socket);
    }
    context->state=0;
}
