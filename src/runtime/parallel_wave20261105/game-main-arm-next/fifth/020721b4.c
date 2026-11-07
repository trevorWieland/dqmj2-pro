#include "context.h"
u32 native_main_020721b4(s32 index)
{
    Widget *widget=*native_fn_02061dcc(index);
    void *renderer=widget->field4;
    DetailPrefix *detail=native_data_021c4f60.detail;
    Point point;
    u32 available,state;
    point.x=0;
    point.y=0;
    native_fn_02049ffc(renderer);
    available=native_fn_0206dc54(detail);
    state=native_fn_0206dca4();
    if(state==0)return state;
    switch(index){
    default:return state;
    case 6:return native_fn_020602ec(widget,detail->value18,detail,0,0,1);
    case 8:
        if(available!=0 && detail->value40!=0)return native_fn_020602ec(widget,detail->value40,detail->text52,point.x,0,1);
        return native_fn_02087a48(renderer,0,point.x,point.y,1,native_data_020de3c4);
    case 10:
        if(available!=0 && detail->value42!=0)return native_fn_020602ec(widget,detail->value42,detail->text66,point.x,0,1);
        return native_fn_02087a48(renderer,0,point.x,point.y,1,native_data_020de3d8);
    case 7:
    case 9:{
        u16 selector;
        if(index==7)selector=13;
        else selector=14;
        state=native_fn_0204aaf0(index,&point,5,2,selector,1,1);
    }
    case 0:
    case 1:
    case 2:
    case 3:
    case 4:
    case 5:return state;
    }
}
