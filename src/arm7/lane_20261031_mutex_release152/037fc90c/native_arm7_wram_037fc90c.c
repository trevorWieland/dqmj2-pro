#include "native_os_context.h"
void native_arm7_wram_037fc90c(OSMutex* mutex) {
    OSIntrMode mode;
    OSThread* current;
    
    mode = OS_DisableInterrupts();
    current = OS_GetCurrentThread();
    if (mutex->thread == current) {
        if (--mutex->count == 0) {
            OSi_DequeueItem(current, mutex);
            mutex->thread = NULL;
            OS_WakeupThread(&mutex->queue);
        }
    }
    (void)OS_RestoreInterrupts(mode);
}
