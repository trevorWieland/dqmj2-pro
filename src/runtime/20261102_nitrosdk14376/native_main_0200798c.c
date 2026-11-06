typedef unsigned short int u16;
extern u16 native_data_main_020e36f0;
void native_main_0200798c(int timerNum);
void native_main_0200798c (int timerNum)
{
    native_data_main_020e36f0 &= ~(1 << timerNum);
}
