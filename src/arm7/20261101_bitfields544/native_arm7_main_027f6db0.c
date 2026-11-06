#include "native_fields.h"
u32 native_arm7_main_027f6db0(u32 address) {
    PackedFields *p=(PackedFields *)address;
    switch(p->code) {
    case 0:
    case 1:
    case 2:
    case 3:
    case 4:
    case 5:
    case 6:
    case 7:
    case 16:
    case 17:
        if(p->flag) p->code+=18; break;
    case 8:
    case 9:
        if(p->flag) p->code+=24; break;
    case 18:
    case 19:
    case 20:
    case 21:
    case 22:
    case 23:
    case 24:
    case 25:
    case 32:
    case 33:
    case 34:
    case 35:
        p->flag=1; break;
    default:
        p->flag=0; p->code=0; break;
    }
    return address;
}
