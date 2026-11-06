#include "context.h"
void native_main_020b28c0
(
  GPConnection * connection,
  GPIPeer * peer,
  int type,
  const char * headers,
  const char * buffer,
  int len
)
{
	char value[64];
	GPITransferID transferID;
#ifndef NOFILE
	GPITransfer * transfer;
	GPIBool success;
#endif

	
	
	if(!gpiValueForKey(headers, native_data_020e1520, value, sizeof(value)))
		return;
	if(sscanf(value, native_data_020e1528, &transferID.profileid, &transferID.count, &transferID.time) != 3)
		return;

#ifdef NOFILE
	gpiSendTransferReply(connection, &transferID, peer, GPI_NOT_ACCEPTING, NULL);
#else

	
	
	if(type == GPI_BM_FILE_SEND_REQUEST)
	{
		
		
		if(!gpiHandleSendRequest(connection, peer, &transferID, headers, buffer, len))
			gpiSendTransferReply(connection, &transferID, peer, GPI_NOT_ACCEPTING, NULL);

		return;
	}

	
	
	transfer = gpiFindTransferByTransferID(connection, &transferID);
	if(!transfer || (transfer->peer != peer))
		return;

	
	
	switch(type)
	{
		case GPI_BM_FILE_SEND_REPLY:
			success = gpiHandleSendReply(connection, transfer, headers, buffer, len);
			break;
		case GPI_BM_FILE_BEGIN:
			success = gpiHandleBegin(connection, transfer, headers);
			break;
		case GPI_BM_FILE_END:
			success = gpiHandleEnd(connection, transfer, headers);
			break;
		case GPI_BM_FILE_DATA:
			success = gpiHandleData(connection, transfer, headers, buffer, len);
			break;
		case GPI_BM_FILE_SKIP:
			success = gpiHandleSkip(connection, transfer, headers);
			break;
		case GPI_BM_FILE_TRANSFER_THROTTLE:
			success = gpiHandleTransferThrottle(connection, transfer, headers);
			break;
		case GPI_BM_FILE_TRANSFER_CANCEL:
			success = gpiHandleTransferCancel(connection, transfer);
			break;
		case GPI_BM_FILE_TRANSFER_KEEPALIVE:
			success = gpiHandleTransferKeepalive(connection, transfer);
			break;
		default:
			success = GPITrue;
	}

	
	
	if(!success)
		gpiTransferError(connection, transfer);
#endif

	GSI_UNUSED(type);
	GSI_UNUSED(buffer);
	GSI_UNUSED(len);
}
