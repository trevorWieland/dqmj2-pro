#include "context.h"
void native_main_0209c24c (GT2Connection connection, GT2Byte * message, int len, GT2Bool reliable)
{
    DWCi_RecvCallback(connection, message, len, reliable);
}
