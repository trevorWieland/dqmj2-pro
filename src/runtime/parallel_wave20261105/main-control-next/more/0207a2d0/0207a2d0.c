#include "context000.h"

Context *native_main_0207a2d0(int id,int slot){
    Context *context=native_fn_0206ea80();
    Selection before=native_data_021c6728;
    native_data_021c6728.id=id;
    native_data_021c6728.slot=slot;
    if(before.id!=native_data_021c6728.id || native_data_021c6728.slot!=before.slot)context->dirty=1;
    return context;
}
