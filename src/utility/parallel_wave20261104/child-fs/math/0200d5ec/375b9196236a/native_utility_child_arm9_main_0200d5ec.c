#include "dependency000.h"

RTCWeek native_utility_child_arm9_main_0200d5ec (RTCDate * date)
{
    int cent;
    int year = (int)(2000 + date->year);
    int month = (int)date->month;
    int day = (int)date->day;
    month -= 2;
    if (month < 1) {
        month += 12;
        --year;
    }
    cent = year / 100;
    year %= 100;
    return (RTCWeek)(((26 * month - 2) / 10 + day + year + year / 4 + cent / 4 + 5 * cent) % 7);
}
