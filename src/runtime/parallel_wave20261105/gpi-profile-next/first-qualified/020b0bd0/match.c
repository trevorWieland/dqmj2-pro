#include "context.h"
GPIBool
native_main_020b0bd0(
  GPConnection * connection,
  gpiProfileMapFunc func,
  void * data
)
{
	GPIConnection * iconnection = (GPIConnection*)*connection;
	GPIProfileMapData mapData;
	mapData.connection = connection;
	mapData.func = func;
	mapData.data = data;
	return (!TableMapSafe2(iconnection->profileList.profileTable, gpiProfileMapCallback, &mapData)) ? GPITrue:GPIFalse;
}
