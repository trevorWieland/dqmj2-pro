#include "context.h"
CounterPrefix *native_main_02071d78(void)
{
restart: ;
    DetailPrefix *detail=native_data_021c4f60.detail;
    ContextPrefix *context=native_fn_02061944();
    native_data_021c50e8.flags.raw=(s8)((native_data_021c50e8.flags.raw&~0xf0)|0x10);
    s32 i=0;
    do {
        native_data_021c50e8.busy[i]=0;
        i+=1;
    } while(i<7);
    u32 populated=native_fn_0206dc54(detail);
    if(native_fn_0206dca4()!=0){
        u32 slot=0;
        native_data_021c50e8.slot=0;
        do {
            if(populated!=0){
                switch(slot){
                case 0:native_fn_02061de4(&context->rows[3],detail->value18,0,0,0);break;
                case 1:native_fn_02061de4(&context->rows[4],detail->value40,1,0,0);break;
                case 2:native_fn_02061de4(&context->rows[5],detail->value42,2,0,0);break;
                case 3:native_fn_02061de4(&context->rows[6],detail->value44,3,0,0);break;
                case 4:native_fn_02061de4(&context->rows[7],detail->value48,4,0,0);break;
                case 5:native_fn_02061de4(&context->rows[8],detail->value46,5,0,0);break;
                case 6:native_fn_02061de4(&context->rows[9],detail->value4a,6,0,0);break;
                }
            }else{
                native_fn_02061de4(&context->rows[slot+3],0x9995,slot,0,0);
            }
            if(native_data_021c50e8.flags.bits.stage==0)break;
            native_data_021c50e8.flags.raw|=4;
            native_fn_0205fd18();
            if(native_data_021c50e8.flags.bits.restart!=0){
                native_data_021c50e8.flags.raw=(s8)(native_data_021c50e8.flags.raw&~8);
                goto restart;
            }
            if(native_fn_0206dca4()!=0){
                s8 current=native_data_021c50e8.slot;
                native_fn_0207211c((s8)(current+3),native_data_020de318[current].first,native_data_020de318[current].second);
                native_data_021c50e8.busy[native_data_021c50e8.slot]=1;
            }
            native_data_021c50e8.slot+=1;
            slot=(u32)native_data_021c50e8.slot;
        } while((s32)slot<7);
    }
    native_data_021c50e8.flags.raw=(s8)(native_data_021c50e8.flags.raw&~4);
    native_data_021c50e8.flags.raw|=2;
    return &native_data_021c50e8;
}
