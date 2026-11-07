typedef unsigned short int u16;

typedef unsigned long u32;

typedef volatile u16 vu16;

typedef vu16 REGType16v;

typedef enum {
    SPI_BAUDRATE_4MHZ = 0,
    SPI_BAUDRATE_2MHZ = 1,
    SPI_BAUDRATE_1MHZ = 2,
    SPI_BAUDRATE_512KHZ = 3
} SPIBaudRate;

typedef enum {
    SPI_TRANSMODE_1BYTE = 0,
    SPI_TRANSMODE_CONTINUOUS = 1
} SPITransMode;

typedef enum {
    SPI_COMMPARTNER_PMIC = 0,
    SPI_COMMPARTNER_EEPROM = 1,
    SPI_COMMPARTNER_TP = 2
} SPICommPartner;

static inline void SPI_Wait(void)
{
    while ((*( REGType16v *) (0x04000000 + 0x1c0)) & 0x0080 ) {
    }
}

static inline void SPI_Send(u16 data)
{
    (*( REGType16v *) (0x04000000 + 0x1c2)) = data & 0xFF;
}

inline void native_host_arm7_arm_03804498(void);

static inline void SPI_SendWait(u16 data)
{
    SPI_Send(data);
    SPI_Wait();
}

static inline void TP_SPIChangeMode(SPITransMode continuous)
{
    (*( REGType16v *) (0x04000000 + 0x1c0)) = (u16)((1 << 15 )
        | (0 << 14 )
        | (SPI_COMMPARTNER_TP << 8 )
        | (continuous << 11 )
        | (0 << 7 )
        | (SPI_BAUDRATE_2MHZ << 0 ));
}

extern const u16 (*ctrdgi_fl_maxtime);

typedef enum {
	EXI_GPIOIF_SERIAL = 0x0000,
	EXI_GPIOIF_UNDEF  = 0x4000 ,
	EXI_GPIOIF_GPIO   = 0x8000 ,
	EXI_GPIOIF_JOY    = 0x8000 | 0x4000
} EXIGpioIF;

void native_host_arm7_arm_037fe5a8(EXIGpioIF type);

enum {
    TOUCH_OFF = 0,
    TOUCH_ON = 1,
    TOUCH_MAY_OFFNOISE = 2
};

extern u16 native_host_arm7_data_03809ea8;

u32 native_host_arm7_wram_038043a4(void);
