#include <stdio.h>
#include "aHeader.h"

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

