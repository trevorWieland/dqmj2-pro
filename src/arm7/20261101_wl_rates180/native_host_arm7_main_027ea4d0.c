typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned long u32;
typedef struct {u8 ID;u8 Length;u8 SupportedRate[2];} SUP_RATE_ELEMENT,*LPSUP_RATE_ELEMENT;
typedef struct {u16 Basic;u16 Support;} RATE_SET,*LPRATE_SET;
extern u8 WL_ReadByte(void *pointer);
extern const u16 native_host_arm7_data_027f73c0[120];
void WElement2RateSet(LPSUP_RATE_ELEMENT pSup, LPRATE_SET pRateSet)
{
    u32 i, length, brate, srate;
    pRateSet->Basic = 0;
    pRateSet->Support = 0;
    length = WL_ReadByte(&pSup->Length);
    for (i = 0; i < length; i++) {
        brate = WL_ReadByte(&pSup->SupportedRate[i]);
        srate = (brate & 0x7F) - 1;
        if ((srate < sizeof(native_host_arm7_data_027f73c0) / 2 ) && (native_host_arm7_data_027f73c0[srate] != 0xFF)) {
            pRateSet->Support |= (0x01 << native_host_arm7_data_027f73c0[srate]);
            if (brate & 0x80) {
                pRateSet->Basic |= (0x01 << native_host_arm7_data_027f73c0[srate]);
            }
        } else {
            pRateSet->Support |= 0x8000;
            if (brate & 0x80) {
                pRateSet->Basic |= 0x8000;
            }
        }
    }
}
