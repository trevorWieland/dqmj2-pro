#include "native_os_context.h"
void native_arm7_wram_037fc96c(OSThread * thread) {
    OSMutex * mutex;
    while (thread->mutexQueue.head) {
        mutex = OSi_RemoveMutexLinkFromQueue(&thread->mutexQueue);
        mutex->count = 0;
        mutex->thread = NULL;
        OS_WakeupThread(&mutex->queue);
    }
}
