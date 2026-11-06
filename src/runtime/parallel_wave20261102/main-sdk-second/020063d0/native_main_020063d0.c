#include "context_00.h"
void native_main_020063d0 (void)
{
    if (native_data_main_020e33c0.field_0004 <= 0) {
        OSThreadInfo * info = &native_data_main_020e33c0.field_0024;
        if (info->irqDepth > 0 || native_fn_02008058() == OS_PROCMODE_IRQ) {
            info->isNeedRescheduling = 1 ;
        } else {
            OSThread * currentThread, * nextThread;
            currentThread = (*native_data_main_020e33c0.field_0008) ;
            nextThread = native_fn_020069b4();
            if (currentThread == nextThread || !nextThread) {
                return;
            }
            if (currentThread->state != OS_THREAD_STATE_TERMINATED
                && native_fn_02006d4c(&currentThread->context)) {
                return;
            }
            if (native_data_main_020e33c0.field_0000) {
                ((OSSwitchThreadCallback)native_data_main_020e33c0.field_0000)(currentThread,
                                                                           nextThread);
            }
            if (info->switchCallback) {
                ((OSSwitchThreadCallback)info->switchCallback)(currentThread, nextThread);
            }
            OS_SetCurrentThread(nextThread);
            native_fn_02006d98(&nextThread->context);
        }
    }
}
