#include "context.h"
void native_main_02094600(u32 name, void *ptr, s32 size)
{
  tagACHOLD *myAcHold;
  
  myAcHold = (tagACHOLD *)DWCi_AC_GetMemPtr(1);
  if ((myAcHold != (tagACHOLD *)0x0) && ((myAcHold->allocState & name) != 0)) {
    myAcHold->allocState = myAcHold->allocState & ~name;
    (*myAcHold->free)(name,ptr,size);
    if (name == 1) {
      acHold = (tagACHOLD *)0x0;
    }
  }
  return;
}
