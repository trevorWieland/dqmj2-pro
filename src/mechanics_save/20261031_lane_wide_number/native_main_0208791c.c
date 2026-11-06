typedef unsigned short u16;
typedef unsigned int u32;
typedef signed int s32;

extern void native_fn_02008be0(u32, void *, s32);
extern int native_fn_020211c0(u16 *, u32, const u16 *, ...);
extern const u16 native_data_020de714[];
extern const u16 native_data_020de720[];
extern const u16 native_data_020de72c[];
extern const u16 native_data_020de738[];
extern const u16 native_data_020de744[];
extern const u16 native_data_020de750[];
extern const u16 native_data_020de75c[];
extern const u16 native_data_020de768[];

u32 native_main_0208791c(s32 arg0, u16 *arg1, u32 arg2, u32 arg3) {
    native_fn_02008be0(0, arg1, (s32)arg2);
    switch (arg3) {
    case 1:
        native_fn_020211c0(arg1, arg2, native_data_020de714, arg0);
        break;
    case 2:
        native_fn_020211c0(arg1, arg2, native_data_020de720, arg0);
        break;
    case 3:
        native_fn_020211c0(arg1, arg2, native_data_020de72c, arg0);
        break;
    case 4:
        native_fn_020211c0(arg1, arg2, native_data_020de738, arg0);
        break;
    case 5:
        native_fn_020211c0(arg1, arg2, native_data_020de744, arg0);
        break;
    case 6:
        native_fn_020211c0(arg1, arg2, native_data_020de750, arg0);
        break;
    case 7:
        native_fn_020211c0(arg1, arg2, native_data_020de75c, arg0);
        break;
    default:
    case 0:
        native_fn_020211c0(arg1, arg2, native_data_020de768, arg0);
        break;
    }
    return (u32)arg1;
}
