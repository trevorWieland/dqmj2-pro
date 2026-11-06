static void WmspStabilizeBeacon(void)
{
    *(vu16 *)((0x04808000) + 0x124) = 200;
    *(vu16 *)((0x04808000) + 0x128) = 2000;
    *(vu16 *)((0x04808000) + 0x150) = 0x0202;
}
