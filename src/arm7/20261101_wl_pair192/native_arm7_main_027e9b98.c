#include "wl_measured_views.h"
u32 native_arm7_main_027e9b98(u32 address)
{
    NativeRateSet *pRateSet = (NativeRateSet *)address;
    NativeRateSet *pWrs = &wlMan->Work.RateSet;
    pWrs->Basic = pRateSet->Basic;
    pWrs->Support = (u16)(pRateSet->Support | pRateSet->Basic);
    native_host_arm7_arm_027e9bd8();
    return 0;
}
