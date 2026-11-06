typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned long long u64;
typedef struct AddressState { u8 opaque0[104]; u64 seed68; u64 multiplier70; u64 increment78; } AddressState;
extern AddressState native_data_021cfcf8;
extern u32 native_data_021cfcf0[2];
extern u64 native_fn_02026124(u64,u64);
extern s32 native_fn_0208e820(const char *,u32 *);
extern u32 native_fn_0208e878(const char *,u32,u16);
static inline u64 next_value(void){u64 value=native_fn_02026124(native_data_021cfcf8.multiplier70,native_data_021cfcf8.seed68)+native_data_021cfcf8.increment78;native_data_021cfcf8.seed68=value;return value;}
#define AT(T,F) ((u32)&((T *)0)->F)
typedef char WordLayout[(sizeof(u32)==4 && sizeof(void *)==4 && sizeof(u64)==8)?1:-1];
typedef char ContextLayout[(sizeof(AddressState)==128 && sizeof(((AddressState *)0)->seed68)==8 && sizeof(((AddressState *)0)->multiplier70)==8 && sizeof(((AddressState *)0)->increment78)==8 && AT(AddressState,seed68)==104 && AT(AddressState,multiplier70)==112 && AT(AddressState,increment78)==120)?1:-1];
static inline u32 bounded_value(u32 maximum){u64 value=next_value();if(maximum==0)return (u32)(value>>32);else return (u32)(((value>>32)*maximum)>>32);}
extern u32 native_fn_0208e7f8(const u8 *,const u8 **);
extern void native_fn_0208d7c0(void);
extern void native_fn_0208d764(void);
extern void native_fn_0208d780(u32,u32,u32);
extern void native_fn_0208d7e0(void);
extern u32 native_fn_0208e644(const char *,u32,u16,u8 *,u32);
