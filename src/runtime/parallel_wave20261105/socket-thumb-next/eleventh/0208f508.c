#include "context.h"
int native_main_0208f508(SocketView *socket){
RecvView *receive=socket->recv64;
ReadCommand *command;
s32 result;
if(receive->consumedF8<(s32)receive->minFC){return 0;}
command=native_fn_0208ebd8(native_fn_0208f540,socket,0);
if(command==0){return -33;}
result=native_fn_0208eca4(socket,command);
return result;
}
