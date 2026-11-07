typedef unsigned short int u16;

typedef signed long s32;

typedef volatile u16 vu16;

typedef vu16 REGType16v;

typedef enum SPITpValidity {
	SPI_TP_VALIDITY_VALID = 0,
	SPI_TP_VALIDITY_INVALID_X,
	SPI_TP_VALIDITY_INVALID_Y,
	SPI_TP_VALIDITY_INVALID_XY
} SPITpValidity;

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

static inline void SPI_Dummy(void)
{
    (*( REGType16v *) (0x04000000 + 0x1c2)) = 0 ;
}

static inline void SPI_Send(u16 data)
{
    (*( REGType16v *) (0x04000000 + 0x1c2)) = data & 0xFF;
}

static inline u16 SPI_Receive(void)
{
    return (*( REGType16v *) (0x04000000 + 0x1c2)) & 0xFF;
}

inline void native_host_arm7_arm_03804498(void);

static inline void SPI_SendWait(u16 data)
{
    SPI_Send(data);
    SPI_Wait();
}

static inline u16 SPI_DummyWaitReceive(void)
{
    SPI_Dummy();
    SPI_Wait();
    return SPI_Receive();
}

static inline u16 SPI_SendWaitReceive(u16 data)
{
    SPI_Send(data);
    SPI_Wait();
    return SPI_Receive();
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
    TP_DETECT_AXIS_X,
    TP_DETECT_AXIS_Y
} TPDetectAxis;

SPITpValidity native_host_arm7_wram_038044bc(u16 *data, s32 range, TPDetectAxis axis, u16 *density);
