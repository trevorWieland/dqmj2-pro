void native_host_arm7_arm_027f1fb4(LPTXFRM pFrm, u16 *pDA);

u32 native_host_arm7_arm_027f2068(u8 *pBuf);

u32 native_host_arm7_arm_027f20dc(u8 *pBuf);

static u32 SetDSParamSet(u8 *pBuf)
{
    native_host_arm7_arm_027ead30(&pBuf[0], 3 );
    native_host_arm7_arm_027ead30(&pBuf[1], 1);
    native_host_arm7_arm_027ead30(&pBuf[2], ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work.CurrChannel);
    return 3;
}

static u32 SetGameInfoElement(u8 *pBuf)
{
    LPWORK_PARAM pWork = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work;
    LPCONFIG_PARAM pConfig = &((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Config;
    u32 i, j, vtsf;
    u8 *p;
    i = 0;
    native_host_arm7_arm_027ead30(&pBuf[i], 221 );
    i++;
    native_host_arm7_arm_027ead30(&pBuf[i], ((LPWL_MAN)(*(u32 *)((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x34))) ->Work.GameInfoLength + 3 + 1 + 4);
    i++;
    native_host_arm7_arm_027ead30(&pBuf[i], 0x00 );
    i++;
    native_host_arm7_arm_027ead30(&pBuf[i], 0x09 );
    i++;
    native_host_arm7_arm_027ead30(&pBuf[i], 0xBF );
    i++;
    native_host_arm7_arm_027ead30(&pBuf[i], 0x00 );
    i++;
    native_host_arm7_arm_027ead30(&pBuf[i], pConfig->ActiveZone);
    i++;
    native_host_arm7_arm_027ead30(&pBuf[i], pConfig->ActiveZone >> 8);
    i++;
    vtsf = *(vu16 *)(((0x03800000 + (0x03810000-0x03800000) - 0x40) + 0x30)) ;
    native_host_arm7_arm_027ead30(&pBuf[i], vtsf & 0x00FF);
    i++;
    native_host_arm7_arm_027ead30(&pBuf[i], vtsf >> 8);
    i++;
    if (pWork->GameInfoLength != 0) {
        p = (u8 *)pWork->GameInfoAdrs;
        if (pWork->GameInfoAlign & 1) {
            p++;
        }
        for (j = 0; j < pWork->GameInfoLength; j++) {
            native_host_arm7_arm_027ead30(&pBuf[i], native_host_arm7_arm_027ead5c(p));
            i++;
            p++;
        }
    }
    return i;
}
