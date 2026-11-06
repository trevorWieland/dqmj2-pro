#include "native_os_context.h"
void native_arm7_wram_037fc1e0(void *arg)
{
    OSThread *currentThread = OSi_GetCurrentThread();
    OSThreadDestructor destructor = currentThread->destructor;

    if (destructor)
    {
        currentThread->destructor = NULL;
        destructor(arg);
        (void)OS_DisableInterrupts();
    }

    OSi_ExitThread_Destroy();
}
