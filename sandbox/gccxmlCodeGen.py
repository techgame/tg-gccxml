##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##
##~ Copyright (C) 2002-2005  TechGame Networks, LLC.              ##
##~                                                               ##
##~ This library is free software; you can redistribute it        ##
##~ and/or modify it under the terms of the BSD style License as  ##
##~ found in the LICENSE file included with this distribution.    ##
##~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~##

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Imports 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from gccxmlParser import ElementVisitor

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#~ Definitions 
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CTypesCodeGen(ElementVisitor):
    useDirectCall = True

    # simple types
    basicTypeCodeMap = {
        'void': 'c_void',
        'char': 'c_char',
        'signed char': 'c_byte',
        'unsigned char': 'c_ubyte',
        'short int': 'c_short',
        'short unsigned int': 'c_ushort',
        'int': 'c_int',
        'unsigned int': 'c_uint',
        'long int': 'c_long',
        'long unsigned int': 'c_ulong',
        'float': 'c_float',
        'double': 'c_double',

        'long double': None,
        'complex float': None,
        'complex double': None,
        'complex long double': None,
        }
    def onFundamentalType(self, item, lookup): 
        return self.basicTypeCodeMap[item.name]

    def onCvQualifiedType(self, item, lookup):
        return self._getTypeRef(item.type, lookup)
        #if item.const:
        #    modifier = 'const'
        #elif item.volatile:
        #    modifier = 'volatile'
        #return result + ' # modifier: ' + modifier

    def onEnumeration(self, item, lookup):
        raise NotImplementedError('TODO')
    def onEnumValue(self, item, lookup):
        raise NotImplementedError('TODO')

    # complex types and pointers
    def onTypedef(self, item, lookup): 
        result = self._getTypeRef(item.type, lookup)
        return '%s = %s' % (item.name, result)
    def onPointerType(self, item, lookup): 
        result = self._getTypeRef(item.type, lookup)
        return 'POINTER(%s)' % (result,)
    def onReferenceType(self, item, lookup): 
        result = self._getTypeRef(item.type, lookup)
        return 'POINTER(%s)' % (result,)
    def onArrayType(self, item, lookup): 
        pass

    # preprocessor
    def onDefine(self, item, lookup): 
        return '%s = %s' % (item.name, item.body)
    def onMacro(self, item, lookup): 
        return '#TODO: #define %s(%s) %s' % (item.name, item.params, item.body)

    # callables
    def onFunction(self, item, lookup): 
        returnType = self._getTypeRef(item.returns, lookup)
        argTypes = ', '.join([self._getArgumentType(arg, lookup) for arg in item.arguments])
        argNames = ', '.join([self._getArgumentName(arg, lookup, d) for d, arg in enumerate(item.arguments)])
        result = []

        result.append('@argtypes(%s, [%s])' % (returnType, argTypes,))

        if self.useDirectCall:
            result.extend( [
                'def %s(%s):' % (item.name, argNames),
                "    '''from: %s (%s)'''" % (lookup.lookupFilename(item.file), item.line),
                ])
        else:
            result.extend( [
                'def %s(%s):' % (item.name, argNames),
                "    '''from: %s (%s)'''" % (lookup.lookupFilename(item.file), item.line),
                '    return %s._api_(%s)' % (item.name, argNames),
                ''])
        return '\n'.join(result)

    def _getArgumentType(self, item, lookup): 
        if item.isEllipsisArgument():
            raise NotImplementedError('C/C++ Ellipsis arguments are not yet supported')
        return self._getTypeRef(item.type, lookup)

    def _getArgumentName(self, item, lookup, idx): 
        if item.isEllipsisArgument():
            raise NotImplementedError('C/C++ Ellipsis arguments are not yet supported')
        argName = item.name or ('arg%d' % idx)
        return argName

    def onFunctionType(self, item, lookup): 
        returnType = self._getTypeRef(item.returns, lookup)
        argTypes = ', '.join([self._getArgumentType(arg, lookup) for arg in item.arguments])
        if argTypes:
            return "CFUNCTYPE(%s, %s)" % (returnType, argTypes)
        else:
            return "CFUNCTYPE(%s)" % (returnType, )
    def onStruct(self, item, lookup): 
        return item.name
    def onUnion(self, item, lookup): 
        return item.name

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def _getTypeRef(self, type, lookup):
        typeItem = lookup.lookupType(type)
        if typeItem.isTypedef():
            return typeItem.name
        else:
            return typeItem.visit(self, lookup)

