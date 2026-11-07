typedef unsigned char u8;
typedef signed short s16;
typedef unsigned int u32;
typedef signed int s32;
extern u8 *native_fn_0203cc2c(const u8*,s32);
extern u32 native_fn_0203cf9c(s32,u8*);
extern u8 native_data_ov006_0220d010[];

typedef char Word32[(sizeof(u32)==4&&sizeof(s32)==4&&sizeof(void*)==4)?1:-1];
typedef char Halfword16[(sizeof(s16)==2)?1:-1];
typedef char UnsignedByte[(((u8)-1)>0&&sizeof(u8)==1)?1:-1];
typedef char SignedHalfword[((s16)-1<0)?1:-1];
s32 native_ov006_021dd434(s32,s32,s32);
