typedef unsigned char u8;
typedef unsigned short int u16;
u16 native_main_02009e60(int dB);
typedef enum {
	SND_CHANNEL_DATASHIFT_NONE,
	SND_CHANNEL_DATASHIFT_1BIT,
	SND_CHANNEL_DATASHIFT_2BIT,
	SND_CHANNEL_DATASHIFT_4BIT
} SNDChannelDataShift;
extern const u8 native_data_main_020d8954[(0 - (-723) + 1) ];
u16 native_main_02009e60 (int dB)
{
    SNDChannelDataShift shift;
    u8 volume;
    if (dB < (-723) ) {
        dB = (-723) ;
    } else if (dB > 0 )   {
        dB = 0 ;
    }
    volume = native_data_main_020d8954[dB - (-723) ];
    if (dB < -240 ) {
        shift = SND_CHANNEL_DATASHIFT_4BIT;
    } else if (dB < -120 )   {
        shift = SND_CHANNEL_DATASHIFT_2BIT;
    } else if (dB < -60 )   {
        shift = SND_CHANNEL_DATASHIFT_1BIT;
    } else {
        shift = SND_CHANNEL_DATASHIFT_NONE;
    }
    return (u16)(shift << 8 | volume);
}
