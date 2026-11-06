typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef struct { u8 status; u8 locked; signed char initialized; u8 reserved; u32 pages; u32 payload; u32 blocks; u32 page_size; u32 stride; u32 capacity; } BackupControl;
typedef struct { signed char type; u8 reserved[3]; int lock_id; } BackupDevice;
typedef int (*BackupSync)(u32, void *, u32);
typedef int (*BackupAsync)(u32, void *, u32, int, int);
extern BackupControl native_backup_control;
extern BackupDevice native_backup_device;
extern BackupSync native_backup_writes[];
extern BackupSync native_backup_reads[];
extern BackupAsync native_backup_async_writes[];
extern BackupAsync native_backup_async_reads[];
extern u32 native_unsigned_div(u32, u32);
extern void native_backup_lock_id(u16);
extern void native_backup_unlock_id(u16);
extern int native_backup_completed(void);
extern u32 native_backup_result(void);
int save_block_lock(void) {
    if (native_backup_control.locked) return 0;
    native_backup_control.locked = 1;
    native_backup_lock_id((u16)native_backup_device.lock_id);
    return 1;
}
int save_block_unlock(void) {
    if (!native_backup_control.locked) return 0;
    native_backup_unlock_id((u16)native_backup_device.lock_id);
    native_backup_control.locked = 0;
    return 1;
}
u32 save_block_payload_set(u32 payload) {
    u32 previous = native_backup_control.payload;
    u32 page_size;
    u32 stride;
    native_backup_control.payload = payload;
    page_size = native_backup_control.page_size;
    stride = page_size * native_unsigned_div(payload + page_size - 1, page_size);
    native_backup_control.stride = stride;
    native_backup_control.pages = native_unsigned_div(stride, page_size);
    native_backup_control.blocks = native_unsigned_div(native_backup_control.capacity, stride);
    return previous;
}
int save_block_write(u32 index, void *source, u32 bytes) {
    int success = 0;
    if (index < native_backup_control.blocks) {
        if (bytes <= native_backup_control.payload) {
            u32 offset;
            save_block_lock();
            offset = index * native_backup_control.stride;
            if (!bytes) bytes = native_backup_control.payload;
            if (native_backup_writes[native_backup_device.type](offset, source, bytes)) {
                native_backup_control.status = 0;
                success = 1;
            } else native_backup_control.status = 8;
            save_block_unlock();
        } else native_backup_control.status = 11;
    } else native_backup_control.status = 4;
    return success;
}
int save_block_write_async(u32 index, void *source, u32 bytes, int first, int second) {
    int started = 0;
    if (index < native_backup_control.blocks) {
        u32 offset;
        save_block_lock();
        offset = index * native_backup_control.stride;
        if (!bytes) bytes = native_backup_control.payload;
        native_backup_async_writes[native_backup_device.type](offset, source, bytes, first, second);
        native_backup_control.status = 0;
        started = 1;
    } else native_backup_control.status = 4;
    return started;
}
int save_block_read(u32 index, void *destination, u32 bytes) {
    int success = 0;
    if (index < native_backup_control.blocks) {
        if (bytes <= native_backup_control.payload) {
            save_block_lock();
            if (!bytes) bytes = native_backup_control.payload;
            if (native_backup_reads[native_backup_device.type](index * native_backup_control.stride, destination, bytes)) {
                native_backup_control.status = 0;
                success = 1;
            } else native_backup_control.status = 9;
            save_block_unlock();
        } else native_backup_control.status = 11;
    } else native_backup_control.status = 4;
    return success;
}
int save_block_read_async(u32 index, void *destination, u32 bytes, int first, int second) {
    int started = 0;
    if (index < native_backup_control.blocks) {
        if (bytes <= native_backup_control.payload) {
            save_block_lock();
            if (!bytes) bytes = native_backup_control.payload;
            native_backup_async_reads[native_backup_device.type](index * native_backup_control.stride, destination, bytes, first, second);
            native_backup_control.status = 0;
            started = 1;
        } else native_backup_control.status = 11;
    } else native_backup_control.status = 4;
    return started;
}
int save_block_poll_result(u8 *error) {
    int complete = native_backup_completed();
    if (complete) {
        u8 result = native_backup_result();
        u8 code;
        if (!result) code = 0;
        else if (result == 1) code = 13;
        else if (result == 2) code = 13;
        else if (result == 3) code = 3;
        else if (result == 4) code = 14;
        else if (result == 6) code = 15;
        else if (result == 7) code = 16;
        else code = 17;
        native_backup_control.status = code;
        if (error) *error = code;
    } else native_backup_control.status = 10;
    return complete;
}
int save_block_poll(u8 *error) {
    if (!save_block_poll_result(error)) {
        native_backup_control.status = 10;
        return 0;
    }
    save_block_unlock();
    native_backup_control.status = 0;
    return 1;
}
u32 save_block_locked(void) { return native_backup_control.locked; }
u32 save_block_stride(void) { return native_backup_control.stride; }
