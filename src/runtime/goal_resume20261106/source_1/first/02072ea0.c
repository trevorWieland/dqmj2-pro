#include "toggle.h"
void native_main_02072ea0(u32 index)
{
    native_data_021c5a11[index].enabled=!native_data_021c5a11[index].enabled;
    native_data_021c5a11[index].dirty=1;
}
