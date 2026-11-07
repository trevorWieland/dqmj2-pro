#include "context000.h"

void native_host_arm7_wram_038046ac(SPITpData *data, s32 range, u16 *density)
{
    u16 temp_pos;
    u32 temp_touch;
    u16 density_x, density_y;
    *density = 0;
    ((void) 0) ;
    if (range < 0) {
        range = -range;
    }
    temp_touch = native_host_arm7_wram_038043a4();
    if (temp_touch == TOUCH_OFF) {
        data->e.x = 0;
        data->e.y = 0;
        data->e.touch = SPI_TP_TOUCH_OFF;
        data->e.validity = SPI_TP_VALIDITY_INVALID_XY;
        native_host_arm7_data_03809ea8 = 0;
        return;
    }
    data->e.validity = native_host_arm7_arm_038044bc(&temp_pos, range, TP_DETECT_AXIS_X, &density_x);
    data->e.x = temp_pos;
    if (native_host_arm7_arm_038044bc(&temp_pos, range, TP_DETECT_AXIS_Y, &density_y) == SPI_TP_VALIDITY_INVALID_Y) {
        data->e.validity |= SPI_TP_VALIDITY_INVALID_Y;
    }
    data->e.y = temp_pos;
    TP_SPIChangeMode(SPI_TRANSMODE_CONTINUOUS);
    for (int i = 0; i < 12; i++) {
        native_host_arm7_arm_03804498();
    }
    TP_SPIChangeMode(SPI_TRANSMODE_1BYTE);
    native_host_arm7_arm_03804498();
    if (temp_touch == TOUCH_MAY_OFFNOISE) {
        data->e.validity = SPI_TP_VALIDITY_INVALID_XY;
    }
    temp_touch = native_host_arm7_wram_038043a4();
    switch (temp_touch) {
    case TOUCH_MAY_OFFNOISE:
        data->e.touch = SPI_TP_TOUCH_ON;
        data->e.validity = SPI_TP_VALIDITY_INVALID_XY;
        native_host_arm7_data_03809ea8 = 0;
        break;
    case TOUCH_ON:
        data->e.touch = SPI_TP_TOUCH_ON;
        native_host_arm7_data_03809ea8 = 1;
        *density = (density_x >= density_y) ? density_x : density_y;
        break;
    case TOUCH_OFF:
        data->e.touch = SPI_TP_TOUCH_OFF;
        native_host_arm7_data_03809ea8 = 0;
        break;
    default:
        native_host_arm7_arm_037fde70() ;
    }
}
