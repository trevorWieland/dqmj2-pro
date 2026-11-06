#include "context.h"
void native_main_020d0bfc(GridHandleView*handle)
{
 s32 x,y,index;
 for(index=0;index<12;index++){
  native_fn_020cfa78(index,&x,&y);
  native_fn_02045dc4(handle->byte10,handle->byte11,(u8)(x/8),(u8)(y/8),2,2);
 }
}
