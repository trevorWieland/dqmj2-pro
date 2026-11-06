#include "context000.h"

int native_main_0207ffb4(const void *needle,Match *result){
    u16 row,column;
    for(row=0;row<105;++row){
        for(column=0;column<4;++column){
            if(native_fn_0201b248(needle,native_data_020db298[row][column],3)==0){
                result->row=row;result->column=column;return 1;
            }
        }
    }
    return 0;
}
