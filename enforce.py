#Purpose: To enforce the format of blocks and dice-strings.
import character

def enforceDiceString(diceString):
    #Not implemented
    pass

def enforceActionBlock(action):
    #Make sure required keys are present.
    assert 'range' in action, "ActionBlocks require range key (Type: RangeBlock)."
    assert 'user' in action, "ActionBlocks require user key (Type: character)"
    assert 'name' in action, "ActionBlocks require name key (Type: string)"

    #Make sure that correct types are given, and that dice strings are valid.
    assert type(action['range']) == dict
    assert type(action['user']) == character
    assert type(action['name']) == str
    assert type(action['damage']) == dict
    for key in action['damage']:
        assert type(action['damage'][key]) == str or type(action['damage'][key]==int)
        enforceDiceString(action['damage'][key])
    assert type(action['effects']) == dict
    for key in action['effects']:
        assert type(action['damage'][key]) == int or type(action['effects'][key]) == int
        enforceDiceString(action['damage'][key])
    assert type(action['chance']) == str
    assert type(action['failureCondition']) == dict
    
    