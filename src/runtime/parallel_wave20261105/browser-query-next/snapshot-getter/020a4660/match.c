typedef unsigned char u8;typedef unsigned short u16;typedef unsigned int u32;typedef unsigned long long u64;
typedef struct{u64 first,second;u16 field10,opaque;}Snapshot;
void native_fn_02008e0c(const void*,void*,u32);
extern u8 native_data_021d2318[],native_data_021d231d[],native_data_021d2322[],native_data_021d2324[];
void native_main_020a4660(Snapshot*out){native_fn_02008e0c(native_data_021d2318,&out->first,6);out->first&=0x7ffffffffffULL;native_fn_02008e0c(native_data_021d231d,&out->second,6);out->second>>=3;out->second&=0x7ffffffffffULL;native_fn_02008e0c(native_data_021d2322,&out->field10,2);out->field10>>=6;out->field10&=0x3ff;native_fn_02008e0c(native_data_021d2324,&out->opaque,2);}
