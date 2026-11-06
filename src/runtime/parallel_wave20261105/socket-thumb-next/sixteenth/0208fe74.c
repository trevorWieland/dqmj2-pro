#include "context.h"
void native_main_0208fe74(void *argument){
PipeView *pipe=(PipeView *)argument;
CommandHeader *command;
u32 enable;
if(pipe==0){return;}
native_fn_02006890(pipe->thread20);
enable=native_fn_02007ff4();(void)native_fn_02006c70();
while(native_fn_02006eb8(pipe->queue0,(void *)&command,0)){if(command){if(command->response8){(void)native_fn_02006e24(command->response8,(void *)-11,0);}native_fn_0208ebfc(command);}}
(void)native_fn_02006ca4();native_fn_020069dc();(void)native_fn_02008008(enable);
}
