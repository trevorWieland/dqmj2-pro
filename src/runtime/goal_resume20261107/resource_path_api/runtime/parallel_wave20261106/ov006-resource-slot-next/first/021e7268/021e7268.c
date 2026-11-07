#include "../../../../../resource_path_api.h"
#include "context.h"
u32 native_ov006_021e7268(void) {
    ActiveBlock *active=native_data_ov006_02218d90.active34;
    if(!active)return (u32)active;
    native_fn_020485b4(active);
    native_fn_020484dc(1,native_data_ov006_0220d114);
    native_data_ov006_02218d90.active34=0;
    native_data_ov006_0220d114=127;
    return (u32)&native_data_ov006_0220d114;
}
