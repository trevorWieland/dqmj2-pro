#include "context_00.h"
SNDCommand * native_main_02009b9c (void)
    {
        OSIntrMode bak_psr = native_fn_02007ff4();
        SNDCommand * command;
        if (native_data_main_020e3780.field_0000 == ((void *)0) ) {
            (void)native_fn_02008008(bak_psr);
            return ((void *)0) ;
        }
        command = native_data_main_020e3780.field_0000;
        native_data_main_020e3780.field_0000 = native_data_main_020e3780.field_0000->next;
        if (native_data_main_020e3780.field_0000 == ((void *)0) )
            native_data_main_020e3780.field_0010 = ((void *)0) ;
        (void)native_fn_02008008(bak_psr);
        return command;
    }
