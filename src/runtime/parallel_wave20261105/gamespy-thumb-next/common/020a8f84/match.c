#include "context.h"
int native_main_020a8f84(int low, int high)
{
	unsigned int range = (unsigned int)high-low;
	int num;
	
	if (range == 0)
		return (low); 

	num = (int)(native_fn_020a8f54() % range);

	return(num + low);
}
