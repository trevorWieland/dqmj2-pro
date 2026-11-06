#include "context.h"
void native_main_020a8b1c (unsigned char *input, unsigned int len, char output[33])
{
    MD5_CTX ctx;
    unsigned char digest[16];

    MD5Init(&ctx);
    MD5Update(&ctx, input, len);
    MD5Final(digest, &ctx);
    MD5Print(digest, output);

}