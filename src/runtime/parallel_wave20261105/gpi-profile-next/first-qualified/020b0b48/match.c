#include "context.h"
void
native_main_020b0b48(
  GPConnection * connection,
  GPIProfile * profile
)
{
	GPIConnection * iconnection = (GPIConnection*)*connection;
	TableRemove(iconnection->profileList.profileTable, profile);
}
