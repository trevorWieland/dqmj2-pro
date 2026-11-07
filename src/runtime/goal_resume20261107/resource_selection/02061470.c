#include "resource_selection.h"
u32 native_main_02061470(void)
{
    u16 zero=0;
    u8 path[32];
    u32 bytes,resource;
    native_fn_0201d444(path,native_data_020ddeb0);
    bytes=native_fn_0202a8e0((u32)path);
    if(bytes!=0){
        resource=native_fn_0203cc3c((u32)path,2);
        native_fn_020481b8(resource,0,bytes);
        native_fn_020481b8((u32)&zero,0,2);
        native_fn_02048308();
        native_fn_0202a498(2,resource);
    }
    native_fn_0201d444(path,native_data_020ddec4);
    if(native_fn_0202a8e0((u32)path)!=0){
        resource=native_fn_0203cc3c((u32)path,2);
        if((s8)native_data_021b9bd4[0x273]!=0)native_fn_0204540c(native_data_021b9bd0[1],(const void *)resource,0,0x900);
        native_fn_0204540c(native_data_021b9bd0[2],(const void *)resource,0,0x900);
        native_fn_0202a498(2,resource);
    }
    native_data_021b9bc8[1]=1;
    return (u32)native_data_021b9bc8;
}
