typedef unsigned long long u64;
int native_main_02023db4(u64 x) {
 x = x - ((x >> 1) & 0x5555555555555555ULL);
 x = (x & 0x3333333333333333ULL) + ((x >> 2) & 0x3333333333333333ULL);
 x = (x + (x >> 4)) & 0x0f0f0f0f0f0f0f0fULL;
 x += x >> 8;
 x += x >> 16;
 x += x >> 32;
 return x & 255;
}
