#include "resource_selection.h"
u32 native_main_02061088(u32 selection,u32 group,u32 lane)
{
    u8 path[32];
    u32 bytes,resource;
    s8 code=((const SelectionPair *)native_data_020dac3c)[selection][lane];
    native_data_021b9bc8[3]=(u8)code;
    if(code==-1){
        native_fn_02008c14(0,((BufferPair *)native_data_021b9bd4)[group][lane],0x800);
        return 0;
    }
    code=(s8)native_data_021b9bc8[3];
    switch(code){
    case 5:
        if(native_fn_020625bc()!=0)native_fn_0201d444(path,native_data_020dde60);
        else native_fn_0201d444(path,native_data_020dde78,(s32)(s8)native_data_021b9bc8[3]);
        break;
    case 120:native_fn_0201d444(path,native_data_020ddde0);break;
    case 121:native_fn_0201d444(path,native_data_020dddf8);break;
    case 122:native_fn_0201d444(path,native_data_020dde10);break;
    case 123:native_fn_0201d444(path,native_data_020dde28);break;
    case 124:native_fn_0201d444(path,native_data_020dde3c);break;
    case 125:native_fn_0201d444(path,native_data_020dde50);break;
    default:native_fn_0201d444(path,native_data_020dde94,(s32)code);break;
    }
    bytes=native_fn_0202a8e0(path);
    if(bytes!=0){
        resource=native_fn_0203cc3c(path,2);
        native_fn_02008ca4(resource,((BufferPair *)native_data_021b9bd4)[group][lane],bytes);
        native_fn_0202a498(2,resource);
    }
    return ((BufferPair *)native_data_021b9bd4)[group][lane];
}
