#include "context.h"
GPResult
native_main_020ae948(
  GPConnection * connection, 
  GPEnum info, 
  int value
)
{
	char intValue[16];

	
	
	switch(info)
	{
	case GP_ZIPCODE:
		
		
		if(value < 0)
			Error(connection, GP_PARAMETER_ERROR, native_data_020e0e08);

		
		
		sprintf(intValue,native_data_020e0e1c,value);

		
		
		CHECK_RESULT(gpiSendLocalInfo(connection, native_data_020e0d10, intValue));

		break;

	case GP_SEX:
		
		
		switch(value)
		{
		case GP_MALE:
			CHECK_RESULT(gpiSendLocalInfo(connection, native_data_020e0d50, native_data_020e0e20));
			break;

		case GP_FEMALE:
			CHECK_RESULT(gpiSendLocalInfo(connection, native_data_020e0d50, native_data_020e0e24));
			break;

		case GP_PAT:
			CHECK_RESULT(gpiSendLocalInfo(connection, native_data_020e0d50, native_data_020e0e28));
			break;

		default:
			Error(connection, GP_PARAMETER_ERROR, native_data_020e0e2c);
		}

		break;

	case GP_ICQUIN:
		
		
		sprintf(intValue,native_data_020e0e1c,value);

		
		
		CHECK_RESULT(gpiSendLocalInfo(connection, native_data_020e0cf8, intValue));

		break;
		
	case GP_CPUBRANDID:
		
		
		sprintf(intValue,native_data_020e0e1c,value);

		
		
		CHECK_RESULT(gpiSendUserInfo(connection, native_data_020e0e3c, intValue));

		break;

	case GP_CPUSPEED:
		
		
		sprintf(intValue,native_data_020e0e1c,value);

		
		
		CHECK_RESULT(gpiSendUserInfo(connection, native_data_020e0e4c, intValue));

		break;

	case GP_MEMORY:
		
		
		value /= 16;

		
		
		sprintf(intValue,native_data_020e0e1c,value);

		
		
		CHECK_RESULT(gpiSendUserInfo(connection, native_data_020e0e58, intValue));

		break;

	case GP_VIDEOCARD1RAM:
		
		
		value /= 4;

		
		
		sprintf(intValue,native_data_020e0e1c,value);

		
		
		CHECK_RESULT(gpiSendUserInfo(connection, native_data_020e0e64, intValue));

		break;

	case GP_VIDEOCARD2RAM:
		
		
		value /= 4;

		
		
		sprintf(intValue,native_data_020e0e1c,value);

		
		
		CHECK_RESULT(gpiSendUserInfo(connection, native_data_020e0e74, intValue));

		break;

	case GP_CONNECTIONID:
		
		
		sprintf(intValue,native_data_020e0e1c,value);

		
		
		CHECK_RESULT(gpiSendUserInfo(connection, native_data_020e0e84, intValue));

		break;

	case GP_CONNECTIONSPEED:
		
		
		sprintf(intValue,native_data_020e0e1c,value);

		
		
		CHECK_RESULT(gpiSendUserInfo(connection, native_data_020e0e94, intValue));

		break;

	case GP_HASNETWORK:
		
		
		if(value)
			value = 1;

		
		
		sprintf(intValue,native_data_020e0e1c,value);

		
		
		CHECK_RESULT(gpiSendUserInfo(connection, native_data_020e0ea8, intValue));

		break;

	case GP_PIC:
		
		
		sprintf(intValue,native_data_020e0e1c,value);

		
		
		CHECK_RESULT(gpiSendLocalInfo(connection, native_data_020e0d68, intValue));

		break;

	case GP_OCCUPATIONID:
		
		
		sprintf(intValue,native_data_020e0e1c,value);

		
		
		CHECK_RESULT(gpiSendLocalInfo(connection, native_data_020e0d70, intValue));

		break;

	case GP_INDUSTRYID:
		
		
		sprintf(intValue,native_data_020e0e1c,value);

		
		
		CHECK_RESULT(gpiSendLocalInfo(connection, native_data_020e0d78, intValue));

		break;

	case GP_INCOMEID:
		
		
		sprintf(intValue,native_data_020e0e1c,value);

		
		
		CHECK_RESULT(gpiSendLocalInfo(connection, native_data_020e0d80, intValue));

		break;

	case GP_MARRIEDID:
		
		
		sprintf(intValue,native_data_020e0e1c,value);

		
		
		CHECK_RESULT(gpiSendLocalInfo(connection, native_data_020e0d88, intValue));

		break;

	case GP_CHILDCOUNT:
		
		
		sprintf(intValue,native_data_020e0e1c,value);

		
		
		CHECK_RESULT(gpiSendLocalInfo(connection, native_data_020e0d90, intValue));

		break;

	case GP_INTERESTS1:
		
		
		sprintf(intValue,native_data_020e0e1c,value);

		
		
		CHECK_RESULT(gpiSendLocalInfo(connection, native_data_020e0d98, intValue));

		break;

	default:
		Error(connection, GP_PARAMETER_ERROR, native_data_020e0eb8);
	}

	return GP_NO_ERROR;
}