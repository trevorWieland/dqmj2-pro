void TxManCtrlFrame(LPTXFRM pFrm)
{
    native_host_arm7_arm_027f10a0(pFrm);
    native_host_arm7_arm_027eff00(1 );
}

void native_host_arm7_arm_027f10a0(LPTXFRM pFrm);

LPDEAUTH_FRAME native_host_arm7_arm_027f1ec8(u16 *pDA, u16 reasonCode, u32 bCheck);
