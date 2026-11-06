static void SetChallengeText(u32 camAdrs, LPAUTH_FRAME pFrm)
{
    u32 i, txtLen;
    u16 *pText;
    u16 rnd;
    ;
    rnd = *(vu16 *)(0x04808000 + 0x044) + (*(vu16 *)(0x04808000 + 0x044) << 8);
    if (rnd == 0) {
        rnd = 1;
    }
    native_host_arm7_arm_027eadac(rnd);
    native_host_arm7_arm_027ebe78(camAdrs, rnd);
    pText = (u16 *)pFrm->Body.ChallengeText.Text;
    txtLen = native_host_arm7_arm_027ead5c(&pFrm->Body.ChallengeText.Length);
    for (i = 0; i < txtLen; i += 2) {
        *pText++ = native_host_arm7_arm_027eadc4();
    }
}

static u32 CheckChallengeText(LPAUTH_FRAME pFrm)
{
    u32 i, txtLen;
    u16 *pText;
    native_host_arm7_arm_027eadac(native_host_arm7_arm_027ec06c(pFrm->FirmHeader.CamAdrs));
    pText = (u16 *)pFrm->Body.ChallengeText.Text;
    txtLen = native_host_arm7_arm_027ead5c(&pFrm->Body.ChallengeText.Length);
    for (i = 0; i < txtLen / 2; i++) {
        if (*pText++ != native_host_arm7_arm_027eadc4()) {
            return 0 ;
        }
    }
    if (txtLen & 1) {
        if ((*pText & 0x00FF) != (native_host_arm7_arm_027eadc4() & 0x00FF)) {
            return 0 ;
        }
    }
    return 1 ;
}
