typedef unsigned char u8;
typedef unsigned short u16;
typedef struct {
    u8 prefix[0x4c];
    volatile u16 field4c;
    volatile u16 field4e;
    volatile u16 field50;
} Counters;
extern Counters native_counters;
u16 saved_20261029_counter4c_get(void) {
    return native_counters.field4c;
}
void saved_20261029_counter4c_increment(void) {
    native_counters.field4c++;
    if (native_counters.field4c > 9999U) native_counters.field4c = 9999;
}
u16 saved_20261029_counter4e_get(void) {
    return native_counters.field4e;
}
void saved_20261029_counter4e_increment(void) {
    native_counters.field4e++;
    if (native_counters.field4e > 9999U) native_counters.field4e = 9999;
}
u16 saved_20261029_counter50_get(void) {
    return native_counters.field50;
}
void saved_20261029_counter50_increment(void) {
    native_counters.field50++;
    if (native_counters.field50 > 9999U) native_counters.field50 = 9999;
}
