WlParamSetCfm *WMSP_WL_ParamSetGameInfo(u16 *buf, u16 gameInfoLength, u16 *gameInfo);

static inline WMSPWork *WMSP_GetSystemWork(void)
{
    return &wmspW;
}
