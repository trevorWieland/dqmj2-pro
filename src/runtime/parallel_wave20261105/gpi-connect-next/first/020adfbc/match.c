#include "context.h"
GPIBool
native_main_020adfbc(
  int day,
  int month,
  int year
)
{
	
	
	if((day == 0) && (month == 0) && (year == 0))
		return GPITrue;

	
	
	if((day < 0) || (month < 0) || (year < 0))
		return GPIFalse;

	
	
	switch(month)
	{
	
	
	case 0:
		
		
		if(day != 0)
			return GPIFalse;
		break;

	
	
	case 1:
	case 3:
	case 5:
	case 7:
	case 8:
	case 10:
	case 12:
		if(day > 31)
			return GPIFalse;
		break;

	
	
	case 4:
	case 6:
	case 9:
	case 11:
		if(day > 30)
			return GPIFalse;
		break;

	
	
	case 2:
		
		
		if((((year % 4) == 0) && ((year % 100) != 0)) || ((year % 400) == 0))
		{
			if(day > 29)
				return GPIFalse;
		}
		else
		{
			if(day > 28)
				return GPIFalse;
		}
		break;

	
	
	default:
		return GPIFalse;
	}

	
	
	
	
	if(year < 1900)
		return GPIFalse;
	if(year > 2079)
		return GPIFalse;
	if(year == 2079)
	{
		if(month > 6)
			return GPIFalse;
		if((month == 6) && (day > 6))
			return GPIFalse;
	}

	return GPITrue;
}
