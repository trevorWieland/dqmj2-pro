typedef unsigned char u8;
typedef unsigned int u32;
typedef struct { u8 status; signed char heap; unsigned short reserved; int (*validator)(void *); u8 *buffer; } SaveIo;
extern SaveIo native_save_io;
extern u8 native_main[];
extern void *native_allocate(int, u32, int);
extern void native_free(int, void *);
extern void native_copy(const void *, void *, u32);
extern void native_fill(void *, int, u32);
extern int native_save_read(u32, void *, u32);
extern int native_save_write(u32, void *, u32);
extern int save_bank_validate(void *);
extern u8 *save_main_pointer(void);
extern int save_load_primary(int);
extern int save_load_primary_async(int);
extern int save_load_async_poll(void);
extern u32 save_write_status(void);
extern int save_header_invalidate(u32);
extern void native_save_error_present(u32);
int save_reload_main(u32 index, int heap) {
    int success = 0;
    u8 *bank = native_allocate(heap, 0x70d0, 4);
    if (bank) {
        if (native_save_read(index, bank, 0)) {
            if (save_bank_validate(bank)) {
                u8 *main_state = save_main_pointer();
                native_copy(bank + 0x90, main_state, 0x39d8);
                native_save_io.status = 0;
                success = 1;
            }
        } else native_save_io.status = 2;
        native_free(heap, bank);
    }
    return success;
}
int save_header_invalidate_again(u32 index) {
    u8 header[0x90];
    native_fill(header, 0, 0x90);
    if (native_save_write(index, header, 0x90)) {
        native_save_io.status = 0;
        return 1;
    }
    native_save_io.status = 1;
    return 0;
}
u8 *save_main_metadata_pointer(void) { return native_main + 8; }
void save_reload_preserving_metadata(void) {
    u8 data[0x14];
    u8 *metadata = save_main_metadata_pointer();
    native_copy(metadata, data, 0x14);
    if (!save_reload_main(0, 2)) {
        if (save_write_status() == 2) native_save_error_present(0x20000000);
        else native_save_error_present(0x60000000);
    }
    native_copy(data, metadata, 0x14);
}
void save_load_primary_checked(void) {
    if (save_load_primary(2)) return;
    if (save_write_status() == 2) native_save_error_present(0x50000000);
    else native_save_error_present(0x60000000);
}
void save_load_primary_async_checked(int heap) {
    if (save_load_primary_async(heap)) return;
    native_save_error_present(0x50000000);
}
int save_load_poll_checked(void) {
    if (save_load_async_poll()) {
        switch (save_write_status()) {
        case 0:
            break;
        case 2:
            native_save_error_present(0x50000000);
            break;
        case 1:
        case 3:
        case 4:
        case 5:
        case 6:
        case 7:
        default:
            save_header_invalidate(0);
            native_save_error_present(0x60000000);
            break;
        }
        return 1;
    }
    return 0;
}
