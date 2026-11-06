#include "context.h"
s32 native_main_020446f8(Step *object,s32 publish) {
    Vec3 first;
    Vec3 second;
    Matrix33 matrix;
    const Vec3 *a;
    const Vec3 *b;
    s32 result=0;
    if(object && object->active0) {
        a=native_fn_020446cc(object->track30,object->index4,0);
        b=native_fn_020446cc(object->track30,object->index4,1);
        if(a && b) {
            second.x=b->x;second.y=b->y;second.z=b->z;
            first.x=a->x;first.y=a->y;first.z=a->z;
            if(object->angle2c) {
                native_fn_02000ce8(&matrix);
                native_fn_02028044(&matrix,object->angle2c);
                native_fn_0200103c(&second,&matrix,&second);
                native_fn_0200103c(&first,&matrix,&first);
            }
            object->end14.x=(u32)second.x+(u32)object->offset20.x;
            object->end14.y=(u32)second.y+(u32)object->offset20.y;
            object->end14.z=(u32)second.z+(u32)object->offset20.z;
            object->start8.x=(u32)first.x+(u32)object->offset20.x;
            object->start8.y=(u32)first.y+(u32)object->offset20.y;
            object->start8.z=(u32)first.z+(u32)object->offset20.z;
            if(publish) {
                native_fn_020283fc(0,object->end14.x,object->end14.y,object->end14.z);
                native_fn_020283dc(0,object->start8.x,object->start8.y,object->start8.z);
            }
        }
        object->index4=(u32)object->index4+1;
        if(object->index4>=object->track30->length4) {
            if(object->loop1)object->index4=0;
            else {object->active0=0;result=1;}
        }
    } else result=-1;
    return result;
}
