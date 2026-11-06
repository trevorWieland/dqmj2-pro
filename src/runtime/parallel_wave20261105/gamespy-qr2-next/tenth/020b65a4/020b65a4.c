#include "context.h"
NATNegotiator native_main_020b65a4()
{
	struct _NATNegotiator _neg = {0};
	if (native_data_021d2bc4 == NULL)
		native_data_021d2bc4 = native_fn_020a85dc(sizeof(_neg), 4, NULL);
	native_fn_020a865c(native_data_021d2bc4, &_neg);
	return (NATNegotiator)native_fn_020a8644(native_data_021d2bc4, native_fn_020a8640(native_data_021d2bc4) - 1);
}
