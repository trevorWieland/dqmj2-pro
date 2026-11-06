typedef unsigned char u8;
typedef signed short s16;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
typedef struct ChoiceRecord { s16 id0; u8 variant2; u8 opaque3; u8 category4; u8 opaque5; } ChoiceRecord;
typedef struct StridedByte { u8 value0; u8 opaque1[5]; } StridedByte;
extern ChoiceRecord native_data_021d71fc[3];
extern ChoiceRecord native_data_021d720e[6];
extern StridedByte native_data_021d71fe[3];
extern StridedByte native_data_021d7210[6];
extern StridedByte native_data_021d7200[3];
extern StridedByte native_data_021d7212[6];
#define AT(T,F) ((u32)&((T *)0)->F)
typedef char WordLayout[(sizeof(s32)==4 && sizeof(void *)==4)?1:-1];
typedef char RecordLayout[(sizeof(ChoiceRecord)==6 && AT(ChoiceRecord,variant2)==2 && AT(ChoiceRecord,category4)==4)?1:-1];
typedef char ByteLayout[(sizeof(StridedByte)==6 && AT(StridedByte,value0)==0)?1:-1];
