#include "widget_registry_types_20261030.h"
u32 native_main_020485c8(u32 kind, RegistryWidget *widget) {
    u8 index = 0;
    u32 address = (u32)&native_data_020fbae8[kind];
    do {
        if (((RegistryManager *)address)->objects[index] == 0) {
            ((RegistryManager *)address)->objects[index] = (u32)widget;
            widget->index = index;
            return 1;
        }
        index++;
    } while (index < 128);
    return 0;
}
