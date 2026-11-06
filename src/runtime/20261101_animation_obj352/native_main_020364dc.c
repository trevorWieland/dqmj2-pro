typedef unsigned int u32;
int native_main_020364dc(int areaWidth, int areaHeight);
int native_main_020364dc (int areaWidth, int areaHeight)
{
    const u32 w = (unsigned int)areaWidth;
    const u32 h = (unsigned int)areaHeight;
    const u32 w8 = w / 8;
    const u32 h8 = h / 8;
    const u32 w4 = (w & 4) >> 2;
    const u32 h4 = (h & 4) >> 2;
    const u32 wcp = ((w & 2) >> 1) + (w & 1);
    const u32 hcp = ((h & 2) >> 1) + (h & 1);
    int ret = 0;
    ret += w8 * h8;
    ret += (wcp * 2 + w4) * h8;
    ret += (hcp * 2 + h4) * w8;
    ret += (wcp + w4) * (hcp + h4);
    return ret;
}
