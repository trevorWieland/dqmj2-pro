#include "context.h"
int native_main_0208ff70(void){
SocketView *socket;
u32 enable;
for(;;){enable=native_fn_02007ff4();for(socket=native_data_021d15ac;socket;socket=socket->next7C){if((int)socket!=native_data_021d154c && !state(socket,16)){break;}}(void)native_fn_02008008(enable);if(!socket){break;}(void)native_fn_0208fcb0((int)socket);}
if(native_data_021d15ac==0 || ((int)native_data_021d15ac==native_data_021d154c && native_data_021d15ac->next7C==0)){if(native_data_021d15b0==0){return 0;}}
return -26;
}
