#include "context.h"
BOOL native_main_020a039c (u8 command,
                                          int srcPid,
                                          u32 srcIP,
                                          u16 srcPort,
                                          const u32 data[],
                                          int len)
{
#pragma unused(len)
    u8 sendCommand;
    u8 aid;
    u16 port = 0;
    u32 ip = 0;
    u32 aidIdx;
    u32 senddata[DWC_MAX_MATCH_IDX_LIST + 1];
    int profileID;
    int sendlen = 0;
    int result;
    int i;
    SBError sbError;
    NegotiateError nnError;
    struct sockaddr_in remoteaddr;
    if (!native_fn_020a3d70() || (native_fn_020a3d70()->state == DWC_MATCH_STATE_INIT)) {
        return TRUE;
    }
    if ((native_fn_0209bc88() == DWC_STATE_MATCHING) &&
        (native_fn_020a3d70()->state == DWC_MATCH_STATE_CL_WAITING) &&
        (srcPid == native_fn_020a3d70()->sbPidList[0])) {
        native_fn_020a2cc8();
    }
    switch (command) {
    case DWC_MATCH_COMMAND_RESERVATION:
    case DWC_MATCH_COMMAND_RESV_PRIOR:
        if (native_fn_020a3d70()->qr2MatchType != DWC_MATCH_TYPE_ANYBODY) {
            srcIP = data[1];
            srcPort = (u16)data[2];
            DWC_Printf(DWC_REPORTFLAG_DEBUG, "friend IP:%x, port:%d\n",
                       srcIP, srcPort);
        }
        sendCommand =
            native_fn_020a0e88(srcPid, srcIP, srcPort, data[0],
                                  command == DWC_MATCH_COMMAND_RESV_PRIOR ? TRUE : FALSE);
        if (sendCommand == DWC_MATCH_COMMAND_RESV_OK) {
#ifdef DWC_LIMIT_FRIENDS_MATCH_VALID
            native_fn_020a3d70()->friendAcceptBit = 0;
#endif
            result = native_fn_020a10d0(srcPid, srcIP, srcPort);
            if (native_fn_020a1258(result)) return FALSE;
            if (native_fn_020a3d70()->qr2MatchType == DWC_MATCH_TYPE_SC_SV) {
                if (native_fn_020a3d70()->newClientCallback) {
                    native_fn_020a3d70()->newClientCallback(native_fn_0209d168(srcPid),
                                                          native_fn_020a3d70()->newClientParam);
                }
            }
            senddata[0] = native_fn_020a3d70()->qr2NNFinishCount;
            for (sendlen = 1; sendlen <= native_fn_020a3d70()->qr2NNFinishCount; sendlen++) {
                senddata[sendlen] = (u32)native_fn_020a3d70()->sbPidList[sendlen];
            }
            senddata[sendlen++] = native_fn_020a3d70()->qr2IP;
            senddata[sendlen++] = native_fn_020a3d70()->qr2Port;
            native_fn_020a3d7c(DWC_MATCH_STATE_SV_OWN_NN);
        } else if (sendCommand == DWC_MATCH_COMMAND_RESV_DENY)   {
            if ((native_fn_020a3d70()->qr2NumEntry > 0) &&
                (native_fn_020a3d70()->qr2NNFinishCount == native_fn_020a3d70()->qr2NumEntry)) {
                if (native_fn_020a3d70()->qr2MatchType == DWC_MATCH_TYPE_SC_SV) {
                    senddata[0] = DWC_MATCH_RESV_DENY_REASON_SV_FULL;
                    sendlen = 1;
                }
            }
        }
        if (sendCommand != DWC_MATCH_COMMAND_DUMMY) {
            result = native_fn_020a00ac(sendCommand, srcPid, srcIP, srcPort, senddata, sendlen);
            if (native_fn_020a1258(result)) return FALSE;
        }
        break;
    case DWC_MATCH_COMMAND_RESV_OK:
        if (native_fn_020a3d70()->state != DWC_MATCH_STATE_CL_WAIT_RESV) break;
        DWC_Printf(DWC_REPORTFLAG_MATCH_NN, "Succeeded NN reservation.\n");
        if (srcPid != native_fn_020a3d70()->reqProfileID) {
            break;
        }
        native_fn_020a3d70()->priorProfileID = 0;
        native_fn_020a3d70()->resvWaitCount = 0;
        native_fn_020a3d70()->cmdTimeoutTime = 0;
        native_fn_020a3d70()->cmdResendFlag = FALSE;
        native_fn_020a3d70()->qr2IPList[0] = data[data[0] + 1];
        native_fn_020a3d70()->qr2PortList[0] = (u16)data[data[0] + 2];
        native_fn_020a3d70()->searchIP = data[data[0] + 1];
        native_fn_020a3d70()->searchPort = (u16)data[data[0] + 2];
        DWC_Printf(DWC_REPORTFLAG_DEBUG, "Server IP:%x, port:%d\n",
                   native_fn_020a3d70()->searchIP, native_fn_020a3d70()->searchPort);
        if (native_fn_020a3d70()->qr2MatchType == DWC_MATCH_TYPE_FRIEND) {
            if (native_fn_020a1edc(&data[1], data[0])) {
                if (native_fn_020a3d70()->gt2NumConnection) {
                    native_fn_020a121c(srcPid, data);
                }
            } else {
                DWC_Printf(DWC_REPORTFLAG_MATCH_NN,
                           "But some clients are not friends.\n");
                result = native_fn_020a16a8(srcPid);
                if (native_fn_020a1258(result)) return FALSE;
                result = native_fn_020a13d8(FALSE, FALSE, srcPid);
                if (native_fn_020a1258(result)) return FALSE;
                break;
            }
        }
        if (native_fn_020a3d70()->qr2MatchType == DWC_MATCH_TYPE_ANYBODY) {
            if (native_fn_020a3d70()->gt2NumConnection) {
                native_fn_020a121c(srcPid, data);
                result = native_fn_020a1908();
                if (native_fn_020a1258(result)) return FALSE;
            }
            native_fn_020a3d7c(DWC_MATCH_STATE_CL_NN);
            nnError = native_fn_0209fde8(0, 0, native_fn_020a699c(native_fn_020a3d70()->sbObj, 0));
            if (native_fn_020a3154(nnError)) return FALSE;
        } else {
            native_fn_020a3d7c(DWC_MATCH_STATE_CL_SEARCH_NN_HOST);
            sbError = native_fn_0209fc38(srcPid);
            if (native_fn_020a304c(sbError)) return FALSE;
        }
        break;
    case DWC_MATCH_COMMAND_RESV_DENY:
        if ((native_fn_020a3d70()->state != DWC_MATCH_STATE_CL_WAIT_RESV) ||
            (srcPid != native_fn_020a3d70()->reqProfileID))
            break;
        DWC_Printf(DWC_REPORTFLAG_MATCH_NN, "Reservation was denied by %u.\n", srcPid);
        if (len > 0) {
            if (data[0] == DWC_MATCH_RESV_DENY_REASON_SV_FULL) {
                DWC_Printf(DWC_REPORTFLAG_MATCH_NN, "Game server is fully occupied.\n");
                native_fn_0209f130(DWC_ERROR_SERVER_FULL, 0);
                return FALSE;
            }
        }
        return native_fn_020a1608(native_fn_020a3d70()->reqProfileID);
        break;
    case DWC_MATCH_COMMAND_RESV_WAIT:
        if (native_fn_020a3d70()->state != DWC_MATCH_STATE_CL_WAIT_RESV) break;
        if (srcPid == native_fn_020a3d70()->reqProfileID) {
            native_fn_020a3d70()->cmdTimeoutStartTick = native_fn_02007a9c();
            if ((native_fn_020a3d70()->priorProfileID &&
                 (native_fn_020a3d70()->resvWaitCount < DWC_RESV_COMMAND_RETRY_MAX)) ||
                (native_fn_020a3d70()->qr2MatchType == DWC_MATCH_TYPE_SC_CL)) {
                native_fn_020a3d70()->cmdResendFlag = TRUE;
                native_fn_020a3d70()->cmdResendTick = native_fn_02007a9c();
                if (native_fn_020a3d70()->qr2MatchType != DWC_MATCH_TYPE_SC_CL) {
                    native_fn_020a3d70()->resvWaitCount++;
                }
                break;
            }
            native_fn_020a3d70()->priorProfileID = 0;
            native_fn_020a3d70()->resvWaitCount = 0;
            if (native_fn_020a3d70()->qr2MatchType == DWC_MATCH_TYPE_ANYBODY) {
                native_fn_020a3d7c(DWC_MATCH_STATE_CL_SEARCH_HOST);
                native_fn_020a3d70()->sbUpdateFlag = DWC_SB_UPDATE_INTERVAL_SHORT;
                native_fn_020a3d70()->sbUpdateTick = native_fn_02007a9c();
            } else if (native_fn_020a3d70()->qr2MatchType == DWC_MATCH_TYPE_FRIEND)   {
                (void)native_fn_020a13d8(TRUE, FALSE, 0);
            }
        }
        break;
    case DWC_MATCH_COMMAND_RESV_CANCEL:
        if (native_fn_020a3d70()->qr2IsReserved &&
            (srcPid == native_fn_020a3d70()->qr2Reservation)) {
            if ((native_fn_020a3d70()->qr2MatchType == DWC_MATCH_TYPE_SC_SV) &&
                (native_fn_020a3d70()->gt2NumConnection == 1) &&
                (native_fn_020a3d70()->sbPidList[1] == srcPid)) {
                native_fn_020b4540(*native_fn_020a3d70()->pGt2Socket);
            }
            if (!native_fn_020a16e4(srcPid)) return FALSE;
        }
        break;
    case DWC_MATCH_COMMAND_TELL_ADDR:
        ip = data[0];
        port = (u16)data[1];
        DWC_Printf(DWC_REPORTFLAG_MATCH_NN,
                   "NN parent is behind same NAT as me. Received IP %x & port %d\n",
                   ip, port);
        if (native_fn_020a3d70()->state == DWC_MATCH_STATE_CL_WAITING) {
            native_fn_020a3d7c(DWC_MATCH_STATE_CL_NN);
        } else if (((native_fn_020a3d70()->state != DWC_MATCH_STATE_CL_NN) &&
                    (native_fn_020a3d70()->state != DWC_MATCH_STATE_SV_OWN_NN)) ||
                   (srcPid != native_fn_020a3d70()->qr2Reservation)) {
            DWC_Printf(DWC_REPORTFLAG_MATCH_NN,
                       "But already canceled reservation.\n");
            break;
        }
        native_fn_020a3d70()->cmdCnt.command = DWC_MATCH_COMMAND_DUMMY;
        if (native_fn_020a3d70()->sbPidList[native_fn_020a3d70()->gt2NumConnection + 1] != srcPid) {
            native_fn_020a3d70()->sbPidList[native_fn_020a3d70()->gt2NumConnection + 1] = srcPid;
        }
        remoteaddr.sin_addr.s_addr = ip;
        remoteaddr.sin_port = SO_HtoNs(port);
        native_fn_020a3d70()->nnInfo.isQR2 = 1;
        native_fn_020a3a4c(nr_success,
                                 native_fn_020b45a0(*native_fn_020a3d70()->pGt2Socket),
                                 &remoteaddr, &native_fn_020a3d70()->nnInfo);
        native_fn_020a3d70()->nnFinishTime = 0;
        break;
    case DWC_MATCH_COMMAND_NEW_PID_AID:
        if ((native_fn_020a3d70()->state != DWC_MATCH_STATE_CL_WAITING) ||
            (srcPid != native_fn_020a3d70()->sbPidList[0])) {
            DWC_Printf(DWC_REPORTFLAG_DEBUG,
                       "Ignore delayed NEW_PID_AID command.\n");
            break;
        }
        profileID = (int)data[0];
        aid = (u8)data[1];
#ifdef DWC_LIMIT_FRIENDS_MATCH_VALID
        if ((native_fn_020a3d70()->qr2MatchType == DWC_MATCH_TYPE_FRIEND) &&
            !native_fn_020a3d70()->distantFriend) {
            senddata[0] = (u32)native_fn_020a2b44(profileID);
            DWC_Printf(DWC_REPORTFLAG_MATCH_NN,
                       "profileID %d is acceptable? - %d.\n",
                       profileID, senddata[0]);
            result = native_fn_020a00ac(DWC_MATCH_COMMAND_FRIEND_ACCEPT,
                                           srcPid, srcIP, srcPort,
                                           senddata, 1);
            if (native_fn_020a1258(result)) return FALSE;
        }
#endif
        native_fn_020a3d70()->sbPidList[native_fn_020a3d70()->qr2NNFinishCount + 1] = profileID;
        native_fn_020a3d70()->aidList[native_fn_020a3d70()->qr2NNFinishCount + 1] = aid;
        native_fn_020b748c(native_fn_020a3d70()->qr2Obj);
        if (native_fn_020a3d70()->newClientCallback) {
            native_fn_020a3d70()->newClientCallback(native_fn_0209d168(profileID),
                                                  native_fn_020a3d70()->newClientParam);
        }
        DWC_Printf(DWC_REPORTFLAG_MATCH_NN,
                   "Received new client's profileID = %u & aid = %d.\n",
                   profileID, aid);
        break;
    case DWC_MATCH_COMMAND_LINK_CLS_REQ:
        if ((native_fn_020a3d70()->state != DWC_MATCH_STATE_CL_WAITING) ||
            (srcPid != native_fn_020a3d70()->sbPidList[0])) {
            DWC_Printf(DWC_REPORTFLAG_DEBUG,
                       "Ignore delayed LINK_CLS_REQ command.\n");
            break;
        }
        profileID = (int)data[0];
        if (!profileID) {
            aidIdx = data[1];
            aid = (u8)data[2];
            native_fn_020a3d70()->aidList[aidIdx] = aid;
            native_fn_020a3d70()->sbPidList[aidIdx] = native_fn_020a3d70()->profileID;
            native_fn_020a19b4(DWC_PP_CONNECTION_CL_FINISH_CONNECT);
        } else {
            aidIdx = data[1];
            aid = (u8)data[2];
            if ((native_fn_020a3d70()->sbPidList[aidIdx] == profileID) &&
                (aidIdx == native_fn_020a3d70()->gt2NumConnection - 1)) {
                DWC_Printf(DWC_REPORTFLAG_MATCH_NN,
                           "Resend command %d for delayed command %d.\n",
                           DWC_MATCH_COMMAND_LINK_CLS_SUC,
                           DWC_MATCH_COMMAND_LINK_CLS_REQ);
                result =
                    native_fn_020a00ac(DWC_MATCH_COMMAND_LINK_CLS_SUC,
                                          srcPid,
                                          native_fn_020a3d70()->qr2IPList[0],
                                          native_fn_020a3d70()->qr2PortList[0],
                                          (u32 *)&profileID, 1);
                if (native_fn_020a1258(result)) return FALSE;
                break;
            }
            native_fn_020a3d70()->sbPidList[aidIdx] = profileID;
            native_fn_020a3d70()->aidList[aidIdx] = aid;
            native_fn_020a3d70()->qr2IPList[aidIdx] = data[3];
            native_fn_020a3d70()->qr2PortList[aidIdx] = (u16)data[4];
            native_fn_020a3d70()->searchIP = data[3];
            native_fn_020a3d70()->searchPort = (u16)data[4];
            DWC_Printf(DWC_REPORTFLAG_DEBUG, "Client IP:%x, port:%d\n", native_fn_020a3d70()->searchIP, native_fn_020a3d70()->searchPort);
            native_fn_020a3d7c(DWC_MATCH_STATE_CL_SEARCH_NN_HOST);
            DWC_Printf(DWC_REPORTFLAG_MATCH_NN, "Next, try to connect to %u.\n", profileID);
            sbError = native_fn_0209fc38(profileID);
            if (native_fn_020a304c(sbError)) return FALSE;
            native_fn_020a3d70()->cmdTimeoutTime = 0;
            native_fn_020a3d70()->cmdResendFlag = FALSE;
        }
        break;
    case DWC_MATCH_COMMAND_LINK_CLS_SUC:
        if ((native_fn_020a3d70()->state == DWC_MATCH_STATE_SV_WAIT_CL_LINK) &&
            (native_fn_020a3d70()->sbPidList[native_fn_020a3d70()->clLinkProgress + 1] == data[0])) {
            native_fn_020a3d70()->clLinkProgress++;
            native_fn_020a19b4(DWC_PP_CONNECTION_SV_CONNECT);
        } else {
            DWC_Printf(DWC_REPORTFLAG_MATCH_NN, "Ignore delayed command %d.\n",
                       DWC_MATCH_COMMAND_LINK_CLS_SUC);
        }
        break;
    case DWC_MATCH_COMMAND_CLOSE_LINK:
        if ((native_fn_020a3d70()->state != DWC_MATCH_STATE_CL_WAITING) &&
            (native_fn_020a3d70()->state != DWC_MATCH_STATE_WAIT_CLOSE)) {
            DWC_Printf(DWC_REPORTFLAG_DEBUG,
                       "Ignore delayed CLOSE_LINK command.\n");
            break;
        }
        if ((native_fn_020a3d70()->qr2MatchType == DWC_MATCH_TYPE_ANYBODY) ||
            native_fn_020a1edc(&data[1], data[0])) {
            native_fn_020a3d70()->priorProfileID = (int)data[1];
            native_fn_020a3d70()->resvWaitCount = 0;
            DWC_Printf(DWC_REPORTFLAG_MATCH_NN,
                       "Received close command. Next try to %u.\n",
                       data[1]);
        } else {
            native_fn_020a3d70()->priorProfileID = 0;
            DWC_Printf(DWC_REPORTFLAG_MATCH_NN,
                       "Received close command. Server %u or its clients are not friends.\n",
                       data[1]);
        }
        if (native_fn_020a3d70()->gt2NumConnection) {
            native_fn_020b4540(*native_fn_020a3d70()->pGt2Socket);
        } else {
            if (native_fn_020a22b4()) return FALSE;
        }
        break;
    case DWC_MATCH_COMMAND_CANCEL:
        if (srcPid != native_fn_020a3d70()->sbPidList[0]) {
            DWC_Printf(DWC_REPORTFLAG_DEBUG,
                       "Ignore delayed CANCEL command.\n");
            break;
        }
        DWC_Printf(DWC_REPORTFLAG_MATCH_NN,
                   "Received cancel command from %u data[0] = %d.\n",
                   srcPid, data[0]);
        DWC_Printf(DWC_REPORTFLAG_DEBUG,
                   "numHost nn=%d gt2=%d, state %d\n",
                   native_fn_020a3d70()->qr2NNFinishCount,
                   native_fn_020a3d70()->gt2NumConnection, native_fn_020a3d70()->state);
        if ((native_fn_020a3d70()->qr2MatchType == DWC_MATCH_TYPE_ANYBODY) ||
            (native_fn_020a3d70()->qr2MatchType == DWC_MATCH_TYPE_FRIEND)) {
            if (!native_fn_020a1878(srcPid)) return FALSE;
        } else if (native_fn_020a3d70()->qr2MatchType == DWC_MATCH_TYPE_SC_CL)   {
            native_fn_020a3d70()->cbEventPid = srcPid;
            native_fn_020a2394();
            native_fn_020a21e0(DWC_MATCH_RESET_ALL);
        }
        break;
    case DWC_MATCH_COMMAND_CANCEL_SYN:
    case DWC_MATCH_COMMAND_CANCEL_SYN_ACK:
    case DWC_MATCH_COMMAND_CANCEL_ACK:
        if (!native_fn_020a277c(srcPid, command, data[0]))
            return FALSE;
        break;
    case DWC_MATCH_COMMAND_SC_CLOSE_CL:
        if (srcPid != native_fn_020a3d70()->sbPidList[0]) return TRUE;
        DWC_Printf(DWC_REPORTFLAG_DEBUG, "Close shutdown client.\n");
        for (i = 0; i < len; i++) {
            aid = native_fn_020a2c38((int)data[i], FALSE);
            if (aid != 0xff) {
                native_fn_0209bba0(aid);
            }
        }
        break;
    case DWC_MATCH_COMMAND_POLL_TIMEOUT:
        if (native_data_021d1b88 && native_data_021d1b88->valid &&
            (OS_TicksToMilliSeconds(native_fn_02007a9c() - native_data_021d1b88->startTime) >= native_data_021d1b88->timeout)) {
            senddata[0] = 1;
            DWC_Printf(DWC_REPORTFLAG_MATCH_GT2,
                       "[OPT_MIN_COMP] time is %lu.\n",
                       OS_TicksToMilliSeconds(native_fn_02007a9c() - native_data_021d1b88->startTime));
        } else {
            senddata[0] = 0;
        }
        result = native_fn_020a00ac(DWC_MATCH_COMMAND_POLL_TO_ACK,
                                       srcPid, srcIP, srcPort,
                                       senddata, 1);
        if (native_fn_020a1258(result)) return FALSE;
        break;
    case DWC_MATCH_COMMAND_POLL_TO_ACK:
        if (native_fn_020a3d70()->state == DWC_MATCH_STATE_SV_POLL_TIMEOUT) {
            aid = native_fn_020a2c38(srcPid, FALSE);
            if (aid != 0xff) {
                native_data_021d1b88->recvBit |= 1u << aid;
                if (data[0]) {
                    native_data_021d1b88->timeoutBit |= 1u << aid;
                }
            }
        }
        break;
    case DWC_MATCH_COMMAND_SC_CONN_BLOCK:
        native_fn_0209f130(DWC_ERROR_MO_SC_CONNECT_BLOCK, 0);
        return FALSE;
#ifdef DWC_LIMIT_FRIENDS_MATCH_VALID
    case DWC_MATCH_COMMAND_FRIEND_ACCEPT:
        if ((native_fn_020a3d70()->qr2MatchType == DWC_MATCH_TYPE_FRIEND) &&
            !native_fn_020a3d70()->distantFriend) {
            for (i = 1; i <= native_fn_020a3d70()->gt2NumConnection; i++) {
                if (native_fn_020a3d70()->sbPidList[i] == srcPid) {
                    DWC_Printf(DWC_REPORTFLAG_MATCH_NN,
                               "New client was accepted? - %d.\n", data[0]);
                    if (!data[0]) {
                        if ((native_fn_020a3d70()->state == DWC_MATCH_STATE_SV_OWN_NN) ||
                            (native_fn_020a3d70()->state == DWC_MATCH_STATE_SV_OWN_GT2)) {
                            result = native_fn_020a2150();
                            if (native_fn_020a1258(result)) return FALSE;
                        }
                        if (native_fn_020a3d70()->nnInfo.cookie) {
                            native_fn_020b6c90(native_fn_020a3d70()->nnInfo.cookie);
                            native_fn_020a3d70()->nnInfo.cookie = 0;
                        }
                        native_fn_020a2290();
                    } else {
                        native_fn_020a3d70()->friendAcceptBit |=
                            1u << native_fn_020a2c38(srcPid, FALSE);
                    }
                    break;
                }
            }
        }
        break;
#endif
    case DWC_MATCH_COMMAND_CL_WAIT_POLL:
        for (i = 1; i <= native_fn_020a3d70()->gt2NumConnection; i++) {
            if (native_fn_020a3d70()->sbPidList[i] == srcPid) {
                result = native_fn_020a00ac(DWC_MATCH_COMMAND_SV_KA_TO_CL,
                                               srcPid, srcIP, srcPort,
                                               NULL, 0);
                if (native_fn_020a1258(result)) return FALSE;
                else break;
            }
        }
        break;
    case DWC_MATCH_COMMAND_SV_KA_TO_CL:
        break;
    default:
        DWC_Printf(DWC_REPORTFLAG_ERROR,
                   "Received unexpected matching command 0x%02x.\n",
                   command);
        break;
    }
    return TRUE;
}
