#include "context.h"
int native_main_0209b2bc (const char * key, char * value, const char * string, char separator)
{
    const char * pSrcBegin;
    char * pSrcEnd;
    int len;
    SDK_ASSERT(key);
    if (!value) return -1;
    pSrcBegin = strchr(string, separator);
    if (!pSrcBegin) return -1;
    while (1) {
        if (!strncmp(pSrcBegin + 1, key, strlen(key)) &&
            (pSrcBegin[strlen(key) + 1] == separator)) {
            break;
        }
        pSrcBegin = strchr(pSrcBegin + 1, separator);
        if (!pSrcBegin) return -1;
        pSrcBegin = strchr(pSrcBegin + 1, separator);
        if (!pSrcBegin) return -1;
    }
    pSrcBegin = strchr(pSrcBegin + 1, separator);
    if (!pSrcBegin) return -1;
    pSrcBegin++;
    pSrcEnd = strchr(pSrcBegin, separator);
    if (pSrcEnd) len = (int)(pSrcEnd - pSrcBegin);
    else len = (int)strlen(pSrcBegin);
    strncpy(value, pSrcBegin, (u32)len);
    value[len] = '\0';
    return len;
}
