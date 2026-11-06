typedef unsigned char u8;
typedef unsigned int u32;
typedef struct { u8 low:4; u8 high:4; } NativeNibbles;
typedef struct { u8 prefix[48]; NativeNibbles pairs[14]; u8 tail[24]; } NativeEktRecord;
extern NativeEktRecord *native_ekt_record(int);
extern u32 native_variant_offset(int);
extern u8 native_projection_table[][3];
extern void native_fill(void *, u32, u32);
u8 saved_projection_value(int species, int variant, int raw) {
    if (raw >= 8) {
        if (native_variant_offset(species) == 1) return native_projection_table[raw - 8][variant * 2];
        return native_projection_table[raw - 8][variant];
    }
    return (u8)raw;
}
void saved_projection_ekt(int species, int variant, u8 *output) {
    NativeEktRecord *kind = native_ekt_record(species);
    output[1] = saved_projection_value(species, variant, kind->pairs[0].low);
    output[2] = saved_projection_value(species, variant, kind->pairs[0].high);
    output[3] = saved_projection_value(species, variant, kind->pairs[1].low);
    output[4] = saved_projection_value(species, variant, kind->pairs[1].high);
    output[5] = saved_projection_value(species, variant, kind->pairs[2].low);
    output[6] = saved_projection_value(species, variant, kind->pairs[2].high);
    output[7] = saved_projection_value(species, variant, kind->pairs[3].low);
    output[8] = saved_projection_value(species, variant, kind->pairs[3].high);
    output[9] = saved_projection_value(species, variant, kind->pairs[4].low);
    output[10] = saved_projection_value(species, variant, kind->pairs[4].high);
    output[11] = saved_projection_value(species, variant, kind->pairs[5].low);
    output[12] = saved_projection_value(species, variant, kind->pairs[5].high);
    output[13] = saved_projection_value(species, variant, kind->pairs[6].low);
    output[14] = saved_projection_value(species, variant, kind->pairs[6].high);
    output[15] = saved_projection_value(species, variant, kind->pairs[7].low);
    output[16] = saved_projection_value(species, variant, kind->pairs[7].high);
    output[17] = saved_projection_value(species, variant, kind->pairs[8].low);
    output[18] = saved_projection_value(species, variant, kind->pairs[8].high);
    output[19] = saved_projection_value(species, variant, kind->pairs[9].low);
    output[20] = saved_projection_value(species, variant, kind->pairs[9].high);
    output[21] = saved_projection_value(species, variant, kind->pairs[10].low);
    output[22] = saved_projection_value(species, variant, kind->pairs[10].high);
    output[23] = saved_projection_value(species, variant, kind->pairs[11].low);
    output[24] = saved_projection_value(species, variant, kind->pairs[11].high);
    output[25] = saved_projection_value(species, variant, kind->pairs[12].low);
    output[26] = saved_projection_value(species, variant, kind->pairs[12].high);
    output[27] = saved_projection_value(species, variant, kind->pairs[13].low);
    output[28] = saved_projection_value(species, variant, kind->pairs[13].high);
}
void saved_projection_feature_add(int feature, u8 *output) {
    int index;
    switch (feature) {
    case 201: index = 1; break;
    case 202: index = 2; break;
    case 203: index = 3; break;
    case 204: index = 4; break;
    case 205: index = 5; break;
    case 206: index = 6; break;
    case 211: index = 7; break;
    case 212: index = 8; break;
    case 213: index = 9; break;
    case 214: index = 10; break;
    case 215: index = 11; break;
    case 216: index = 12; break;
    case 217: index = 13; break;
    case 218: index = 14; break;
    case 219: index = 15; break;
    case 220: index = 16; break;
    case 221: index = 17; break;
    case 222: index = 18; break;
    case 223: index = 19; break;
    case 224: index = 20; break;
    case 225: index = 21; break;
    case 226: index = 22; break;
    case 227: index = 23; break;
    case 208: index = 24; break;
    case 228: index = 25; break;
    case 207: index = 26; break;
    case 209: index = 27; break;
    case 210: index = 28; break;
    default: return;
    }
    if (output[index] < 5) {
        int value = output[index] + 2;
        if (value >= 5) value = 5;
        output[index] = value;
    }
}
void saved_projection_with_features(int species, int variant, const u8 *features, u8 *output) {
    int index;
    native_fill(output, 0, 32);
    saved_projection_ekt(species, variant, output);
    index = 0;
    do {
        int feature = features[index];
        if (!feature) return;
        saved_projection_feature_add(feature, output);
        index++;
    } while (index < 64);
}
