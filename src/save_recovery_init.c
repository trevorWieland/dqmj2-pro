typedef unsigned char u8;
typedef unsigned int u32;
typedef struct { u8 status; u8 locked; signed char initialized; u8 reserved; u32 pages; u32 payload; u32 blocks; u32 page_size; u32 stride; u32 capacity; } BackupControl;
typedef struct { signed char type; u8 reserved[3]; int lock_id; } BackupDevice;
extern BackupControl native_backup_control;
extern BackupDevice native_backup_device;
extern int native_backup_busy(void);
extern void native_backup_wait(void);
extern int native_lock_id_allocate(void);
extern int save_block_lock(void);
extern int save_block_unlock(void);
extern u32 native_device_config_values[];
extern int native_device_configure(u32);
extern u32 native_device_capacity(void);
extern u32 native_device_page_size(void);
int save_device_initialize(void) {
    int success = 0;
    if (!native_backup_control.initialized) {
        int lock_id;
        if (native_backup_busy()) native_backup_wait();
        native_backup_control.locked = 0;
        lock_id = native_lock_id_allocate();
        native_backup_device.lock_id = lock_id;
        if (lock_id == -3) native_backup_control.status = 1;
        else {
            native_backup_device.type = -1;
            native_backup_control.blocks = native_backup_control.stride = native_backup_control.pages = native_backup_control.payload = native_backup_control.page_size = native_backup_control.capacity = 0;
            success = 1;
            native_backup_control.initialized = 1;
            native_backup_control.status = 0;
        }
    } else native_backup_control.status = 12;
    return success;
}
int save_device_type_set(int type) {
    int success = 0;
    if (native_backup_device.lock_id != -3) {
        save_block_lock();
        if (!native_device_configure(native_device_config_values[type])) native_backup_control.status = 3;
        else {
            native_backup_device.type = type;
            native_backup_control.capacity = native_device_capacity();
            native_backup_control.page_size = native_device_page_size();
            native_backup_control.status = 0;
            success = 1;
        }
        save_block_unlock();
    } else native_backup_control.status = 2;
    return success;
}
