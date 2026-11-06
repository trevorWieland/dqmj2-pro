#include "context_00.h"
void native_main_02009780 (struct SNDCommand * command)
{
    OSIntrMode bak_psr;
    ((void) 0) ;
    bak_psr = native_fn_02007ff4();
    if (native_data_main_020e3780.field_000c == ((void *)0) ) {
        native_data_main_020e3780.field_0008 = command;
        native_data_main_020e3780.field_000c = command;
    } else {
        native_data_main_020e3780.field_000c->next = command;
        native_data_main_020e3780.field_000c = command;
    }
    command->next = ((void *)0) ;
    (void)native_fn_02008008(bak_psr);
}
