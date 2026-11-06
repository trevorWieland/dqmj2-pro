static inline WMSPWork *WMSP_GetSystemWork(void)
{
    return &native_host_arm7_data_027f7884;
}

static inline WMStatus *WMSP_GetStatusStructure(void)
{
    return native_host_arm7_data_027f7884.status;
}

extern OSVAlarm native_host_arm7_data_0380b4bc;

void native_host_arm7_main_027e5c5c(void *arg);

 void native_host_arm7_main_027e5dc0(void *arg);

 void native_host_arm7_main_027e5e80(void *arg);

static void WmspSetVAlarm(s16 count, OSVAlarmHandler handler, void *arg);

static void WmspCalcVRemain(void);

static void WmspSetVAlarm(s16 count, OSVAlarmHandler handler, void *arg)
{
    native_host_arm7_arm_037fd898(&native_host_arm7_data_0380b4bc, count, (192 + 71) , handler, arg);
}

static void WmspCalcVRemain(void)
{
    u16 low0, low1, high;
    u32 cur_tsf;
    u16 vcount;
    u32 next_0line_tsf;
    int i;
    WMSPWork *p = WMSP_GetSystemWork();
    WMStatus *status = WMSP_GetStatusStructure();
    status->v_tsf <<= 6;
    low0 = *(vu16 *)((0x04808000) + 0x0F8) ;
    high = *(vu16 *)((0x04808000) + 0x0FA) ;
    low1 = *(vu16 *)((0x04808000) + 0x0F8) ;
    if (low0 > low1) {
        high = *(vu16 *)((0x04808000) + 0x0FA) ;
    }
    cur_tsf = high;
    cur_tsf <<= 16;
    cur_tsf |= low1;
    cur_tsf &= 0x003fffc0;
    vcount = (u16)GX_GetVCount();
    next_0line_tsf = cur_tsf;
    next_0line_tsf <<= 1;
    next_0line_tsf += ((263 - vcount) * 127);
    next_0line_tsf >>= 1;
    next_0line_tsf &= 0x003fffc0;
    if (status->v_tsf > next_0line_tsf) {
        status->v_remain = 0;
        return;
    }
    for (i = 1; i < 30; ++i) {
        status->v_tsf += ((u32)(1000000ULL * (192 + 71) * (256 + 99) * 6 / 33513982)) ;
        if (status->v_tsf > next_0line_tsf) {
            status->v_remain = status->v_tsf - next_0line_tsf;
            if (status->v_remain > (((u32)(1000000ULL * (192 + 71) * (256 + 99) * 6 / 33513982)) - ((u32)(1000000ULL * (5) * (256 + 99) * 6 / 33513982)) )) {
                status->v_remain = 0;
            }
            return;
        }
    }
    status->v_remain = 0;
}
