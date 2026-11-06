void native_host_arm7_main_027ebdb4(u32 camAdrs);

void CAM_SetAwake(u32 camAdrs)
{
    ;
    ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->CamMan.PowerState |= (1 << camAdrs);
}

void native_host_arm7_arm_027ebf6c(u16 camAdrs);

u32 CAM_GetPowerMgtMode(u32 camAdrs)
{
    return (((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->CamMan.PowerMgtMode >> camAdrs) & 1;
}

u32 native_host_arm7_arm_027ec0d8(u32 camAdrs);

WlStaElement *CAM_GetTbl(u32 camAdrs)
{
    return &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config.pCAM[camAdrs];
}
