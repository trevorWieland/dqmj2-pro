#include "context.h"
u32 native_ov000_021ec044(u32 field0,u32 field1)
{
    Point16 point={0,0};
    native_fn_0204a010(native_fn_02049ad0(7)->link->resource,88,0,80,16);
    point.x=72;
    native_fn_0204a104(7,&point,1,native_data_ov000_0222ee48);
    point.x+=8;
    native_fn_0204a154(7,&point,1,field0,7,0);
    native_fn_0204a010(native_fn_02049ad0(8)->link->resource,88,0,80,16);
    point.x=72;
    native_fn_0204a104(8,&point,1,native_data_ov000_0222ee4c);
    point.x+=8;
    return native_fn_0204a154(8,&point,1,field1,7,0);
}
