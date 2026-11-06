static inline PXIFifoStatus PXIi_SetToFifo (u32 data)
{
    OSIntrMode enabled;
    if ((*( REGType16v *) (0x04000000 + 0x184)) & 0x4000 ) {
        (*( REGType16v *) (0x04000000 + 0x184)) |= (0x8000 | 0x4000 );
        return PXI_FIFO_FAIL_SEND_ERR;
    }
    enabled = native_utility_child_arm9_arm_0200a64c();
    if ((*( REGType16v *) (0x04000000 + 0x184)) & 0x0002 ) {
        (void)native_utility_child_arm9_arm_0200a660(enabled);
        return PXI_FIFO_FAIL_SEND_FULL;
    }
    (*( REGType32v *) (0x04000000 + 0x188)) = data;
    (void)native_utility_child_arm9_arm_0200a660(enabled);
    return PXI_FIFO_SUCCESS;
}
