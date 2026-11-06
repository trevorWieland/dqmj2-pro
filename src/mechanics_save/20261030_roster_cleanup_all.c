typedef signed char s8;
typedef signed int s32;
extern void native_fn_0206ce54(s32 sprite);
extern s8 native_data_021c4af4[];
void native_main_0206d7f8(void) {
    s8 sprite = 0;
    if (*native_data_021c4af4 > 0) {
        do {
            native_fn_0206ce54(sprite);
            sprite++;
        } while (*native_data_021c4af4 > sprite);
    }
}
