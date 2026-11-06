#include "context_00.h"
WMOtherElements native_main_02012464 (WMBssDesc * bssDesc)
{
    WMOtherElements elems;
    u8 * p_elem;
    int i;
    u8 curr_elem_len;
    u8 elems_len;
    u8 elems_len_counter;
    if (bssDesc->gameInfoLength != 0) {
        elems.count = 0;
        return elems;
    }
    elems.count = (u8)(bssDesc->otherElementCount);
    if (elems.count == 0)
        return elems;
    if (elems.count > 16 )
        elems.count = 16 ;
    p_elem = (u8 *)&(bssDesc->gameInfo);
    elems_len = (u8)((bssDesc->length * sizeof(u16)) - 64);
    elems_len_counter = 0;
    for (i = 0; i < elems.count; ++i) {
        elems.element[i].id = p_elem[0];
        elems.element[i].length = p_elem[1];
        elems.element[i].body = (u8 *)&(p_elem[2]);
        curr_elem_len = (u8)(elems.element[i].length + 2);
        elems_len_counter += curr_elem_len;
        if (elems_len_counter > elems_len) {
            ((void) 0) ;
            elems.count = 0;
            return elems;
        }
        p_elem = (u8 *)(p_elem + curr_elem_len);
    }
    return elems;
}
