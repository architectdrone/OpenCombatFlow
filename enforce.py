#Purpose: To enforce the format of blocks and dice-strings.
import character

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
        
