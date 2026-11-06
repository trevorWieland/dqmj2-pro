#include "context.h"
int native_main_0208fcb0(int value){
SocketView *socket=(SocketView *)value;
CommandView *command;
if((int)socket<=0){return -28;}
if(native_fn_020902b4(socket)){return -26;}
if(native_fn_02090294(socket)){return 0;}
if(!created(socket)){return -39;}
if(state(socket,16)){return -26;}
socket->state70|=24;
if(tcp(socket)){(void)native_fn_0208ec1c(socket->send68,0);}
command=native_fn_0208ebd8(native_fn_0208fd4c,socket,1);
command->response8=0;
(void)native_fn_0208ec50(socket,command);
return 0;
}
