// This is a silly header file
//
//

#define A_STRING_DEF "a string value"
#define AN_INT_DEF 1234

#define A_MACRO(A_MARCO_ARG_1, A_MACRO_ARG_2) A_MACRO_ARG_1##A_MACRO_ARG_2

#ifndef OUTER
#ifdef WEIRD || LUMA

#define SECTION_A

#elif defined(LEEMA)

#define SECTION_B

#else

#define SECTION_C

    typedef struct {
        int anInt;
        char* aString;
    } AStruct;

#endif

#elif defined(OUTER_OTHER) // OUTER

#define SECTION_D

#else

#define SECTION_E

#endif // OUTER

void aFuncWithStruct(AStruct* aRef);

void aFuncWithInt(int anInt);

