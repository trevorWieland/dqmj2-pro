#include "context.h"
int native_main_02098f14(DWCHttp*http,char*label,char*buffer,unsigned long size){char*value=native_fn_02098ed8(http,label);u32 result;if(!value)return 0;result=native_fn_0209a83c(value,native_fn_0201d69c(value),buffer,size);if(result!=0xffffffff&&result<size)buffer[result]=0;return result;}
