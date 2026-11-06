typedef unsigned char u8;
typedef unsigned short u16;
typedef struct {
    u8 prefix[12];
    u16 *stream;
} PublicationRoot;
__declspec(align(4)) extern PublicationRoot native_data_02102974;
u16 *native_main_02049f14(u16 *stream) {
    native_data_02102974.stream = stream;
    return stream;
}
