typedef unsigned char u8;
typedef unsigned short u16;
extern int native_fn_020643b0(void);
extern int native_fn_02026144(int, int);
extern void native_fn_020877bc(int, u16 *, int, int);
extern void native_fn_ov005_021dded4(int, const u16 *, int);
void native_ov005_021db6f8(int input)
{
    u16 buffer[8] = {0};
    u8 cursor = 0;
    u16 value = native_fn_02026144(input * 1000, native_fn_020643b0());
    if (value >= 1000) {
        native_fn_020877bc(100, buffer, 4, 3);
        native_fn_ov005_021dded4(11, buffer, 8);
        return;
    }
    native_fn_020877bc(value / 10, buffer, sizeof(buffer), 2);
    cursor += 2;
    buffer[cursor] = '.';
    cursor++;
    native_fn_020877bc(value % 10, buffer + cursor, sizeof(buffer) - cursor * 2, 1);
    native_fn_ov005_021dded4(11, buffer, 4);
}
