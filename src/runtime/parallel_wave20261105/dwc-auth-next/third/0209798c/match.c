#include "context.h"
DWCAuthError native_main_0209798c(void)
{
 int code;
 void*work;
 DWCAuthAlloc alloc=DWCauth->param.alloc;
 DWCAuthFree free=DWCauth->param.free;
 DWCHttp*http=DWCauth->http;
 if(native_fn_02098d0c(http,0)!=1){DWCauth->result.returncode=20100;return 14;}
 if(native_fn_02097ab0()!=0)return 14;
 if(DWCauth->result.returncode<20100){
  if(DWCauth->result.returncode==20002){
   work=alloc((u32)native_data_020debb0,0x71f);
   if(work==NULL){DWCauth->result.returncode=20100;return 2;}
   if(native_fn_020a5488(&native_data_021d18fc,(void*)(((u32)work+31)&~31UL))!=1){
    free((u32)native_data_020debc0,work,0);
    DWCauth->result.returncode=20100;
    return 15;
   }
   free((u32)native_data_020debc0,work,0);
  }
  return 21;
 }
 code=DWCauth->result.returncode;
 switch(code){
 case 20104:native_fn_020a54c0(&native_data_021d18fc);DWCauth->result.returncode=20104;return 16;
 case 20108:{
  work=alloc((u32)native_data_020debb0,0x700);
  if(work==NULL){DWCauth->result.returncode=20108;return 17;}
  native_fn_020a5458((void*)(((u32)work+31)&~31UL));
  free((u32)native_data_020debc0,work,0);
  DWCauth->result.returncode=20108;
  return 17;
 }
 default:return 18;
 }
}
