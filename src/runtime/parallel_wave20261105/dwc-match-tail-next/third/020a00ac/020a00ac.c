#include "context.h"
int native_main_020a00ac (u8 command, int profileID, u32 ip, u16 port, const u32 data[], int len)
{
    char message[DWC_MATCH_COMMAND_ADD_MESSAGE_MAX];
    char tmpStr[16];
    int msgLen = 0, tmpLen;
    int result;
    int i;
    if ((native_fn_020a3d70()->qr2MatchType == DWC_MATCH_TYPE_ANYBODY) ||
        (((native_fn_020a3d70()->qr2MatchType == DWC_MATCH_TYPE_SC_CL) ||
          native_fn_020a3d70()->distantFriend) &&
         (command == DWC_MATCH_COMMAND_TELL_ADDR))) {
        result = (int)native_fn_020a020c(command, ip, port, data, len);
    } else {
        if (data && len) {
            msgLen = native_fn_020061ac(message, sizeof(message), native_data_020e01a4, data[0]);
            for (i = 1; i < len; i++) {
                tmpLen = native_fn_020061ac(tmpStr, sizeof(tmpStr), native_data_020e0298, data[i]);
                if (msgLen + tmpLen + 1 > sizeof(message)) {
                    SDK_ASSERTMSG(0, "Match command is too long.");
                    break;
                }
                native_fn_02008e0c(tmpStr, &message[msgLen], (u32)tmpLen);
                msgLen += tmpLen;
            }
        }
        message[msgLen] = '\0';
        result = (int)native_fn_020a02b4(native_fn_020a3d70()->pGpObj, command, profileID, message);
    }
    if ((command == DWC_MATCH_COMMAND_RESV_OK) ||
        (command == DWC_MATCH_COMMAND_TELL_ADDR) ||
        (command == DWC_MATCH_COMMAND_LINK_CLS_REQ) ||
        (command == DWC_MATCH_COMMAND_LINK_CLS_SUC)) {
        native_fn_020a3d70()->cmdCnt.command = command;
        native_fn_020a3d70()->cmdCnt.port = port;
        native_fn_020a3d70()->cmdCnt.ip = ip;
        native_fn_020a3d70()->cmdCnt.profileID = profileID;
        native_fn_020a3d70()->cmdCnt.len = len;
        native_fn_020a3d70()->cmdCnt.sendTime = native_fn_02007a9c();
        if (data && len) {
            native_fn_02008c28(data, native_fn_020a3d70()->cmdCnt.data, (u32)len * 4);
        }
    }
    return result;
}
