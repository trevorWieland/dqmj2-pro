#include "widget_registry_types_20261030.h"
void native_main_0204861c(u32 kind, u32 index) {
    u32 address = (u32)&native_data_020fbae8[kind];
    (*(u32 *)(address + index * 4 + 0x3544)) = 0;
}
