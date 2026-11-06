WlStaElement *CAM_GetTbl(u32 camAdrs)
{
    return &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config.pCAM[camAdrs];
}
