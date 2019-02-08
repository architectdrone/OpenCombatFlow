#Purpose: To enforce the format of blocks and dice-strings.
from character import Character

'''
ENFORCEMENT BLOCK
    (NOTE)
    I decided not to add this to the DSD, because 1). It is only relevant for the purpose of rapid development of protocol enforcement, and 2). It has a list as the top level structure, not a dictionary.

    (LIST)
    At the top level, the enforcementBlock is a list. Each element of the list corresponds to an element specified by the DSD. At each index in the list, there is a dictionary detailing information about the elemtn, as defined below.
        (MANDATORY)
        "name": The name of the key. (string)
        "type": The type of the element at the key. This can be a type (eg, 'int', 'str', etc.) or a string, specifying a specific type of block.

        (CONDITIONALLY MANDATORY)
        "dictElement": What type of element each key in a dictionary must be of. Only nessesary if "type" is dict.

        (NON-MANDATORY)
        "mandatory": If true, this key must be present. Otherwise, or if it not provided, it is assumed to be non-mandatory.
        
'''
def enforce(blockToCheck, blockType):
    '''
    Enforce rules for the given blockType.
    '''

def _enforceDiceString(diceString):
    '''
    PRIVATE: Makes sure the dice string is a valid dice string.
    '''
    pass


def _enforceType(toCheck, requestedType, dictElement = None):
    '''
    PRIVATE: Checks to make sure that variables match specifications for types. Depending upon the value of requestedType, this has different tests that it performs:
    -If requestedType is a Type, it will check to make sure that toCheck is of that type.
    -If requestedType is a Type of dict, and dictElement is not None, raise an error if each element of the dictionary is not of dictElement.
    -If requestedType is a string equal to "DS", it makes sure that toCheck is a valid dice string.
    -If requestedType is any string besides "DS", it checks that toCheck is a valid block of the type requestedType.
    '''
    if type(requestedType) == type: #If we are doing a check of a 'normal' variable test. (IE, not specified by a string.) We tell this by seeing if requestedType is of type type, or of type string
        if type(toCheck) != requestedType: #See if the types match. 
            raise KeyError #If they don't match, raise an error.
        if requestedType == dict and dictElement is not None: #If the type is a dictionary, run additional testing of the given dictionary.
            for internalKey in toCheck: #Check each individual key in the dictionary.
                _enforceType(internalKey, dictElement) #Test each element.
    elif type(requestedType) == str: #If the requestedType is a string, perform special testing, including block and dicestring, as specified by the string.
        if requestedType == "DS": #If requested type is 'DS', we enforce the dice string.
            _enforceDiceString(toCheck)
        else: #If it is not 'DS', we assume that it is a specification of a block, and we let enforce take care of it.
            enforce(toCheck, requestedType)

def _enforceHelper(blockToCheck, enforcementBlock):
    '''
    PRIVATE: This is to enforce protocols using a pre-determined enforcement block. Please use an appropriate front-end channel to access this functionality.
    '''

    for keyToCheck in enforcementBlock:
        #Check if mandatory elements are present.
        keyName = keyToCheck['name']
        if keyToCheck.get('mandatory', default=False) == True and keyName not in blockToCheck:
            raise KeyError(f"The Key {keyName} must be present in this block.")
        elif keyName not in blockToCheck:
            continue

        #Check if given values were consistent with required values.
        element = blockToCheck[keyName]
        if type(keyToCheck['type']) == type:
            if type(element) != keyToCheck['type']: #Does the key in blockToCheck have the correct type?
                raise KeyError(f"The Key {keyName} must be of type {keyToCheck['type']}, not of type {type(element)}")
            elif keyToCheck['type'] == dict: #Should we perform additional testing on the dictionary?
                for internalKey in element:
                    if type(element[internalKey]) != keyToCheck['dictElement']:
                        raise KeyError(f"The Key {internalKey} within the key {keyName} must be of type {keyToCheck['dictElement']}, not of type {type(element[internalKey])}")
        elif type(keyToCheck['type']) == str: #Should we do block testing?
            enforce(element, keyToCheck['type'])
        