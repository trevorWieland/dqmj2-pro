#include "context.h"
void native_main_0209463c(void)
{
  tagACHOLD *myAcHold;
  void *ptr;
  
  myAcHold = (tagACHOLD *)DWCi_AC_GetMemPtr(1);
  if (myAcHold != (tagACHOLD *)0x0) {
    if ((myAcHold->allocState & 0x10) != 0) {
      ptr = (void *)DWCi_AC_GetMemPtr(0x10);
      myAcHold->allocState = myAcHold->allocState & ~16;
      (*myAcHold->free)(0x10,ptr,0xd18);
    }
    if ((myAcHold->allocState & 8) != 0) {
      ptr = (void *)DWCi_AC_GetMemPtr(8);
      myAcHold->allocState = myAcHold->allocState & ~8;
      (*myAcHold->free)(8,ptr,0xc);
    }
    if ((myAcHold->allocState & 4) != 0) {
      ptr = (void *)DWCi_AC_GetMemPtr(4);
      myAcHold->allocState = myAcHold->allocState & ~4;
      (*myAcHold->free)(4,ptr,0x58);
    }
    if ((myAcHold->allocState & 2) != 0) {
      ptr = (void *)DWCi_AC_GetMemPtr(2);
      myAcHold->allocState = myAcHold->allocState & ~2;
      (*myAcHold->free)(2,ptr,0x2300);
    }
    if ((myAcHold->allocState & 1) != 0) {
      myAcHold->allocState = myAcHold->allocState & ~1;
      (*myAcHold->free)(1,myAcHold,0x24);
      acHold = (tagACHOLD *)0x0;
    }
  }
  return;
}
