#include "context.h"
void native_ov001_0220ac9c(s32 index,const void *data,u16 code,s16 position,u8 arg4,s8 arg5){
 ResourceView *resource=native_fn_02049ad0(index)->field0->field4;
 u16 buffer[4];
 native_fn_02049ffc(resource);
 native_fn_02008be0(0,buffer,8);
 if(code==0)buffer[0]=0x3000;
 else buffer[0]=native_data_020dbc18[(u16)(code+13)+0x17b];
 native_fn_02087a48(resource,0,position,arg4,1,buffer);
 native_fn_02087a48(resource,0,position+8,arg4,arg5,data);
 native_fn_02086b14(resource,0);
}
