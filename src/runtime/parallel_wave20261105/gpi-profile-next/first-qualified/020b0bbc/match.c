#include "context.h"
int
native_main_020b0bbc(
  void *arg,
  void *udata
)
{
	GPIProfile * profile = (GPIProfile *)arg;
	GPIProfileMapData * data = (GPIProfileMapData *)udata;
	return (int)data->func(data->connection, profile, data->data);
}
