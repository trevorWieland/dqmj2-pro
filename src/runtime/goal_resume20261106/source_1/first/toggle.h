typedef unsigned char u8;
typedef unsigned int u32;
typedef struct {u8 prefix[6];u8 enabled,dirty,padding;} ToggleRow;
typedef char ByteWidth[(sizeof(u8)==1)?1:-1];
typedef char WordWidth[(sizeof(u32)==4)?1:-1];
typedef char RowStride[(sizeof(ToggleRow)==9)?1:-1];
extern ToggleRow native_data_021c5a11[2];
extern void native_main_02072ea0(u32);
