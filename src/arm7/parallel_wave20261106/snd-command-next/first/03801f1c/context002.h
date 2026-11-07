static void SetChannelTimer (u32 chBitMask, int timer)
    {
        int ch;
        for (ch = 0; ch < 16 && chBitMask != 0; ch++, chBitMask >>= 1) {
            if ((chBitMask & 0x01) == 0)
                continue;
            native_host_arm7_arm_037feac0(ch, timer);
        }
    }

static void SetChannelVolume (u32 chBitMask, int volume, SNDChannelDataShift shift)
    {
        int ch;
        for (ch = 0; ch < 16 && chBitMask != 0; ch++, chBitMask >>= 1) {
            if ((chBitMask & 0x01) == 0)
                continue;
            native_host_arm7_arm_037fea48(ch, volume, shift);
        }
    }

static void SetChannelPan (u32 chBitMask, int pan)
    {
        int ch;
        for (ch = 0; ch < 16 && chBitMask != 0; ch++, chBitMask >>= 1) {
            if ((chBitMask & 0x01) == 0)
                continue;
            native_host_arm7_arm_037fead8(ch, pan);
        }
    }

static void StartTimer (u32 chBitMask, u32 capBitMask, u32 alarmBitMask, u32)
    {
        OSIntrMode enabled;
        int i;
        enabled = native_host_arm7_arm_037fdd00();
        for (i = 0; i < 16 && chBitMask != 0; i++, chBitMask >>= 1) {
            if ((chBitMask & 0x01) == 0)
                continue;
            SND_StartChannel(i);
        }
        if (capBitMask & (1 << SND_CAPTURE_0)) {
            if (capBitMask & (1 << SND_CAPTURE_1)) {
                SND_StartCaptureBoth();
            } else {
                SND_StartCapture(SND_CAPTURE_0);
            }
        } else if (capBitMask & (1 << SND_CAPTURE_1))   {
            SND_StartCapture(SND_CAPTURE_1);
        }
        for (i = 0; i < 8 && alarmBitMask != 0; i++, alarmBitMask >>= 1) {
            if ((alarmBitMask & 0x01) == 0)
                continue;
            native_host_arm7_arm_03801dac(i);
        }
        (void)native_host_arm7_arm_037fdd14(enabled);
        native_host_arm7_arm_03801c8c();
    }

static void StopTimer (u32 chBitMask, u32 capBitMask, u32 alarmBitMask, u32 flags)
    {
        OSIntrMode enabled;
        int i;
        enabled = native_host_arm7_arm_037fdd00();
        for (i = 0; i < 8 && alarmBitMask != 0; i++, alarmBitMask >>= 1) {
            if ((alarmBitMask & 0x01) == 0)
                continue;
            native_host_arm7_arm_03801e68(i);
        }
        for (i = 0; i < 16 && chBitMask != 0; i++, chBitMask >>= 1) {
            if ((chBitMask & 0x01) == 0)
                continue;
            native_host_arm7_arm_037fea20(i, (s32)flags);
        }
        if (capBitMask & (1 << SND_CAPTURE_0)) {
            SND_StopCapture(SND_CAPTURE_0);
        }
        if (capBitMask & (1 << SND_CAPTURE_1)) {
            SND_StopCapture(SND_CAPTURE_1);
        }
        (void)native_host_arm7_arm_037fdd14(enabled);
        native_host_arm7_arm_03801c8c();
    }

static void ReadDriverInfo (SNDDriverInfo * info)
    {
        int ch;
        MI_CpuCopy32(&native_host_arm7_data_03807ee0, &info->work, sizeof(native_host_arm7_data_03807ee0));
        info->workAddress = &native_host_arm7_data_03807ee0;
        for (ch = 0; ch < 16 ; ch++) {
            info->chCtrl[ch] = native_host_arm7_arm_037febd0(ch);
        }
        info->lockedChannels = native_host_arm7_arm_037ffcf8(0);
    }
