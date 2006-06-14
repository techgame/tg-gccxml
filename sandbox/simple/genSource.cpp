#include <stdio.h>
#include "aHeader.h"

long aLong;
long long aLongLong;

unsigned long anUnsignedLong;
long unsigned long aLongUnsignedLong;

float aFloat;
double aDouble;
long double aLongDouble;

enum anEnum {
    value0,
    value1,
    value42=42,
};

class AClass {
    public:
        anEnum anEnumMember;
        
};
class BClass : public AClass {
    protected:
        int aValue;
        virtual int* aMethod(int aMethodArg);
    public:
        virtual ~BClass() { }
};
