#include "context_00.h"
void native_main_02007a34 (void)
{
    native_data_main_020e36f4.field_0008++;
    if (native_data_main_020e36f4.field_0004) {
        OS_SetTimerControl(OS_TIMER_0 , 0);
        OS_SetTimerCount((OSTimer)OS_TIMER_0 , (u16)0);
        OS_SetTimerControl(OS_TIMER_0 , (u16)(0x0080 | 0x0040 | OS_TIMER_PRESCALER_64) );
        native_data_main_020e36f4.field_0004 = 0 ;
    }
    native_data_main_02005cac(OS_TIMER_0 , (void (*)(void *)) native_main_02007a34, 0);
}
