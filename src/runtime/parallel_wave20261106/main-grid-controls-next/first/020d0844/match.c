#include "context.h"
u32 native_main_020d0844(u32 a,u32 b,u32 c)
{
 s32 page,limit;
 u32 total,result;
 s32 x,y;
 native_data_main_021d6b5c.previousPage=native_data_main_021d6b5c.page;
 page=native_data_main_021d6b5c.page;
 result=native_fn_020c1a04(208,40,&page,native_fn_020d0a24());
 native_data_main_021d6b5c.page=(u8)page;
 total=native_fn_020629e0();
 if(native_data_main_021d6b5c.page!=native_data_main_021d6b5c.previousPage&&result){
  native_fn_020d0218(a,b,c);
  if((s32)(native_fn_020d0210(total)-1)<=0)limit=0;else limit=native_fn_020d0210(total)-1;
  x=(s8)native_data_main_021d6b64.x;
  if(x>=limit){if((s32)(native_fn_020d0210(total)-1)<=0)x=0;else x=native_fn_020d0210(total)-1;}
  native_data_main_021d6b64.x=(u8)x;
  if((s32)(native_fn_020d0208(total)-1)<=0)limit=0;else limit=native_fn_020d0208(total)-1;
  y=native_data_main_021d6b64.y;
  if(y>=limit){if((s32)(native_fn_020d0208(total)-1)<=0)y=0;else y=native_fn_020d0208(total)-1;}
  native_data_main_021d6b64.y=y;
  native_fn_0205e7a8(-1,86);
 }
 native_data_main_021d6b5c.previousPage=native_data_main_021d6b5c.page;
 return result;
}
