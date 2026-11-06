typedef unsigned long u32;
typedef signed long s32;
typedef struct RTCTime {
	u32 hour;
	u32 minute;
	u32 second;
} RTCTime;
void native_main_0200fdd0(RTCTime * time, s32 sec);
void native_main_0200fdd0 (RTCTime * time, s32 sec)
{
    if (sec < 0) {
        sec = 0;
    }
    if (sec > 86399) {
        sec = 86399;
    }
    time->second = (u32)(sec % 60);
    sec /= 60;
    time->minute = (u32)(sec % 60);
    sec /= 60;
    time->hour = (u32)sec;
}
