typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct { u32 marker; u32 total_length; u32 payload_length; u8 rest[0x84]; } SaveHeader;
typedef struct { u8 status; signed char heap; u16 reserved; int (*validator)(void *); u8 *buffer; } SaveIo;
extern SaveIo native_save_io;
extern int save_payload_valid(void *);
extern int save_payload_header28_valid(void *);
extern u8 *save_main_pointer(void);
extern u8 *save_section2_pointer(void);
extern u8 *save_section3_pointer(void);
extern u8 *save_section4_pointer(void);
extern u32 save_payload_checksum(void *);
extern u32 save_header_checksum(void *);
extern void native_copy(const void *, void *, u32);
extern void native_fill(void *, int, u32);
extern void native_backup_type_set(int);
extern void native_backup_size_set(u32);
extern void native_date_get(void *);
extern void native_time_get(void *);
extern u32 native_save_stride(void);
extern void *native_allocate_tail(int, u32, int);
extern void native_free(int, void *);
extern int native_save_write_async(u32, void *, u32, int, int);
extern int native_save_write(u32, void *, u32);
extern int native_save_read(u32, void *, u32);
extern int native_save_poll(u8 *);
extern void save_header_summary(void *, void *);
void save_write_initialize(void) {
    native_backup_type_set(2);
    native_backup_size_set(0x70d0);
    native_save_io.buffer = 0;
    native_save_io.validator = save_payload_valid;
}
void save_header_initialize(SaveHeader *header) {
    header->marker = 0x5a4953;
    header->total_length = 0x10000;
    header->payload_length = 0x70d0;
    native_date_get((u8 *)header + 0xc);
    native_time_get((u8 *)header + 0x1c);
}
int save_write_start(int heap) {
    int success = 0;
    u8 *bank;
    u8 *main_state;
    u8 *section2;
    u8 *section3;
    u8 *section4;
    u32 bytes;
    native_save_io.status = 0;
    bytes = native_save_stride() * 2;
    bank = native_allocate_tail(heap, bytes, 4);
    native_save_io.buffer = bank;
    if (bank) {
        native_save_io.heap = heap;
        main_state = save_main_pointer();
        section2 = save_section2_pointer();
        section3 = save_section3_pointer();
        section4 = save_section4_pointer();
        save_header_initialize((SaveHeader *)bank);
        save_header_summary(bank + 0x28, main_state);
        native_copy(main_state, bank + 0x90, 0x39d8);
        native_copy(section2, bank + 0x3a68, 0x34);
        native_copy(section3, bank + 0x3a9c, 0x22a4);
        native_copy(section4, bank + 0x5d40, 0x1390);
        *(u32 *)(bank + 0x88) = save_payload_checksum(bank);
        *(u32 *)(bank + 0x8c) = save_header_checksum(bank);
        native_copy(bank, bank + native_save_stride(), 0x70d0);
        if (native_save_write_async(0, native_save_io.buffer, bytes, 0, 0)) success = 1;
        else native_save_io.status = 1;
    } else native_save_io.status = 8;
    return success;
}
int save_write_poll(void) {
    int done = 0;
    u8 error;
    native_save_io.status = 0;
    if (native_save_poll(&error)) {
        if (error) native_save_io.status = 1;
        if (native_save_io.buffer) {
            native_free(native_save_io.heap, native_save_io.buffer);
            native_save_io.buffer = 0;
        } else if (!native_save_io.status) native_save_io.status = 8;
        done = 1;
    }
    return done;
}
int save_read_header(u32 index, SaveHeader *output) {
    SaveHeader header;
    int valid = 0;
    if (native_save_read(index, &header, 0x90)) {
        if (header.marker == 0x5a4953) {
            if (header.total_length == 0x10000) {
                if (header.payload_length == 0x70d0) {
                    int checksum_valid = *(u32 *)((u8 *)&header + 0x8c) == save_header_checksum(&header);
                    if (checksum_valid) {
                        if (output) native_copy(&header, output, 0x90);
                        native_save_io.status = 0;
                        valid = 1;
                    } else native_save_io.status = 5;
                } else native_save_io.status = 7;
            } else native_save_io.status = 4;
        } else native_save_io.status = 3;
    } else native_save_io.status = 2;
    return valid;
}
int save_header_invalidate(u32 index) {
    SaveHeader header;
    native_fill(&header, 0, 0x90);
    if (native_save_write(index, &header, 0x90)) {
        native_save_io.status = 0;
        return 1;
    }
    native_save_io.status = 1;
    return 0;
}
u32 save_write_status(void) { return native_save_io.status; }
void save_alternate_validator_set(void) { native_save_io.validator = save_payload_header28_valid; }
u32 save_serialize_allocate(int heap) {
    u32 stride;
    u8 *main_state;
    u8 *section2;
    u8 *section3;
    u8 *section4;
    native_save_io.heap = heap;
    stride = native_save_stride();
    native_save_io.buffer = native_allocate_tail(heap, stride, 4);
    if (!native_save_io.buffer) return 0;
    main_state = save_main_pointer();
    section2 = save_section2_pointer();
    section3 = save_section3_pointer();
    section4 = save_section4_pointer();
    save_header_initialize((SaveHeader *)native_save_io.buffer);
    save_header_summary(native_save_io.buffer + 0x28, main_state);
    native_copy(main_state, native_save_io.buffer + 0x90, 0x39d8);
    native_copy(section2, native_save_io.buffer + 0x3a68, 0x34);
    native_copy(section3, native_save_io.buffer + 0x3a9c, 0x22a4);
    native_copy(section4, native_save_io.buffer + 0x5d40, 0x1390);
    *(u32 *)(native_save_io.buffer + 0x88) = save_payload_checksum(native_save_io.buffer);
    *(u32 *)(native_save_io.buffer + 0x8c) = save_header_checksum(native_save_io.buffer);
    return stride;
}
u8 *save_serialized_buffer_get(void) { return native_save_io.buffer; }
void save_serialized_buffer_free(void) {
    native_free(native_save_io.heap, native_save_io.buffer);
    native_save_io.buffer = 0;
}
