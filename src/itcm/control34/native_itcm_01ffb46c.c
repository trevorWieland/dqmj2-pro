typedef unsigned int u32;
typedef signed short s16;
typedef struct { s16 x; s16 y; } Point;
extern u32 native_fn_01ffb340(void);
extern u32 native_fn_01ffb34c(void);
extern void native_fn_02049008(u32, u32, u32, u32, u32);
extern void native_fn_ov000_02223980(u32, u32, Point *);
void native_itcm_01ffb46c(void) {
    Point point;
    u32 object;
    native_fn_02049008(native_fn_01ffb340(), 5, 0, 1, 4);
    point.x = 0x10;
    point.y = 0x28;
    object = native_fn_01ffb340();
    native_fn_ov000_02223980(object, native_fn_01ffb34c(), &point);
}
