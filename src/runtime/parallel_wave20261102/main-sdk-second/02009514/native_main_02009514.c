#include "context_00.h"
void native_main_02009514 (void)
{
    SNDCommand * command;
    int i;
    native_fn_02009b14();
    native_data_main_020e3780.field_0000 = &native_data_main_020e3780.field_02e0[0];
    for (i = 0; i < 256 - 1; i++) {
        native_data_main_020e3780.field_02e0[i].next = &native_data_main_020e3780.field_02e0[i + 1];
    }
    native_data_main_020e3780.field_02e0[256 - 1].next = ((void *)0) ;
    native_data_main_020e3780.field_0010 = &native_data_main_020e3780.field_02e0[256 - 1];
    native_data_main_020e3780.field_0008 = ((void *)0) ;
    native_data_main_020e3780.field_000c = ((void *)0) ;
    native_data_main_020e3780.field_001c = 0;
    native_data_main_020e3780.field_0014 = 0;
    native_data_main_020e3780.field_0018 = 0;
    native_data_main_020e3780.field_0020 = 1;
    native_data_main_020e3780.field_0004 = 0;
    native_data_main_020e52c0 = &native_data_main_020e3780.field_0060;
    native_fn_02009de4(native_data_main_020e52c0);
    command = native_fn_020096f8((1 << 0) );
    if (command != ((void *)0) ) {
        command->id = SND_COMMAND_SHARED_WORK;
        command->arg[0] = (u32)native_data_main_020e52c0;
        native_fn_02009780(command);
        (void)native_fn_020097b8((1 << 0) );
    }
}
