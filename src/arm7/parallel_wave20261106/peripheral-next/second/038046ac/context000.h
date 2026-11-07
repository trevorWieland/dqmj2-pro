typedef unsigned char u8;

typedef unsigned short int u16;

typedef unsigned long u32;

typedef signed long s32;

typedef volatile u16 vu16;

typedef vu16 REGType16v;

void native_host_arm7_arm_037fde70();

extern void native_host_arm7_arm_037fde70(void);

typedef enum SPITpTouch {
	SPI_TP_TOUCH_OFF = 0,
	SPI_TP_TOUCH_ON
} SPITpTouch;

typedef enum SPITpValidity {
	SPI_TP_VALIDITY_VALID = 0,
	SPI_TP_VALIDITY_INVALID_X,
	SPI_TP_VALIDITY_INVALID_Y,
	SPI_TP_VALIDITY_INVALID_XY
} SPITpValidity;

typedef union SPITpData {
	struct {
		u32 x : 12;
		u32 y : 12;
		u32 touch : 1;
		u32 validity : 2;
		u32 dummy : 5;
	} e;
	u32 raw;
	u8 bytes[4];
	u16 halfs[2];
} SPITpData;

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

inline void native_host_arm7_arm_03804498(void);

static inline void TP_SPIChangeMode(SPITransMode continuous)
{
    (*( REGType16v *) (0x04000000 + 0x1c0)) = (u16)((1 << 15 )
        | (0 << 14 )
        | (SPI_COMMPARTNER_TP << 8 )
        | (continuous << 11 )
        | (0 << 7 )
        | (SPI_BAUDRATE_2MHZ << 0 ));
}

void native_host_arm7_wram_038046ac(SPITpData *data, s32 range, u16 *density);

extern const u16 (*ctrdgi_fl_maxtime);

typedef enum {
    TP_DETECT_AXIS_X,
    TP_DETECT_AXIS_Y
} TPDetectAxis;

enum {
    TOUCH_OFF = 0,
    TOUCH_ON = 1,
    TOUCH_MAY_OFFNOISE = 2
};

extern u16 native_host_arm7_data_03809ea8;

u32 native_host_arm7_wram_038043a4(void);

SPITpValidity native_host_arm7_arm_038044bc(u16 *data, s32 range, TPDetectAxis axis, u16 *density);
