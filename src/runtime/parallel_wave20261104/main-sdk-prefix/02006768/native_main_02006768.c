#include "context_00.h"
void native_main_02006768 (void * arg)
    {
        OSThread * currentThread = (*native_data_main_020e33c0.field_0008) ;
        OSThreadDestructor destructor;
        ((void) 0) ;
        destructor = currentThread->destructor;
        if (destructor) {
            currentThread->destructor = ((void *)0) ;
            destructor(arg);
            (void)native_fn_02007ff4();
        }
        native_fn_020067a0();
    }
