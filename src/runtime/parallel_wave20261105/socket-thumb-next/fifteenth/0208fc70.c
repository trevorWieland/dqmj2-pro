#include "context.h"
int native_main_0208fc70(void *arg){
CommandView *command=(CommandView *)arg;
SocketView *socket=command->socket4;
if(tcp(socket)){native_fn_0208d8e8();}
return 0;
}
