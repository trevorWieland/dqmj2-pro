#include "dependency000.h"

int native_utility_child_arm9_main_0200f9b4 (int fifotag, u32 data, BOOL err)
{
    PXIFifoMessage fifomsg;
    ((void) 0) ;
    ((void) 0) ;
    fifomsg.e.tag = (PXIFifoTag)fifotag;
    fifomsg.e.err = (u32)err;
    fifomsg.e.data = data;
    return PXIi_SetToFifo(fifomsg.raw);
}
#include "dependency001.h"
