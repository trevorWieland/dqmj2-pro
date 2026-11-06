#include "context.h"
GPResult
native_main_020b0600(
  GPConnection * connection,
  GPIPeer * peer,
  int type,
  const struct GPITransferID_s * transferID
)
{
	char buffer[64];
	GPITransferID tid;
	tid.count = transferID->count;
	tid.profileid = transferID->profileid;
	tid.time = transferID->time;

	GS_ASSERT(transferID);
	if (!transferID)
		return GP_NETWORK_ERROR;
	
	
	sprintf(buffer, native_data_020e10ac, type, tid.profileid, tid.count, tid.time);

	return gpiSendOrBufferString(connection, peer, buffer);
}