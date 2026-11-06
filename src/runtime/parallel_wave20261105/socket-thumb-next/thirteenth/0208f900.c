#include "context.h"
s32 native_main_0208f900(SocketView *socket){
SendView *send=socket->send68;
s32 size,in,out,available;
size=(s32)send->sizeF8;in=(s32)send->in100;out=(s32)send->out102;
available=out-in-1;if(available<0){available+=size;}return available;
}
