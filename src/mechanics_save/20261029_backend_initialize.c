typedef unsigned char u8;
typedef unsigned int u32;
typedef signed int s32;
typedef struct { u8 prefix[0x1c]; u32 first; u32 second; u32 bytes; s32 pending; u8 fields2c[12]; u32 callback; u32 argument; u8 fields40[0xd4]; u32 flags; } BackupBackend;
typedef struct { u32 first; u8 middle[0x1c]; u32 callback; } BackupRuntime;
extern BackupBackend native_backup_backend;
extern BackupRuntime native_backup_runtime;
extern void native_backup_common_initialize(void);
extern u32 native_backup_worker_callback_get(void);
extern void native_backup_fifo_initialize(void);
void saved_20261029_backend_initialize(void) {
    BackupBackend *backend = &native_backup_backend;
    BackupRuntime *runtime;
    if (backend->flags) return;
    runtime = &native_backup_runtime;
    backend->flags = 1;
    backend->first = backend->second = backend->bytes = 0;
    backend->pending = -1;
    backend->callback = 0;
    backend->argument = 0;
    runtime->first = 0;
    native_backup_common_initialize();
    runtime->callback = native_backup_worker_callback_get();
    native_backup_fifo_initialize();
}
